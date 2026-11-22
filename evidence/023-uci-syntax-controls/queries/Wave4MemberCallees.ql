/**
 * @name Wave 4 member callee syntax
 * @description Test-only inventory of member-shaped callees at predeclared source sites; no receiver or target resolution.
 * @kind table
 * @id ucode/wave4/member-callees
 * @tags testing
 */

import codeql.files.FileSystem
import codeql.ucode.ast.internal.TreeSitter

from
  UCODE::CallExpression call,
  UCODE::MemberExpression callee,
  UCODE::Expression receiver,
  UCODE::PropertyIdentifier property
where
  (
    call.getLocation().getFile().getBaseName() = "uci.uc" and
    (call.getLocation().getStartLine() = 28 or call.getLocation().getStartLine() = 59)
    or call.getLocation().getFile().getBaseName() = "session-set.uc" and call.getLocation().getStartLine() = 2
    or call.getLocation().getFile().getBaseName() = "unknown-direct-call.uc" and call.getLocation().getStartLine() = 2
  ) and
  callee = call.getFunction() and
  receiver = callee.getObject() and
  property = callee.getProperty()
select
  call,
  callee,
  receiver,
  property,
  receiver.(UCODE::Identifier).getValue() as receiver_identifier,
  property.getValue() as property_name,
  call.getLocation().getFile().getRelativePath() as source_path,
  call.getLocation().getStartLine() as call_line,
  call.getLocation().getStartColumn() as call_column
