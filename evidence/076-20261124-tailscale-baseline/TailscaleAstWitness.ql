/**
 * @name Tailscale historical source/sink AST witness
 * @description Local read-only witness for predeclared source properties and line-164 popen site.
 * @kind table
 */
import codeql.ucode.m3.Models
from UCODE::MemberExpression src, NamedCall sink
where
  src.getLocation().getFile() = sink.getLocation().getFile() and
  (src.getProperty().getValue() = "form_data" or src.getProperty().getValue() = "loginserver" or src.getProperty().getValue() = "loginserver_authkey") and
  (src.getLocation().getStartLine() = 140 or src.getLocation().getStartLine() = 152 or src.getLocation().getStartLine() = 153) and
  sink.getName() = "popen" and sink.getLocation().getStartLine() = 164
select src, src.getProperty().getValue(), src.getLocation().getStartLine(), src.getLocation().getStartColumn(), src.getLocation().getEndLine(), src.getLocation().getEndColumn(), sink, sink.getLocation().getStartLine(), sink.getLocation().getStartColumn(), sink.getLocation().getEndLine(), sink.getLocation().getEndColumn()
