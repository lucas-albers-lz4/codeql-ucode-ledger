import codeql.ucode.Markup
string parentKind(UcodeMarkup::AstNode n) { result = n.getParent().getAPrimaryQlClass() or not exists(n.getParent()) and result = "<root>" }
int parentIndex(UcodeMarkup::AstNode n) { result = n.getParentIndex() or not exists(n.getParent()) and result = -1 }
from UcodeMarkup::AstNode n
where n.getLocation().getFile().getBaseName() = ["siblings.ut", "siblings-all-covered.ut"] and
 n.getAPrimaryQlClass() = ["Markup", "FunctionExpression", "VariableDeclarator", "Number", "LexicalDeclaration", "CallExpression", "ExpressionStatement"]
select n.getLocation().getFile().getBaseName(), n.getAPrimaryQlClass(), n.getLocation().getStartLine(), n.getLocation().getStartColumn(), n.getLocation().getEndLine(), n.getLocation().getEndColumn(), parentKind(n), parentIndex(n),
 count(UcodeMarkup::AstNode x | x.getLocation() = n.getLocation() and x.getAPrimaryQlClass() = n.getAPrimaryQlClass() and parentKind(x) = parentKind(n) and parentIndex(x) = parentIndex(n) | x)
