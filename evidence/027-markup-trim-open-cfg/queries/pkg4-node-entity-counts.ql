import codeql.ucode.MarkupCFG

string identity(MarkupCFG::Node n) {
  result = n.getRole() and n.getRole() = ["entry", "exit"]
  or exists(UcodeMarkup::AstNode a | a = n.getAstNode() |
    result = a.getAPrimaryQlClass() + ":" + a.getLocation().getStartLine().toString() + ":" +
      a.getLocation().getStartColumn().toString() + ":" + a.getLocation().getEndLine().toString() + ":" +
      a.getLocation().getEndColumn().toString() + ":" + a.getParent().getAPrimaryQlClass() + ":" +
      a.getParentIndex().toString())
}

int identityEntityCount(MarkupCFG::Node n) {
  result = count(MarkupCFG::Node other |
    other.getScope() = n.getScope() and other.getRole() = n.getRole() and
    identity(other) = identity(n)
  )
}

from MarkupCFG::Node n
where n.getScope().getLocation().getFile().getBaseName() = ["normal.ut", "trim-open.ut"]
select n.getScope().getLocation().getFile().getBaseName(), n.getRole(), identity(n),
  identityEntityCount(n)
