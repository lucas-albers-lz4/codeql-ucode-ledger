/**
 * @name Mixed LuCI profile AST root counts
 * @description Counts distinct syntax root entities by file and parse mode.
 * @kind table
 * @id ucode/ledger/mixed-profile-root-counts
 */
import codeql.files.FileSystem
import codeql.ucode.Markup

from File file, string path, int programRoots, int markupRoots
where
  path = file.getRelativePath() and
  path != "" and
  programRoots = count(UCODE::Program root | root.getLocation().getFile() = file) and
  markupRoots = count(UcodeMarkup::Markup root | root.getLocation().getFile() = file)
select path, programRoots, markupRoots
