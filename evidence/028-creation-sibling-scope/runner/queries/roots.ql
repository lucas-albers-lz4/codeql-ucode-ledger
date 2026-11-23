import codeql.ucode.MarkupCFG
import codeql.ucode.MarkupCreationCFG
string foundation(UcodeMarkup::Markup r) { MarkupCFG::isCovered(r) and result = "covered" or not MarkupCFG::isCovered(r) and result = "unsupported" }
string creation(UcodeMarkup::Markup r) { MarkupCreationCFG::hasTopLevelObservation(r) and result = "top-observed" or not MarkupCreationCFG::hasTopLevelObservation(r) and result = "unsupported" }
from UcodeMarkup::Markup r
where r.getLocation().getFile().getBaseName() = ["siblings.ut", "siblings-all-covered.ut"]
select r.getLocation().getFile().getBaseName(), r.getLocation().getStartLine(), r.getLocation().getStartColumn(), r.getLocation().getEndLine(), r.getLocation().getEndColumn(), foundation(r), creation(r),
 count(UcodeMarkup::Markup x | x.getLocation() = r.getLocation() and foundation(x) = foundation(r) and creation(x) = creation(r) | x)
