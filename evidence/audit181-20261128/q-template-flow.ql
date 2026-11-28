/**
#181 pass-2 corpus-wide: confirm template_string has no dataflow value node anywhere
in the extracted slice (generalizes TemplateNoValueFlow.ql's two-file scope).
*/
import codeql.files.FileSystem
import codeql.ucode.AST
import codeql.ucode.DataFlow
private import codeql.ucode.ast.internal.AstNodes
private import codeql.ucode.ast.internal.TreeSitter

private int totalTemplates() { result = count(TemplateString t | exists(t.getLocation()) | t) }

private int subExpressions() {
  result = count(TemplateSubstitution sub, TemplateSubstitutionExpression e |
      e = sub.getExpression() | e)
}

private int templatesWithCfgNode() {
  result = count(TemplateString t, DataFlow::ExprNode n |
      toTreeSitter(n.getExprNode().getAstNode()) = toTreeSitter(t) | t)
}

private int substitutionExprsWithCfgNode() {
  result = count(TemplateSubstitutionExpression e, DataFlow::ExprNode n |
      toTreeSitter(n.getExprNode().getAstNode()) = e.getRawAstNode() | e)
}

from string label, int n
where
  label = "template_strings_total" and n = totalTemplates()
  or
  label = "substitution_expressions_total" and n = subExpressions()
  or
  label = "template_strings_with_cfg_node" and n = templatesWithCfgNode()
  or
  label = "substitution_exprs_with_cfg_node" and n = substitutionExprsWithCfgNode()
select label, n
