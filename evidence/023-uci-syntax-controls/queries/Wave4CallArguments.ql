/**
 * @name Wave 4 selected call argument entities
 * @description Test-only inventory of predeclared call-site semantic argument positions; entity columns preserve AST multiplicity.
 * @kind table
 * @id ucode/wave4/call-arguments
 * @tags testing
 */

import codeql.files.FileSystem
import codeql.ucode.ast.internal.TreeSitter

from UCODE::CallExpression call, int index, UCODE::AstNode argument
where
  (
    call.getLocation().getFile().getBaseName() = "uci.uc" and
    (call.getLocation().getStartLine() = 28 or call.getLocation().getStartLine() = 59 or
     call.getLocation().getStartLine() = 76 or call.getLocation().getStartLine() = 79 or
     call.getLocation().getStartLine() = 144 or call.getLocation().getStartLine() = 145)
    or call.getLocation().getFile().getBaseName() = "changes.uc" and call.getLocation().getStartLine() = 2
    or call.getLocation().getFile().getBaseName() = "session-set.uc" and call.getLocation().getStartLine() = 2
    or call.getLocation().getFile().getBaseName() = "unrelated-same-name-helper.uc" and call.getLocation().getStartLine() = 6
    or call.getLocation().getFile().getBaseName() = "unknown-direct-call.uc" and call.getLocation().getStartLine() = 2
    or call.getLocation().getFile().getBaseName() = "swapped-argument-order.uc" and call.getLocation().getStartLine() = 2
  ) and
  (index = 0 or index = 1 or index = 2) and
  argument = call.getArguments().getChild(index) and
  not exists(call.getArguments().getChild(3))
select
  call,
  index,
  argument,
  call.getLocation().getFile().getRelativePath() as source_path,
  call.getLocation().getStartLine() as call_line,
  call.getLocation().getStartColumn() as call_column,
  argument.getAPrimaryQlClass() as argument_kind,
  argument.getLocation().getStartLine() as argument_line,
  argument.getLocation().getStartColumn() as argument_column,
  argument.getLocation().getEndLine() as argument_end_line,
  argument.getLocation().getEndColumn() as argument_end_column
