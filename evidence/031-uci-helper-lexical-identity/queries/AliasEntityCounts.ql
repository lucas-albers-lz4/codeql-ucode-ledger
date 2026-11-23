/** Count distinct AST entities in the alias eligibility diagnostic. */
import codeql.ucode.m3.Models
import codeql.ucode.ast.Variables
import codeql.ucode.ast.internal.AstNodes
import codeql.ucode.ast.internal.TreeSitter

private predicate aliasCandidate(NamedCall site, UCODE::FunctionDeclaration helper,
  UCODE::CallExpression forward, UCODE::Identifier arg, VariableReadAccess read) {
  site.getName() = "ubus_call" and sameFileCall(site, helper) and
  stringLiteralValue(site.getArgument(0).(UCODE::String)) = "uci" and
  stringLiteralValue(site.getArgument(1).(UCODE::String)) = "commit" and
  forward.getParent*() = helper.getBody() and
  forward.getFunction().(UCODE::MemberExpression).getObject().(UCODE::Identifier).getValue() = "ubus" and
  forward.getFunction().(UCODE::MemberExpression).getProperty().(UCODE::PropertyIdentifier).getValue() = "call" and
  arg = forward.getArguments().getChild(1) and read.getAstNode() = TIdentifier(arg) and
  read.getVariable().getAstNode() != TIdentifier(helper.getParameters().getChild(1))
}

from NamedCall site, UCODE::FunctionDeclaration helper, UCODE::CallExpression forward,
  int forwardEntities, int argumentEntities, int localTargets
where
  site.getName() = "ubus_call" and sameFileCall(site, helper) and
  forwardEntities = count(UCODE::CallExpression candidate |
    exists(UCODE::Identifier arg, VariableReadAccess read | aliasCandidate(site, helper, candidate, arg, read))) and
  argumentEntities = count(UCODE::Identifier arg |
    exists(UCODE::CallExpression candidate, VariableReadAccess read | aliasCandidate(site, helper, candidate, arg, read))) and
  localTargets = count(Variable target |
    exists(UCODE::CallExpression candidate, UCODE::Identifier arg, VariableReadAccess read |
      aliasCandidate(site, helper, candidate, arg, read) and target = read.getVariable())) and
  aliasCandidate(site, helper, forward, _, _)
select site, forward,
  "distinct alias entities: calls=" + forwardEntities.toString() +
  ", arg1 identifiers=" + argumentEntities.toString() + ", variable targets=" + localTargets.toString()
