/**
 * @name Wave 4 property read without call control
 * @description Test-only inventory of the eligible property-read near miss; no dispatch or binding claim.
 * @kind table
 * @id ucode/wave4/property-read-control
 * @tags testing
 */

import codeql.files.FileSystem
import codeql.ucode.ast.internal.TreeSitter

from
  UCODE::MemberExpression member,
  UCODE::Expression receiver,
  UCODE::PropertyIdentifier property,
  UCODE::AstNode parent
where
  member.getLocation().getFile().getBaseName() = "property-read.uc" and
  member.getLocation().getStartLine() = 2 and
  receiver = member.getObject() and
  property = member.getProperty() and
  property.getValue() = "ubus_call" and
  parent = member.getParent() and
  not exists(UCODE::CallExpression call | call.getFunction() = member)
select
  member,
  receiver,
  property,
  parent,
  member.getLocation().getFile().getRelativePath() as source_path,
  member.getLocation().getStartLine() as member_line,
  member.getLocation().getStartColumn() as member_column,
  member.getLocation().getEndLine() as member_end_line,
  member.getLocation().getEndColumn() as member_end_column,
  receiver.getAPrimaryQlClass() as receiver_kind,
  property.getValue() as property_name
