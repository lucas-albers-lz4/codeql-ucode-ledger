/** @name Issue 156 testing-only commit/restart adjacency observation
 * @description Bounded syntactic experiment; not a production security rule.
 * @kind table
 * @id scratch/issue-156-candidate-adjacency
 */
import codeql.files.FileSystem
import codeql.ucode.AST
import codeql.ucode.ast.internal.AstNodes
import codeql.ucode.ast.internal.TreeSitter
import codeql.ucode.m3.Models

predicate selected(UCODE::AstNode n) {
  n.getLocation().getFile().getRelativePath() = "usr/share/rpcd/ucode/luci.adblock-fast" or
  n.getLocation().getFile().getRelativePath().matches("controls/%")
}

predicate plain(UCODE::String s, string value) {
  s.getChild(0).(UCODE::StringFragment).getValue() = value and not exists(s.getChild(1))
}

predicate functionNode(UCODE::AstNode n) {
  n instanceof UCODE::FunctionExpression or n instanceof UCODE::FunctionDeclaration or
  n instanceof UCODE::ArrowFunction
}

predicate nearestFunction(UCODE::AstNode n, UCODE::FunctionExpression f) {
  n.getParent+() = f and
  not exists(UCODE::AstNode inner | functionNode(inner) and n.getParent+() = inner and inner.getParent+() = f)
}

predicate rawWrite(UCODE::Identifier id) {
  exists(UCODE::AssignmentExpression a | a.getLeft() = id) or
  exists(UCODE::AugmentedAssignmentExpression a | a.getLeft() = id) or
  exists(UCODE::UpdateExpression u | u.getArgument() = id) or
  exists(UCODE::ForInStatement f | not exists(f.getKind()) and
    (f.getVariable() = id or f.getKey() = id or f.getValue() = id)) or
  exists(UCODE::ForInAltStatement f | not exists(f.getKind()) and
    (f.getVariable() = id or f.getKey() = id or f.getValue() = id))
}

predicate namedCursorImport(UCODE::ImportStatement imp, UCODE::ImportSpecifier spec) {
  spec = imp.getClause().getNamed().getChild(_) and
  spec.getName().(UCODE::Identifier).getValue() = "cursor" and
  not exists(spec.getAlias()) and plain(imp.getSource(), "uci") and
  imp.getParent() instanceof UCODE::Program
}

predicate safeFileBindings(UCODE::ImportStatement imp, UCODE::ImportSpecifier spec) {
  namedCursorImport(imp, spec) and
  not exists(UCODE::ImportSpecifier other | other.getLocation().getFile() = imp.getLocation().getFile() and other != spec and
    (other.getName().(UCODE::Identifier).getValue() = "cursor" or other.getAlias().getValue() = "cursor")) and
  not exists(UCODE::VariableDeclarator d | d.getLocation().getFile() = imp.getLocation().getFile() and d.getName().getValue() = "cursor") and
  not exists(UCODE::Identifier formal | formal.getLocation().getFile() = imp.getLocation().getFile() and
    formal.getValue() = "cursor" and formal.getParent() instanceof UCODE::FormalParameters) and
  not exists(UCODE::FunctionDeclaration d | d.getLocation().getFile() = imp.getLocation().getFile() and d.getName().getValue() = "cursor") and
  not exists(UCODE::Identifier id | id.getLocation().getFile() = imp.getLocation().getFile() and id.getValue() = "cursor" and
    (exists(UCODE::RestElement rest | rest.getChild() = id) or
     exists(UCODE::ArrowFunction arrow | arrow.getParameter() = id) or
     exists(UCODE::CatchClause c | c.getParameter() = id) or
     exists(UCODE::FunctionExpression f | f.getName() = id) or
     exists(UCODE::ForInStatement f | exists(f.getKind()) and (f.getVariable() = id or f.getKey() = id or f.getValue() = id)) or
     exists(UCODE::ForInAltStatement f | exists(f.getKind()) and (f.getVariable() = id or f.getKey() = id or f.getValue() = id)) or
     exists(UCODE::ImportClause clause | clause.getDefault() = id or clause.getNamespace().getChild() = id))) and
  not exists(UCODE::Identifier id | id.getLocation().getFile() = imp.getLocation().getFile() and
    id.getValue() = ["cursor", "uci_ctx", "system"] and rawWrite(id))
}

