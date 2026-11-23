import codeql.ucode.Markup

string parentKind(UcodeMarkup::AstNode n) {
  result = n.getParent().getAPrimaryQlClass()
  or not exists(n.getParent()) and result = "<root>"
}

int parentIndex(UcodeMarkup::AstNode n) {
  result = n.getParentIndex()
  or not exists(n.getParent()) and result = -1
}

int tupleEntityCount(UcodeMarkup::AstNode n) {
  result = count(UcodeMarkup::AstNode other |
    other.getLocation().getFile() = n.getLocation().getFile() and
    other.getAPrimaryQlClass() = n.getAPrimaryQlClass() and
    other.toString() = n.toString() and
    other.getLocation().getStartLine() = n.getLocation().getStartLine() and
    other.getLocation().getStartColumn() = n.getLocation().getStartColumn() and
    other.getLocation().getEndLine() = n.getLocation().getEndLine() and
    other.getLocation().getEndColumn() = n.getLocation().getEndColumn() and
    parentKind(other) = parentKind(n) and parentIndex(other) = parentIndex(n)
  )
}

from UcodeMarkup::AstNode n
where n.getLocation().getFile().getBaseName() = ["normal.ut", "trim-open.ut"]
select n.getLocation().getFile().getBaseName(), n.getAPrimaryQlClass(), n.toString(),
  n.getLocation().getStartLine(), n.getLocation().getStartColumn(),
  n.getLocation().getEndLine(), n.getLocation().getEndColumn(), parentKind(n),
  parentIndex(n), tupleEntityCount(n)
