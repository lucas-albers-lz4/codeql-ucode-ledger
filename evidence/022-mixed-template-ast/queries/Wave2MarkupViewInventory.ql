/** Proposed broad Wave 2 inventory. Preserve entities and report all tags/calls. */
import codeql.ucode.Markup

string parentKind(UcodeMarkup::AstNode n) {
  result = n.getParent().getAPrimaryQlClass() or
  not exists(n.getParent()) and result = "<root>"
}

int parentIndex(UcodeMarkup::AstNode n) {
  result = n.getParentIndex() or not exists(n.getParent()) and result = -1
}

int parentStartLine(UcodeMarkup::AstNode n) {
  result = n.getParent().getLocation().getStartLine() or
  not exists(n.getParent()) and result = -1
}

int parentStartColumn(UcodeMarkup::AstNode n) {
  result = n.getParent().getLocation().getStartColumn() or
  not exists(n.getParent()) and result = -1
}

int parentEndLine(UcodeMarkup::AstNode n) {
  result = n.getParent().getLocation().getEndLine() or
  not exists(n.getParent()) and result = -1
}

int parentEndColumn(UcodeMarkup::AstNode n) {
  result = n.getParent().getLocation().getEndColumn() or
  not exists(n.getParent()) and result = -1
}

predicate selected(UcodeMarkup::AstNode n) {
  n instanceof UcodeMarkup::ExpressionTag or
  n instanceof UcodeMarkup::CallExpression or
  n instanceof UcodeMarkup::RawText or
  n instanceof UcodeMarkup::Identifier and n.toString() = "view" and
    exists(UcodeMarkup::ExpressionTag e | e.getChild() = n) or
  n instanceof UcodeMarkup::String
}

from UcodeMarkup::AstNode n
where
  selected(n) and
  n.getLocation().getFile().getRelativePath() in [
    "usr/share/ucode/luci/template/view.ut",
    "usr/share/ucode/controls/literal-near-miss.ut"
  ]
select n, n.getLocation().getFile().getRelativePath(), n.getAPrimaryQlClass(), n.toString(),
  n.getLocation().getStartLine(), n.getLocation().getStartColumn(),
  n.getLocation().getEndLine(), n.getLocation().getEndColumn(),
  parentKind(n), parentStartLine(n), parentStartColumn(n), parentEndLine(n),
  parentEndColumn(n), parentIndex(n)
