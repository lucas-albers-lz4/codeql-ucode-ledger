import codeql.ucode.Diagnostics

from Diagnostic d
where d.getLocation().getFile().getBaseName() in ["plain.ut", "trim-open.ut", "trim-close.ut", "trim-both.ut", "trim-member.ut", "ordinary-member.ut"]
select d.getLocation().getFile().getBaseName(), d.getTag(), d.getMessage(),
  d.getLocation().getStartLine(), d.getLocation().getStartColumn(), d.getLocation().getEndLine(), d.getLocation().getEndColumn()
