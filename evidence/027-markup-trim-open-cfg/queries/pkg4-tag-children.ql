import codeql.ucode.Markup

from UcodeMarkup::ExpressionTag tag
where tag.getLocation().getFile().getBaseName() = ["normal.ut", "trim-open.ut"]
select tag.getLocation().getFile().getBaseName(), tag.getLocation().getStartLine(),
  tag.getLocation().getStartColumn(), tag.getLocation().getEndLine(), tag.getLocation().getEndColumn(),
  tag.getOpen().getAPrimaryQlClass(), tag.getOpen().getLocation().getStartColumn(),
  tag.getOpen().getLocation().getEndColumn(), tag.getChild().getAPrimaryQlClass(),
  tag.getChild().toString(), tag.getChild().getLocation().getStartColumn(),
  tag.getChild().getLocation().getEndColumn(), tag.getClose().getAPrimaryQlClass(),
  tag.getClose().getLocation().getStartColumn(), tag.getClose().getLocation().getEndColumn()
