/**
 * @name Wave 4 pinned indirect UCI syntax inventory
 * @description Test-only inventory of predeclared call sites and controls. Reports raw AST entities and locations; does not resolve bindings, forwarding flow, UCI effects, or runtime behavior.
 * @kind table
 * @id ucode/wave4/uci-call-syntax
 * @tags testing
 */

import codeql.files.FileSystem
import codeql.ucode.ast.internal.TreeSitter

private string simpleText(UCODE::AstNode node) {
  result = node.(UCODE::Identifier).getValue()
  or
  result = node.(UCODE::String).getChild(0).(UCODE::StringFragment).getValue()
  or
  result = "<non-simple>" and
    not node instanceof UCODE::Identifier and
    not node instanceof UCODE::String
}

from
  UCODE::CallExpression call,
  UCODE::AstNode callee,
  UCODE::AstNode arg0,
  UCODE::AstNode arg1,
  UCODE::AstNode arg2,
  UCODE::AstNode enclosing,
  UCODE::AstNode enclosingParent,
  int arity,
  string calleeKind,
  string calleeName,
  string receiverText,
  string propertyText
where
  (
    call.getLocation().getFile().getBaseName() = "uci.uc" and
    (call.getLocation().getStartLine() = 28 or
     call.getLocation().getStartLine() = 59 or
     call.getLocation().getStartLine() = 76 or
     call.getLocation().getStartLine() = 79 or
     call.getLocation().getStartLine() = 144 or
     call.getLocation().getStartLine() = 145)
    or
    call.getLocation().getFile().getBaseName() = "changes.uc" and call.getLocation().getStartLine() = 2
    or
    call.getLocation().getFile().getBaseName() = "session-set.uc" and call.getLocation().getStartLine() = 2
    or
    call.getLocation().getFile().getBaseName() = "unrelated-same-name-helper.uc" and call.getLocation().getStartLine() = 6
    or
    call.getLocation().getFile().getBaseName() = "unknown-direct-call.uc" and call.getLocation().getStartLine() = 2
    or
    call.getLocation().getFile().getBaseName() = "swapped-argument-order.uc" and call.getLocation().getStartLine() = 2
  ) and
  arity = count(int i | exists(call.getArguments().getChild(i))) and
  arity = 3 and
  callee = call.getFunction() and
  (
    calleeKind = "Identifier" and
    callee instanceof UCODE::Identifier and
    calleeName = callee.(UCODE::Identifier).getValue() and
    receiverText = "" and
    propertyText = ""
    or
    calleeKind = "MemberExpression" and
    callee instanceof UCODE::MemberExpression and
    calleeName = callee.(UCODE::MemberExpression).getProperty().getValue() and
    receiverText = callee.(UCODE::MemberExpression).getObject().(UCODE::Identifier).getValue() and
    propertyText = callee.(UCODE::MemberExpression).getProperty().getValue()
  ) and
  arg0 = call.getArguments().getChild(0) and
  arg1 = call.getArguments().getChild(1) and
  arg2 = call.getArguments().getChild(2) and
  enclosing = call.getParent+() and
  (
    enclosing instanceof UCODE::FunctionDeclaration or
    enclosing instanceof UCODE::FunctionExpression or
    enclosing instanceof UCODE::ArrowFunction
  ) and
  not exists(UCODE::AstNode closer |
    closer = call.getParent+() and
    (closer instanceof UCODE::FunctionDeclaration or
     closer instanceof UCODE::FunctionExpression or
     closer instanceof UCODE::ArrowFunction) and
    closer.getParent+() = enclosing
  ) and
  enclosingParent = enclosing.getParent()
select
  call,
  callee,
  enclosing,
  enclosingParent,
  arg0,
  arg1,
  arg2,
  call.getLocation().getFile().getRelativePath() as source_path,
  call.getLocation().getStartLine() as call_line,
  call.getLocation().getStartColumn() as call_column,
  call.getLocation().getEndLine() as call_end_line,
  call.getLocation().getEndColumn() as call_end_column,
  calleeKind,
  calleeName,
  receiverText,
  propertyText,
  arity,
  simpleText(arg0) as arg0_text,
  arg0.getAPrimaryQlClass() as arg0_kind,
  arg0.getLocation().getStartLine() as arg0_line,
  arg0.getLocation().getStartColumn() as arg0_column,
  arg0.getLocation().getEndLine() as arg0_end_line,
  arg0.getLocation().getEndColumn() as arg0_end_column,
  simpleText(arg1) as arg1_text,
  arg1.getAPrimaryQlClass() as arg1_kind,
  arg1.getLocation().getStartLine() as arg1_line,
  arg1.getLocation().getStartColumn() as arg1_column,
  arg1.getLocation().getEndLine() as arg1_end_line,
  arg1.getLocation().getEndColumn() as arg1_end_column,
  simpleText(arg2) as arg2_text,
  arg2.getAPrimaryQlClass() as arg2_kind,
  arg2.getLocation().getStartLine() as arg2_line,
  arg2.getLocation().getStartColumn() as arg2_column,
  arg2.getLocation().getEndLine() as arg2_end_line,
  arg2.getLocation().getEndColumn() as arg2_end_column,
  enclosing.getAPrimaryQlClass() as enclosing_kind,
  enclosing.getLocation().getStartLine() as enclosing_line,
  enclosing.getLocation().getStartColumn() as enclosing_column,
  enclosing.getLocation().getEndLine() as enclosing_end_line,
  enclosing.getLocation().getEndColumn() as enclosing_end_column
