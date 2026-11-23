/** Count distinct AST entities satisfying the observer's exact relation. */
import codeql.ucode.m3.Models
import codeql.ucode.ast.Variables
import codeql.ucode.ast.internal.AstNodes
import codeql.ucode.ast.internal.TreeSitter

private predicate forwards(UCODE::FunctionDeclaration f, UCODE::CallExpression call, int i) {
  exists(UCODE::Identifier formal, UCODE::Identifier arg, VariableReadAccess read |
    formal = f.getParameters().getChild(i) and
    arg = call.getArguments().getChild(i) and
    read.getAstNode() = TIdentifier(arg) and
    read.getVariable().getAstNode() = TIdentifier(formal)
  )
}

private predicate qualifies(NamedCall site, UCODE::FunctionDeclaration helper, UCODE::CallExpression forward) {
  site.getName() = "ubus_call" and sameFileCall(site, helper) and
  stringLiteralValue(site.getArgument(0).(UCODE::String)) = "uci" and
  stringLiteralValue(site.getArgument(1).(UCODE::String)) = "commit" and
  exists(site.getArgument(2)) and not exists(site.getArgument(3)) and
  forward.getParent*() = helper.getBody() and
  not exists(UCODE::AstNode nested |
    nested = forward.getParent+() and nested.getParent*() = helper.getBody() and
    (nested instanceof UCODE::FunctionDeclaration or nested instanceof UCODE::FunctionExpression or
      nested instanceof UCODE::ArrowFunction)
  ) and
  forward.getFunction().(UCODE::MemberExpression).getObject().(UCODE::Identifier).getValue() = "ubus" and
  forward.getFunction().(UCODE::MemberExpression).getProperty().(UCODE::PropertyIdentifier).getValue() = "call" and
  not exists(forward.getFunction().(UCODE::MemberExpression).getOptionalChain()) and
  not exists(forward.getOptionalChain()) and
  forwards(helper, forward, 0) and forwards(helper, forward, 1) and forwards(helper, forward, 2) and
  not exists(forward.getArguments().getChild(3)) and not exists(helper.getParameters().getChild(3))
}

from NamedCall site, int forwardEntities, int helperEntities
where
  forwardEntities > 0 and helperEntities > 0 and
  forwardEntities = count(UCODE::CallExpression forward |
    exists(UCODE::FunctionDeclaration helper | qualifies(site, helper, forward))) and
  helperEntities = count(UCODE::FunctionDeclaration helper |
    exists(UCODE::CallExpression forward | qualifies(site, helper, forward)))
select site, "distinct observer entities: forwarding calls=" + forwardEntities.toString() +
  ", helpers=" + helperEntities.toString()
