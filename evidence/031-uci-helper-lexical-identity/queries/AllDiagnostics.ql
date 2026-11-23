/** Enumerate all UCODE Diagnostics entities in the finalized database. */
import codeql.ucode.Diagnostics

int severity() { result = 2 }

from Diagnostic d
where exists(d.getLocation().getFile().getRelativePath())
select d, d.getSeverityText() + " [" + d.getTag() + "]: " + d.getFullMessage(), severity()
