/**
 * @name WOL callback declaration binding audit
 * @description Testing-only resolved function declaration references in selected WOL controls.
 * @kind table
 * @tags testing
 * @id ucode/testing/wol-callback-binding-audit
 */
import codeql.ucode.AST
import codeql.ucode.ast.internal.AstNodes
import codeql.ucode.m3.Models
from NamedCall mapCall, UCODE::Identifier use, UCODE::FunctionDeclaration decl,
  VariableReadAccess read, string basename
where
  mapCall.getName() = "map" and
  mapCall.getArgument(1) = use and
  read.getAstNode() = TIdentifier(use) and
  read.getVariable().getAstNode() = TFunctionDeclaration(decl) and
  basename = use.getLocation().getFile().getBaseName() and
  basename in ["identity.uc", "identity_fixed_guard.uc", "luci.wol", "callback_shadow.uc", "callback_write.uc"]
select use, decl, basename,
  count(VariableWriteAccess write | write.getVariable().getAstNode() = TFunctionDeclaration(decl))
