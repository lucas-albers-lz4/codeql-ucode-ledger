/** @name Issue 155 selected structural gate violations
 * @kind table
 * @id scratch/issue-155-duplicate-structural-violations
 */
import codeql.files.FileSystem
import codeql.ucode.ast.internal.TreeSitter

from UCODE::CallExpression call, UCODE::FunctionExpression handler, string violation
where
  call.getLocation().getFile() = handler.getLocation().getFile() and
  (call.getLocation().getFile().getRelativePath() = "controls/positive-direct.uc" and call.getLocation().getStartLine() = 9 and handler.getLocation().getStartLine() = 6 or
   call.getLocation().getFile().getRelativePath() = "controls/negative-duplicate.uc" and call.getLocation().getStartLine() = 10 and handler.getLocation().getStartLine() = 7) and
  (exists(call.getOptionalChain()) and violation = "optional-call" or
   exists(call.getArguments().getChild(1)) and violation = "extra-argument" or
   exists(handler.getParameters().getChild(1)) and violation = "extra-formal" or
   exists(UCODE::AstNode nested | nested = call.getParent+() and nested.getParent*() = handler.getBody() and
     (nested instanceof UCODE::FunctionExpression or nested instanceof UCODE::FunctionDeclaration or nested instanceof UCODE::ArrowFunction)) and violation = "nested-function" or
   not call.getParent*() = handler.getBody() and violation = "call-outside-body")
select call.getLocation().getFile().getRelativePath() as path, call as call_node, handler as handler_node, violation
