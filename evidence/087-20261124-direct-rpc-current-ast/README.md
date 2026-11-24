# Claim 087 portable evidence

The [source-first oracle](source-first-oracle.json), [fixture](controls.uc),
[testing query](QuotedSwitchAst.ql) and [normalized receipt](run-receipt.json)
describe the canonical fresh local run. The original database and raw output
stay in ignored `work/direct-rpc-nearmiss-ast-20261124-c/` on the originating
machine and are not portable. The receipt's `raw_hashes` identify the raw
preflight, command log, AST rows, diagnostic decodes, routing JSON and SARIF.

For portability, the receipt replaces the absolute run root in command
arguments and working directories with `<RUN_ROOT>` and the local CodeQL
executable with `<CODEQL_2_27_4>`. All other command text and observed exits,
wall times and output hashes are retained. AST entity source URLs are
normalized to the pinned staged relative URI and retain their exact line and
column locations. The SARIF rule ID, URI and region are copied from the raw
result. The normalized receipt is a review aid, not execution authentication;
the claim's fresh-run status depends on the retained raw run and independent
source/result comparison described in [claim 087](../../claims/087-current-luci-quoted-switch-ast.md).
