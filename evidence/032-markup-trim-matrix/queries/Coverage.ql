import codeql.ucode.Markup
import codeql.ucode.MarkupCFG

string coverage(UcodeMarkup::Markup root) {
  MarkupCFG::isCovered(root) and result = "covered"
  or not MarkupCFG::isCovered(root) and result = "unsupported"
}

from UcodeMarkup::Markup root
where root.getLocation().getFile().getBaseName() in ["plain.ut", "trim-open.ut", "trim-close.ut", "trim-both.ut", "trim-member.ut", "ordinary-member.ut"]
select root.getLocation().getFile().getBaseName(), root.getLocation().getStartLine(),
  root.getLocation().getStartColumn(), root.getLocation().getEndLine(),
  root.getLocation().getEndColumn(), coverage(root)
