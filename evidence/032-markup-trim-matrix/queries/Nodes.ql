import codeql.ucode.MarkupCFG

string identity(MarkupCFG::Node n) {
  result = n.getRole() and n.getRole() in ["entry", "exit"]
  or exists(UcodeMarkup::AstNode a | a = n.getAstNode() |
    result = a.getAPrimaryQlClass() + ":" + a.getLocation().getStartLine().toString() + ":" +
      a.getLocation().getStartColumn().toString() + ":" + a.getLocation().getEndLine().toString() + ":" +
      a.getLocation().getEndColumn().toString() + ":" + a.getParent().getAPrimaryQlClass() + ":" +
      a.getParentIndex().toString())
}

from MarkupCFG::Node n
where n.getScope().getLocation().getFile().getBaseName() in ["plain.ut", "trim-open.ut", "trim-close.ut", "trim-both.ut", "trim-member.ut", "ordinary-member.ut"]
select n.getScope().getLocation().getFile().getBaseName(), n.getRole(), identity(n),
  count(MarkupCFG::Node duplicate |
    duplicate.getScope() = n.getScope() and duplicate.getRole() = n.getRole() and identity(duplicate) = identity(n))
