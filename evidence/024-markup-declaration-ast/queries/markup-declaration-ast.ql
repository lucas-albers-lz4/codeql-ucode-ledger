/**
 * @name Markup declaration AST prequery
 * @description Source-identity inventory for one initialized declaration and a valid let-without-initializer control.
 * @kind table
 * @id ucode/prep/markup-declaration-ast
 */

import codeql.ucode.Markup

string parentKind(UcodeMarkup::AstNode n) {
  result = n.getParent().getAPrimaryQlClass() or
  not exists(n.getParent()) and result = "<root>"
}

from UcodeMarkup::AstNode n
where
  (n.getLocation().getFile().getBaseName() = "mixed.ut" or
   n.getLocation().getFile().getBaseName() = "no-init.ut") and
  (n instanceof UcodeMarkup::LexicalDeclaration or
   n instanceof UcodeMarkup::VariableDeclarator or
   n instanceof UcodeMarkup::Number)
select n, n.getLocation().getFile().getBaseName(), n.getAPrimaryQlClass(),
  n.getLocation().getStartLine(), n.getLocation().getStartColumn(),
  n.getLocation().getEndLine(), n.getLocation().getEndColumn(),
  parentKind(n), n.getParentIndex()
