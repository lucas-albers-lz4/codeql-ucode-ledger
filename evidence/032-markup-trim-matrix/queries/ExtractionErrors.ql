import codeql.ucode.Diagnostics

from ExtractionError error
where error.getLocation().getFile().getBaseName() in ["plain.ut", "trim-open.ut", "trim-close.ut", "trim-both.ut", "trim-member.ut", "ordinary-member.ut"]
select error.getLocation().getFile().getBaseName(), error.getTag(), error.getMessage(),
  error.getLocation().getStartLine(), error.getLocation().getStartColumn(), error.getLocation().getEndLine(), error.getLocation().getEndColumn()
