/**
 * @name Quoted switch substitution AST identities
 * @description Testing-only witness for distinct shellquote(request.args.switch)
 *              substitutions passed directly to imported fs.popen.
 * @kind table
 * @id ucode/testing/quoted-switch-ast-identities
 */

import codeql.ucode.m3.Models

from RequestArgsAccess src, NamedCall sq,
     UCODE::TemplateSubstitution sub, UCODE::TemplateString tmpl,
     NamedFsPopenCall sink
where
  src.getProperty().getValue() = "switch" and
  sq.getName() = "shellquote" and
  src = sq.getArgument(0) and
  sq = sub.getChild() and
  sub.getParent() = tmpl and
  tmpl = sink.getArgument(0) and
  src.getLocation().getFile().getRelativePath() in
    ["usr/share/rpcd/ucode/luci", "usr/share/rpcd/ucode/controls.uc"]
select src, sq, sub, tmpl, sink,
  src.getLocation().getFile().getRelativePath(),
  src.getLocation().getStartLine(), src.getLocation().getStartColumn(),
  src.getLocation().getEndLine(), src.getLocation().getEndColumn(),
  sub.getLocation().getStartColumn(), tmpl.getLocation().getStartColumn(),
  sink.getLocation().getStartColumn()
