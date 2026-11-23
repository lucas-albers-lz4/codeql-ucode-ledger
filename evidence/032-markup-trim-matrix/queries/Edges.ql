import codeql.ucode.MarkupCFG

string identity(MarkupCFG::Node n) {
  result = n.getRole() and n.getRole() in ["entry", "exit"]
  or exists(UcodeMarkup::AstNode a | a = n.getAstNode() |
    result = a.getAPrimaryQlClass() + ":" + a.getLocation().getStartLine().toString() + ":" +
      a.getLocation().getStartColumn().toString() + ":" + a.getLocation().getEndLine().toString() + ":" +
      a.getLocation().getEndColumn().toString() + ":" + a.getParent().getAPrimaryQlClass() + ":" +
      a.getParentIndex().toString())
}

from MarkupCFG::Node a, MarkupCFG::Node b
where MarkupCFG::edge(a, b) and a.getScope().getLocation().getFile().getBaseName() in ["plain.ut", "trim-open.ut", "trim-close.ut", "trim-both.ut", "trim-member.ut", "ordinary-member.ut"]
select a.getScope().getLocation().getFile().getBaseName(), identity(a), identity(b),
  count(MarkupCFG::Node c, MarkupCFG::Node d |
    MarkupCFG::edge(c, d) and c.getScope() = a.getScope() and d.getScope() = b.getScope() and
    identity(c) = identity(a) and identity(d) = identity(b))
