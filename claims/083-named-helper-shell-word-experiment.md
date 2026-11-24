# Claim 083: named-helper shell-word experiment

**Status:** Demonstrated

**Scope:** A fresh local, explicit-query matrix for a testing-tagged named-helper shell-word candidate. It checks a returned-handler argument passed to a uniquely named same-file helper whose formal is interpolated into an imported `fs.popen` command template. The matrix uses one pinned real LuCI file and 20 synthetic controls.

**Out of scope:** Default-suite promotion, a current-source alert, installed package bytes, RPC registration or reachability, full shell quote state, vulnerability, broader helper flow, and consumer acceptance. The real `luci.lldpd` has only four visible fixed-literal actuals and is a near miss for request-derived flow, not a safety result.

## Revisions and context

- LuCI source: clean `b2e0be4b46ec0fd43394c081fa7c50657af14011`, `applications/luci-app-lldpd/root/usr/share/rpcd/ucode/luci.lldpd`, Git blob `3774e222cec2f43f73edb6fb07978dab14ed6d36`, SHA-256 `a9d6e6477307408a130ce20ad9f92813dfeca611e5c8a5a7a86f2ca746081eac`.
- Producer: clean local disposable branch `security/helper-shell-word-experiment` at `3111982595ab5cc873d95db09bb0ae71057d63e8`; query SHA-256 `43143b692f848bcb490a9bf3333adeb0073285fd057152c893deaac9f822593e`. The preflight recorded uncommitted query/control bytes on base `b0e18ec39b99be3ae13e74d1171035140c27dcfd` before this final commit; the tested query hash matches the committed bytes.
- Source-first oracle SHA-256: `f269580b4cc3e17c37b5e9fe07836041173c3270c15a9982fd6a211f490556f9`. The original dynamic/fixed pair was revised to returned `methods.getStatus.call` syntax before CodeQL output. Additional controls and expectations were frozen in the run-d preflight before output.
- Tool: local CodeQL CLI 2.27.4; extractor executable SHA-256 `c7bde2d31303127f6bf8ebbbb364a5a47840867b67962a013032a3b6bbe7f8d2`, reused from a recorded pack build at `8375887ed14825dd59addbfd0df43616d9e684fb`.

## Evidence required and observed

1. The fresh run staged exactly 21 independently hashed files under proposed `usr/share/rpcd/ucode/` paths. `SuccessfullyExtractedFiles` returned each exact staged identity once, and `ExtractionErrors` returned zero tuples. Preflight and post-run source hashes match. This is source staging, not package-install verification.
2. The source-first expected results were one row each for `helper-dynamic-positive.uc` and the distinct `trailing_word_positive.uc`, and zero for the real file and 18 controls. Explicit query and SARIF each returned exactly those two positives at `12:23–43` under rule `ucode/m4/named-helper-shell-word`; no other row appeared. The real source's four fixed-string calls and fixed-literal synthetic counterpart are eligible near misses for the modeled request-derived helper argument.
3. Discriminating controls cover duplicate/shadowed helper names, augmented/update writes, formal reassignment, request/formal/helper loop bindings at active uses, a catch binding, nested-block declarations/table/return, imported sink shadowing, earlier dynamic quote-context substitution, literal quoting, and word fragments. Supplemental AST witness CSVs identify the intended call, formal, sink and control entities. Those witness queries were run locally but their invocations are not in the ten-command matrix log; they support interpretation, not a separately authenticated run.
   A later independent requery attempt on a copied database failed at CodeQL extension-pack resolution before producing output; its failure is retained under ignored `work/helper-shell-witness-verify-e/` and is not counted as a pass.
4. A read-only adversarial review found the earlier binding and scope gaps, which were corrected and rerun with new controls. Its final review found no concrete false-positive path in these 21 files. The query remains testing-tagged. Its Program-ancestry exclusion does not explicitly model every unbraced layout; unsupported identities and complete shell semantics remain unknown.

## Run record

- Date/environment: 2026-11-24 UTC, isolated macOS run `work/helper-shell-run-d/` with its own stage, database, cache, temp and output paths; the source worktree was clean. The run owned its writable database and caches. Raw artifacts remain in ignored `work/` and are not portable.
- Commands/exits: database init, index and finalize; successful-file and error query/decode; candidate query/decode; explicit SARIF analyze: ten recorded commands, all exit 0. Index took 0.784 seconds/119,980,032 bytes peak RSS; finalize 1.120 seconds/229,785,600 bytes; candidate query 2.903 seconds/461,389,824 bytes; SARIF analyze 1.930 seconds/207,503,360 bytes. These are 21-file timings, not corpus-scale estimates.
- Portable artifacts: [normalized receipt](../evidence/083-20261124-helper-shell-experiment/run-receipt.json) SHA-256 `301e21641f54ff7f7233c2c1cde7811f12ab9604aae90c30893b94a6879f9f91`, [source-first oracle](../evidence/083-20261124-helper-shell-experiment/source-first-oracle.json), witness CSVs and [provenance notes](../evidence/083-20261124-helper-shell-experiment/README.md). The receipt retains exact relative identities, multiplicity, command arguments/exits/timings and raw output hashes with local roots normalized. The local producer commit has not been pushed.
- Follow-up: keep this a separate experimental rule while testing actual helper-flow candidates in a larger current slice and resolving unbraced scope/quote-context behavior. A fixed-literal absence is not negative proof for all callers or runtime inputs.
