/**
 * @name Markup initialized declaration value identity
 * @description Asserts that the selected mixed.ut declarator's value relation resolves to a Number AST entity.
 * @kind table
 * @id ucode/prep/markup-declaration-value-positive
 */

import codeql.ucode.Markup

from UcodeMarkup::VariableDeclarator d, UcodeMarkup::Number n
where
  d.getLocation().getFile().getBaseName() = "mixed.ut" and
  d.getLocation().getStartLine() = 2 and
  d.getLocation().getStartColumn() = 8 and
  d.getLocation().getEndColumn() = 12 and
  d.getValue() = n
select d, n, d.getLocation().getStartLine(), d.getLocation().getStartColumn(),
  d.getLocation().getEndColumn(), n.getLocation().getStartLine(),
  n.getLocation().getStartColumn(), n.getLocation().getEndColumn(), n.getValue()
