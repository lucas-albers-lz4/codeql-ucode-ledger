/**
 * @name Function binding regression matrix
 * @description Testing-only matrix of print-argument reads and lexical declarations.
 * @kind table
 * @tags testing
 * @id ucode/testing/function-binding-matrix
 */
import codeql.ucode.AST
import codeql.ucode.ast.internal.AstNodes
import codeql.ucode.m3.Models
from VariableReadAccess read, UCODE::Identifier use, NamedCall call, string basename
where
  read.getAstNode() = TIdentifier(use) and
  call.getArgument(0) = use and
  call.getName() = "print" and
  basename = use.getLocation().getFile().getBaseName() and
  basename.matches("matrix_%")
select basename, use.getLocation().getStartLine(), read.getVariable().getLocation().getStartLine(),
  read.getVariable().getAstNode().getAPrimaryQlClass(), read.getName()
