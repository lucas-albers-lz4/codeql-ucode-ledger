/**
 * @name Markup uninitialized declaration value control
 * @description Asserts that the selected no-init.ut declarator has no value relation.
 * @kind table
 * @id ucode/prep/markup-declaration-value-negative
 */

import codeql.ucode.Markup

from UcodeMarkup::VariableDeclarator d
where
  d.getLocation().getFile().getBaseName() = "no-init.ut" and
  d.getLocation().getStartLine() = 1 and
  d.getLocation().getStartColumn() = 8 and
  not exists(d.getValue())
select d, d.getLocation().getStartLine(), d.getLocation().getStartColumn(),
  d.getLocation().getEndLine(), d.getLocation().getEndColumn(), d.getParentIndex()
