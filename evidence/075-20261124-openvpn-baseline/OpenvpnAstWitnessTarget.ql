/**
 * @name OpenVPN historical source/sink AST witness
 * @description Local read-only witness for the predeclared cl_meta and popen sites.
 * @kind table
 */
import codeql.ucode.m3.Models
from UCODE::MemberExpression src, NamedCall sink
where
  src.getProperty().getValue() = "cl_meta" and
  sink.getName() = "popen" and
  sink.getLocation().getStartLine() = 77 and
  src.getLocation().getFile() = sink.getLocation().getFile()
select src, src.getAPrimaryQlClass(), src.getLocation().getStartLine(), src.getLocation().getStartColumn(), src.getLocation().getEndLine(), src.getLocation().getEndColumn(), sink, sink.getAPrimaryQlClass(), sink.getLocation().getStartLine(), sink.getLocation().getStartColumn(), sink.getLocation().getEndLine(), sink.getLocation().getEndColumn()
