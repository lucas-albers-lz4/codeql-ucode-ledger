/**
 * @name Wave 4 identifier callee syntax
 * @description Test-only inventory of identifier-shaped callees at predeclared source sites; no binding resolution.
 * @kind table
 * @id ucode/wave4/identifier-callees
 * @tags testing
 */

import codeql.files.FileSystem
import codeql.ucode.ast.internal.TreeSitter

from UCODE::CallExpression call, UCODE::Identifier callee
where
  (
    call.getLocation().getFile().getBaseName() = "uci.uc" and
    (call.getLocation().getStartLine() = 76 or call.getLocation().getStartLine() = 79 or
     call.getLocation().getStartLine() = 144 or call.getLocation().getStartLine() = 145)
    or call.getLocation().getFile().getBaseName() = "changes.uc" and call.getLocation().getStartLine() = 2
    or call.getLocation().getFile().getBaseName() = "unrelated-same-name-helper.uc" and call.getLocation().getStartLine() = 6
    or call.getLocation().getFile().getBaseName() = "swapped-argument-order.uc" and call.getLocation().getStartLine() = 2
  ) and
  callee = call.getFunction()
select
  call,
  callee,
  callee.getValue() as identifier_callee,
  call.getLocation().getFile().getRelativePath() as source_path,
  call.getLocation().getStartLine() as call_line,
  call.getLocation().getStartColumn() as call_column
