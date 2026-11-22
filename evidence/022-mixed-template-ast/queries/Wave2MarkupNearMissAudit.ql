/** Broad control audit: any expression tag or call node in the literal-lookalike .ut. */
import codeql.ucode.Markup

string parentKind(UcodeMarkup::AstNode n) {
  result = n.getParent().getAPrimaryQlClass() or
  not exists(n.getParent()) and result = "<root>"
}

int parentIndex(UcodeMarkup::AstNode n) {
  result = n.getParentIndex() or not exists(n.getParent()) and result = -1
}

from UcodeMarkup::AstNode n
where
  n.getLocation().getFile().getRelativePath() =
    "usr/share/ucode/controls/literal-near-miss.ut" and
  (n instanceof UcodeMarkup::ExpressionTag or n instanceof UcodeMarkup::CallExpression)
select n, n.getAPrimaryQlClass(), n.getLocation().getStartLine(),
  n.getLocation().getStartColumn(), n.getLocation().getEndLine(),
  n.getLocation().getEndColumn(), parentKind(n), parentIndex(n)
