/** Wave 1 ledger-local all-diagnostics inventory; not an upstream query. */
import codeql.ucode.Diagnostics
import codeql.files.FileSystem

string diagnosticPath(Diagnostic d) {
  exists(File f | f = d.getLocation().getFile() and result = f.getRelativePath())
  or exists(File f | f = d.getLocation().getFile() and
    not exists(f.getRelativePath()) and result = f.getAbsolutePath())
  or
  not exists(File f | f = d.getLocation().getFile()) and result = "<unattributed>"
}
int diagnosticLine(Diagnostic d) {
  exists(int n | n = d.getLocation().getStartLine() and result = n)
  or not exists(int n | n = d.getLocation().getStartLine()) and result = -1
}
int diagnosticColumn(Diagnostic d) {
  exists(int n | n = d.getLocation().getStartColumn() and result = n)
  or not exists(int n | n = d.getLocation().getStartColumn()) and result = -1
}
string diagnosticSeverityText(Diagnostic d) {
  exists(string s | s = d.getSeverityText() and result = s)
  or not exists(string s | s = d.getSeverityText()) and result = "<unknown-severity-text>"
}
from Diagnostic d
select d, diagnosticPath(d), diagnosticLine(d), diagnosticColumn(d),
  d.getSeverity(), diagnosticSeverityText(d), d.getTag(), d.getMessage()
