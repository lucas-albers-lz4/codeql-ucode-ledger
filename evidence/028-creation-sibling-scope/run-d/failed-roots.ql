import codeql.ucode.MarkupCFG
import codeql.ucode.MarkupCreationCFG
string foundation(UcodeMarkup::Markup r) { MarkupCFG::isCovered(r) and result = "covered" or not MarkupCFG::isCovered(r) and result = "unsupported" }
string creation(UcodeMarkup::Markup r) { MarkupCreationCFG::hasTopLevelObservation(r) and result = "top-observed" or not MarkupCreationCFG::hasTopLevelObservation(r) and result = "unsupported" }
from string file, int sl, int sc, int el, int ec, string f, string c, int entities
where file = ["siblings.ut", "siblings-all-covered.ut"] and
  entities = count(UcodeMarkup::Markup r | r.getLocation().getFile().getBaseName() = file and
    r.getLocation().getStartLine() = sl and r.getLocation().getStartColumn() = sc and
    r.getLocation().getEndLine() = el and r.getLocation().getEndColumn() = ec and foundation(r) = f and creation(r) = c | r) and entities > 0
select file, sl, sc, el, ec, f, c, entities
