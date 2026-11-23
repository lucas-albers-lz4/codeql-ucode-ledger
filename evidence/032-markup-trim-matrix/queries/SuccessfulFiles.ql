import codeql.files.FileSystem
import codeql.ucode.Diagnostics

from File f
where f.getBaseName() in ["plain.ut", "trim-open.ut", "trim-close.ut", "trim-both.ut", "trim-member.ut", "ordinary-member.ut"] and
  not exists(ExtractionError e | e.getLocation().getFile() = f) and exists(f.getRelativePath())
select f, f.getRelativePath()
