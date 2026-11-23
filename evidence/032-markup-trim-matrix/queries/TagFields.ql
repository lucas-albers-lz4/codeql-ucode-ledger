import codeql.ucode.Markup

from UcodeMarkup::ExpressionTag tag
where tag.getLocation().getFile().getBaseName() in ["plain.ut", "trim-open.ut", "trim-close.ut", "trim-both.ut", "trim-member.ut", "ordinary-member.ut"]
select tag.getLocation().getFile().getBaseName(),
  tag.getOpen().getAPrimaryQlClass(), tag.getOpen().getLocation().getStartColumn(), tag.getOpen().getLocation().getEndColumn(),
  tag.getChild().getAPrimaryQlClass(), tag.getChild().getLocation().getStartColumn(), tag.getChild().getLocation().getEndColumn(),
  tag.getClose().getAPrimaryQlClass(), tag.getClose().getLocation().getStartColumn(), tag.getClose().getLocation().getEndColumn()
