# Claim 013: getFeatures direct call inventory

**Status: Demonstrated for the named pinned source and controls.**

## Claim and boundaries

For the pinned LuCI fixture, the actual `GetFeaturesDirectExec.ql` query
reports exactly the five expected syntactically direct `system` and imported
`fs` `popen` call sites inside `getFeatures.call`. A query result identifies
the supported source shape; it does not prove runtime reachability, builtin
identity, device execution, taint or authorization. The query is not a fixed
command verifier and does not claim every possible call form.

## Run: 2026-11-18 UTC

Producer `d3588ca6821fe983d240fcbb2e80692fabcc6aab`, CodeQL 2.27.4. The
source and [query contract](https://github.com/lucas-albers-lz4/codeql-ucode/blob/d3588ca6821fe983d240fcbb2e80692fabcc6aab/docs/m4-getfeatures-direct-exec.md)
identify `system` at lines 268 and 275 and `popen` at 278, 294 and 315.
The query and model were inspected before the run. The fresh single-source
database, fixture digest and extraction diagnostics are recorded in
[claim 002](002-getblock-query.md). Ran the real query with `--threads=1
--ram=2048`, then decoded entity locations as JSON; both commands exited 0.
[Results](../evidence/013/real.json) have exactly these five rows, with
source spans `268:32–268:94`, `275:38–275:107`, `278:13–278:50`,
`294:9–294:38`, and `315:9–315:41` respectively.

A second fresh database was created by the retained
[control runner](../evidence/013/run-controls.py). Its two synthetic inputs
were both successfully extracted with [zero errors](../evidence/013/errors.json).
The actual query selected exactly the positive `popen` and `system` calls at
line 3; same-named calls in a different method and a `popen` imported from
`other` produced no rows. The [control results](../evidence/013/results.json),
[extraction identities](../evidence/013/extracted.json) and
[routing receipt](../evidence/013/routing.json) are retained with local path
prefixes normalized. Raw databases and command logs remain under ignored
`work/`. These controls test those particular method/import boundaries, not
lexical resolution in all scopes or exclusion of nonliteral commands.
Broader query and modeling work remains owned by
[ucode #54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54).
