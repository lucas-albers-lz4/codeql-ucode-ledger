import codeql.ucode.Diagnostics
from Diagnostic d
where d.getLocation().getFile().getBaseName() = ["normal.ut", "trim-open.ut"]
select d.getLocation().getFile().getBaseName(), d.getTag(), d.getMessage()
