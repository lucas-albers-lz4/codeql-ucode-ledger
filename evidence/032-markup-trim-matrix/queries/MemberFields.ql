import codeql.ucode.Markup

from UcodeMarkup::MemberExpression member
where member.getLocation().getFile().getBaseName() in ["trim-member.ut", "ordinary-member.ut"] and
  not exists(member.getOptionalChain())
select member.getLocation().getFile().getBaseName(),
  member.getObject().getAPrimaryQlClass(), member.getObject().getLocation().getStartColumn(), member.getObject().getLocation().getEndColumn(), member.getObject().(UcodeMarkup::Identifier).getValue(),
  member.getObject().getParentIndex(),
  member.getProperty().getAPrimaryQlClass(), member.getProperty().getLocation().getStartColumn(), member.getProperty().getLocation().getEndColumn(), member.getProperty().(UcodeMarkup::PropertyIdentifier).getValue(),
  member.getProperty().getParentIndex(), "optional-chain-absent"
