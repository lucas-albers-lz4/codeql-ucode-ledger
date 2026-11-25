/** @name Issue 155 imported local identifier witnesses
 * @kind table
 * @id scratch/issue-155-duplicate-import-witness
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

from UCODE::ImportStatement imp, UCODE::Identifier id
where imp.getLocation().getFile().getRelativePath() = ["controls/positive-direct.uc", "controls/negative-duplicate.uc"] and id = statImportBinding(imp) and id.getValue() = "stat"
select imp.getLocation().getFile().getRelativePath() as path, imp as import_node, id as identifier,
 imp.getLocation().getStartLine() as import_line, imp.getLocation().getStartColumn() as import_column, id.getLocation().getStartLine() as identifier_line, id.getLocation().getStartColumn() as identifier_column
