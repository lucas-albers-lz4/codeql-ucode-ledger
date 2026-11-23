/** Diagnostic for the lexical binding of argument 1 in the alias near miss. */
import codeql.ucode.m3.Models
import codeql.ucode.ast.Variables
import codeql.ucode.ast.internal.AstNodes
import codeql.ucode.ast.internal.TreeSitter

from NamedCall site, UCODE::FunctionDeclaration helper, UCODE::CallExpression forward,
  UCODE::Identifier arg, VariableReadAccess read
where
  site.getName() = "ubus_call" and sameFileCall(site, helper) and
  stringLiteralValue(site.getArgument(0).(UCODE::String)) = "uci" and
  stringLiteralValue(site.getArgument(1).(UCODE::String)) = "commit" and
  forward.getParent*() = helper.getBody() and
  forward.getFunction().(UCODE::MemberExpression).getObject().(UCODE::Identifier).getValue() = "ubus" and
  forward.getFunction().(UCODE::MemberExpression).getProperty().(UCODE::PropertyIdentifier).getValue() = "call" and
  arg = forward.getArguments().getChild(1) and read.getAstNode() = TIdentifier(arg) and
  read.getVariable().getAstNode() != TIdentifier(helper.getParameters().getChild(1))
select site, "caller/helper candidate; arg1 identifier resolves away from formal", forward, arg, read.getVariable().getAstNode()
