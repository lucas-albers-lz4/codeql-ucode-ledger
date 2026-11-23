import codeql.ucode.MarkupCFG

string identity(MarkupCFG::Node n) {
  result = n.getRole() and n.getRole() = ["entry", "exit"]
  or exists(UcodeMarkup::AstNode a | a = n.getAstNode() |
    result = a.getAPrimaryQlClass() + ":" + a.getLocation().getStartLine().toString() + ":" +
      a.getLocation().getStartColumn().toString() + ":" + a.getLocation().getEndLine().toString() + ":" +
      a.getLocation().getEndColumn().toString() + ":" + a.getParent().getAPrimaryQlClass() + ":" +
      a.getParentIndex().toString())
}

int edgePairCount(MarkupCFG::Node a, MarkupCFG::Node b) {
  result = count(MarkupCFG::Node x, MarkupCFG::Node y |
    MarkupCFG::edge(x, y) and x.getScope() = a.getScope() and y.getScope() = b.getScope() and
    identity(x) = identity(a) and identity(y) = identity(b)
  )
}

from MarkupCFG::Node a, MarkupCFG::Node b
where MarkupCFG::edge(a, b) and
  a.getScope().getLocation().getFile().getBaseName() = ["normal.ut", "trim-open.ut"]
select a.getScope().getLocation().getFile().getBaseName(), identity(a), identity(b),
  edgePairCount(a, b)
