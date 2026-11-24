/**
 * @name Tailscale control source/sink AST witness
 * @description Local read-only witness for predeclared control sites.
 * @kind table
 */
import codeql.ucode.m3.Models
from UCODE::MemberExpression src, NamedCall sink
where
  src.getLocation().getFile() = sink.getLocation().getFile() and
  (src.getProperty().getValue() = "cmd" or src.getProperty().getValue() = "form_data" or src.getProperty().getValue() = "loginserver") and
  sink.getName() = "popen"
select src, src.getLocation().getFile().getBaseName(), src.getProperty().getValue(), src.getLocation().getStartLine(), src.getLocation().getStartColumn(), src.getLocation().getEndColumn(), sink, sink.getLocation().getStartLine(), sink.getLocation().getStartColumn(), sink.getLocation().getEndColumn()