predicate sourceBefore(UCODE::AstNode first, UCODE::AstNode second) {
  first.getLocation().getFile() = second.getLocation().getFile() and
  (first.getLocation().getStartLine() < second.getLocation().getStartLine() or
   first.getLocation().getStartLine() = second.getLocation().getStartLine() and
   first.getLocation().getStartColumn() < second.getLocation().getStartColumn())
}

predicate siblings(UCODE::AstNode owner, int i, UCODE::ExpressionStatement first, UCODE::ExpressionStatement second) {
  exists(UCODE::StatementBlock b | owner = b and first = b.getChild(i) and second = b.getChild(i + 1)) or
  exists(UCODE::SwitchCase c | owner = c and first = c.getBody(i) and second = c.getBody(i + 1))
}

from UCODE::ImportStatement imp, UCODE::ImportSpecifier spec, UCODE::VariableDeclarator decl,
  UCODE::CallExpression init, UCODE::Identifier initName, VariableReadAccess read,
  UCODE::Identifier receiver, UCODE::MemberExpression member, UCODE::CallExpression commit,
  UCODE::String packageLiteral, UCODE::CallExpression restart, BuiltinSystemCall builtin,
  UCODE::String commandLiteral, UCODE::ExpressionStatement first, UCODE::ExpressionStatement second,
  UCODE::AstNode owner, UCODE::FunctionExpression fn, int i, string packageName, string command, string service
where
  selected(imp) and safeFileBindings(imp, spec) and
  decl.getLocation().getFile() = imp.getLocation().getFile() and decl.getName().getValue() = "uci_ctx" and
  decl.getParent() instanceof UCODE::LexicalDeclaration and init = decl.getValue() and
  initName = init.getFunction() and initName.getValue() = "cursor" and
  not exists(init.getOptionalChain()) and not exists(init.getArguments().getChild(0)) and
  receiver = member.getObject() and receiver.getValue() = "uci_ctx" and member.getProperty().getValue() = "commit" and
  not exists(member.getOptionalChain()) and commit.getFunction() = member and not exists(commit.getOptionalChain()) and
  packageLiteral = commit.getArguments().getChild(0) and not exists(commit.getArguments().getChild(1)) and plain(packageLiteral, packageName) and
  toTreeSitter(read.getAstNode()) = receiver and toTreeSitter(read.getVariable().getAstNode()) = decl and
  restart = builtin and not exists(restart.getOptionalChain()) and
  commandLiteral = restart.getArguments().getChild(0) and not exists(restart.getArguments().getChild(1)) and plain(commandLiteral, command) and
  command.regexpMatch("/etc/init[.]d/[A-Za-z0-9_-]+ restart >/dev/null 2>&1") and
  service = command.regexpCapture("/etc/init[.]d/([A-Za-z0-9_-]+) restart >/dev/null 2>&1", 1) and
  first.getChild() = commit and second.getChild() = restart and sourceBefore(first, second) and siblings(owner, i, first, second) and
  nearestFunction(first, fn) and nearestFunction(second, fn) and nearestFunction(decl, fn)
select imp.getLocation().getFile().getRelativePath() as path, fn as function_entity, imp as import_entity,
  spec as import_specifier_entity, decl as declaration_entity, init as initializer_entity, receiver as receiver_entity,
  owner as owner_entity, i as first_index, first as first_statement_entity, commit as commit_entity,
  packageLiteral as package_entity, packageName as package_name, second as second_statement_entity,
  restart as restart_entity, commandLiteral as command_entity, service as service_name, "restart" as action
