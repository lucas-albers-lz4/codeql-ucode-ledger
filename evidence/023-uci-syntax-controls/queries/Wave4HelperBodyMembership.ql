/**
 * @name Wave 4 helper body membership witnesses
 * @description Test-only AST containment observations for the named helper body; never joins an external caller by spelling.
 * @kind table
 * @id ucode/wave4/helper-body-membership
 * @tags testing
 */

import codeql.files.FileSystem
import codeql.ucode.ast.internal.TreeSitter

from UCODE::FunctionDeclaration declaration, UCODE::CallExpression bodyCall, UCODE::Identifier name
where
  name = declaration.getName() and
  name.getValue() = "ubus_call" and
  bodyCall.getParent+() = declaration.getBody() and
  (
    declaration.getLocation().getFile().getBaseName() = "uci.uc" and
    bodyCall.getLocation().getStartLine() = 28
    or declaration.getLocation().getFile().getBaseName() = "unrelated-same-name-helper.uc" and
    bodyCall.getLocation().getStartLine() = 2
  )
select declaration, bodyCall, name
