/** Selected syntax call sites in markup and plain ucode; no target resolution. */
import codeql.ucode.Markup

predicate site(string tree, string path, string kind, string name, int sl, int sc, int el, int ec) {
  exists(UcodeMarkup::CallExpression c |
    tree = "markup" and path = c.getLocation().getFile().getRelativePath() and
    kind = c.getFunction().getAPrimaryQlClass() and
    (c.getFunction() instanceof UcodeMarkup::Identifier and name = c.getFunction().toString() or
     not c.getFunction() instanceof UcodeMarkup::Identifier and name = "<non-identifier>") and
    sl = c.getLocation().getStartLine() and sc = c.getLocation().getStartColumn() and
    el = c.getLocation().getEndLine() and ec = c.getLocation().getEndColumn()
  ) or
  exists(UCODE::CallExpression c |
    tree = "plain" and path = c.getLocation().getFile().getRelativePath() and
    kind = c.getFunction().getAPrimaryQlClass() and
    (c.getFunction() instanceof UCODE::Identifier and name = c.getFunction().toString() or
     not c.getFunction() instanceof UCODE::Identifier and name = "<non-identifier>") and
    sl = c.getLocation().getStartLine() and sc = c.getLocation().getStartColumn() and
    el = c.getLocation().getEndLine() and ec = c.getLocation().getEndColumn()
  )
}
from string tree, string path, string kind, string name, int sl, int sc, int el, int ec
where site(tree, path, kind, name, sl, sc, el, ec)
select tree, path, kind, name, sl, sc, el, ec
