import codeql.ucode.Markup

string parentKind(UcodeMarkup::AstNode n) {
  result = n.getParent().getAPrimaryQlClass()
  or not exists(n.getParent()) and result = "<root>"
}

int parentIndex(UcodeMarkup::AstNode n) {
  result = n.getParentIndex()
  or not exists(n.getParent()) and result = -1
}

from UcodeMarkup::AstNode n
where n.getLocation().getFile().getBaseName() in ["plain.ut", "trim-open.ut", "trim-close.ut", "trim-both.ut", "trim-member.ut", "ordinary-member.ut"]
select n.getLocation().getFile().getBaseName(), n.getAPrimaryQlClass(), n.toString(),
  n.getLocation().getStartLine(), n.getLocation().getStartColumn(),
  n.getLocation().getEndLine(), n.getLocation().getEndColumn(), parentKind(n), parentIndex(n),
  count(UcodeMarkup::AstNode duplicate |
    duplicate.getLocation().getFile() = n.getLocation().getFile() and
    duplicate.getAPrimaryQlClass() = n.getAPrimaryQlClass() and
    duplicate.getLocation().getStartLine() = n.getLocation().getStartLine() and
    duplicate.getLocation().getStartColumn() = n.getLocation().getStartColumn() and
    duplicate.getLocation().getEndLine() = n.getLocation().getEndLine() and
    duplicate.getLocation().getEndColumn() = n.getLocation().getEndColumn() and
    parentKind(duplicate) = parentKind(n) and parentIndex(duplicate) = parentIndex(n))
