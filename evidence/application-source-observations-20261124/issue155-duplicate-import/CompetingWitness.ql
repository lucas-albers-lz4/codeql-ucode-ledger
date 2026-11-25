/** @name Issue 155 duplicate import guard witnesses
 * @kind table
 * @id scratch/issue-155-duplicate-guard-witness
 */
import codeql.files.FileSystem
import codeql.ucode.ast.internal.TreeSitter
/** A local identifier introduced by any import clause in `imp`. */
private UCODE::Identifier statImportBinding(UCODE::ImportStatement imp) {
  exists(UCODE::ImportSpecifier spec |
    spec = imp.getClause().getNamed().getChild(_) and
    (result = spec.getAlias() or not exists(spec.getAlias()) and result = spec.getName())
  )
  or result = imp.getClause().getDefault()
  or result = imp.getClause().getNamespace().getChild()
}

/** Competing binding or write, checked across the entire file. */
private predicate statCompetingBindingOrWrite(UCODE::Identifier id) {
  exists(UCODE::VariableDeclarator d | d.getName() = id)
  or exists(UCODE::FunctionDeclaration f | f.getName() = id)
  or exists(UCODE::FunctionExpression f | f.getName() = id)
  or exists(UCODE::FormalParameters ps | id = ps.getChild(_))
  or exists(UCODE::RestElement rest, UCODE::FormalParameters ps |
    rest = ps.getChild(_) and id = rest.getChild()
  )
  or exists(UCODE::ArrowFunction f | f.getParameter() = id)
  or exists(UCODE::CatchClause c | c.getParameter() = id)
  or exists(UCODE::ForInStatement f | id = f.getVariable() or id = f.getKey() or id = f.getValue())
  or exists(UCODE::ForInAltStatement f | id = f.getVariable() or id = f.getKey() or id = f.getValue())
  or exists(UCODE::AssignmentExpression a | a.getLeft() = id)
  or exists(UCODE::AugmentedAssignmentExpression a | a.getLeft() = id)
  or exists(UCODE::UpdateExpression u | u.getArgument() = id)
}


from UCODE::Identifier id
where id.getLocation().getFile().getRelativePath() = ["controls/positive-direct.uc", "controls/negative-duplicate.uc"] and id.getValue() = "stat" and statCompetingBindingOrWrite(id)
select id.getLocation().getFile().getRelativePath() as path, id as identifier,
 id.getPrimaryQlClasses() as classes, id.getLocation().getStartLine() as line, id.getLocation().getStartColumn() as column
