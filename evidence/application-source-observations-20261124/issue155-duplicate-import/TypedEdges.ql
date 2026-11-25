/** @name Issue 155 typed raw AST field edges
 * @description Independent field and list edges for all selected files.
 * @kind table
 * @id scratch/issue-155-v2-typed-edges
 */
import codeql.files.FileSystem
import codeql.ucode.ast.internal.TreeSitter

predicate edge(UCODE::AstNode a, string field, int idx, UCODE::AstNode b) {
  exists(UCODE::CallExpression x | a=x and idx=-1 and
    (field="call-function" and b=x.getFunction() or field="call-arguments" and b=x.getArguments() or field="call-optional" and b=x.getOptionalChain()))
  or exists(UCODE::Arguments x | a=x and b=x.getChild(idx) and field="argument")
  or exists(UCODE::MemberExpression x | a=x and idx=-1 and
    (field="member-object" and b=x.getObject() or field="member-property" and b=x.getProperty() or field="member-optional" and b=x.getOptionalChain()))
  or exists(UCODE::FunctionExpression x | a=x and idx=-1 and (field="function-parameters" and b=x.getParameters() or field="function-body" and b=x.getBody()))
  or exists(UCODE::ReturnStatement x | a=x and idx=-1 and field="return-value" and b=x.getChild())
  or exists(UCODE::FormalParameters x | a=x and field="formal" and b=x.getChild(idx))
  or exists(UCODE::TemplateString x | a=x and field="template-child" and b=x.getChild(idx))
  or exists(UCODE::TemplateSubstitution x | a=x and idx=-1 and field="substitution-child" and b=x.getChild())
  or exists(UCODE::Pair x | a=x and idx=-1 and
    (field="pair-key" and b=x.getKey() or field="pair-value" and b=x.getValue()))
  or exists(UCODE::Object x | a=x and field="object-child" and b=x.getChild(idx))
  or exists(UCODE::String x | a=x and field="string-child" and b=x.getChild(idx))
  or exists(UCODE::ExpressionStatement x | a=x and idx=-1 and field="statement-expression" and b=x.getChild())
  or exists(UCODE::ImportStatement x | a=x and idx=-1 and
    (field="import-clause" and b=x.getClause() or field="import-source" and b=x.getSource()))
  or exists(UCODE::ImportClause x | a=x and idx=-1 and
    (field="import-default" and b=x.getDefault() or field="import-named" and b=x.getNamed() or field="import-namespace" and b=x.getNamespace()))
  or exists(UCODE::NamedImports x | a=x and b=x.getChild(idx) and field="named-import")
  or exists(UCODE::ImportSpecifier x | a=x and idx=-1 and
    (field="import-name" and b=x.getName() or field="import-alias" and b=x.getAlias()))
  or exists(UCODE::VariableDeclarator x | a=x and idx=-1 and
    (field="declarator-name" and b=x.getName() or field="declarator-value" and b=x.getValue()))
  or exists(UCODE::LexicalDeclaration x | a=x and b=x.getChild(idx) and field="lexical-declarator")
  or exists(UCODE::AssignmentExpression x | a=x and idx=-1 and
    (field="assignment-left" and b=x.getLeft() or field="assignment-right" and b=x.getRight()))
  or exists(UCODE::AugmentedAssignmentExpression x | a=x and idx=-1 and
    (field="augmented-left" and b=x.getLeft() or field="augmented-right" and b=x.getRight()))
  or exists(UCODE::FunctionDeclaration x | a=x and idx=-1 and field="function-declaration-name" and b=x.getName())
  or exists(UCODE::FunctionExpression x | a=x and idx=-1 and field="function-expression-name" and b=x.getName())
  or exists(UCODE::RestElement x | a=x and idx=-1 and field="rest-child" and b=x.getChild())
  or exists(UCODE::ArrowFunction x | a=x and idx=-1 and field="arrow-parameter" and b=x.getParameter())
  or exists(UCODE::CatchClause x | a=x and idx=-1 and field="catch-parameter" and b=x.getParameter())
  or exists(UCODE::ForInStatement x | a=x and idx=-1 and (field="for-in-variable" and b=x.getVariable() or field="for-in-key" and b=x.getKey() or field="for-in-value" and b=x.getValue()))
  or exists(UCODE::ForInAltStatement x | a=x and idx=-1 and (field="for-in-alt-variable" and b=x.getVariable() or field="for-in-alt-key" and b=x.getKey() or field="for-in-alt-value" and b=x.getValue()))
  or exists(UCODE::UpdateExpression x | a=x and idx=-1 and field="update-argument" and b=x.getArgument())
}

from UCODE::AstNode a, UCODE::AstNode b, string field, int idx
where
  a.getLocation().getFile().getRelativePath() = ["controls/positive-direct.uc", "controls/negative-duplicate.uc"] and
  edge(a, field, idx, b)
select a.getLocation().getFile().getRelativePath() as path, a as source,
  a.getPrimaryQlClasses() as source_classes, field, idx as field_index, b as target,
  b.getPrimaryQlClasses() as target_classes,
  a.getLocation().getStartLine() as source_start_line, a.getLocation().getStartColumn() as source_start_column,
  b.getLocation().getStartLine() as target_start_line, b.getLocation().getStartColumn() as target_start_column
