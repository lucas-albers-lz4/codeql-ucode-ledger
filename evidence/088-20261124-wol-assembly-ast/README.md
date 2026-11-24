# Claim 088 portable evidence

The [oracle](source-first-oracle.json), [fixture](controls.uc),
[testing query](WolAssemblyAst.ql), [preflight](preflight.json) and
[normalized receipt](run-receipt.json) describe the isolated source-staged
run. Raw BQRS/JSON output, routing receipt, logs and database remain under
ignored `work/wol-assembly-ast-20261124-a/` on the originating machine.

The receipt replaces the absolute run root in commands with `<RUN_ROOT>` and
the CodeQL executable with `<CODEQL_2_27_4>`. Its entity rows retain exact
staged relative source URIs and line/column ranges. The preflight retains
the original local paths; those identify this run and are not portable file
access. Raw hashes connect the normalized receipt to the local output. A new
machine must rerun to authenticate execution. The query observes AST shape
only and does not emit a security alert.
