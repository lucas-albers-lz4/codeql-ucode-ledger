/** @name Issue 155 raw string fragment values
 * @description Scratch-only control witnesses, with exact entity IDs.
 * @kind table
 * @id scratch/issue-155-string-values
 */
import codeql.files.FileSystem
import codeql.ucode.ast.internal.TreeSitter
from UCODE::StringFragment fragment
where fragment.getLocation().getFile().getRelativePath() = ["controls/positive-direct.uc", "controls/negative-duplicate.uc"]
select fragment.getLocation().getFile().getRelativePath() as path, fragment as fragment_node, fragment.getValue() as value
