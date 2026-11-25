# Testing-only WOL map/join identity-callback rule candidate

This is a source-shape experiment, not a production alert, security finding, or runtime proof. The [query](WolUnquotedMapJoin.ql) starts with the bounded returned-handler binding table from the [prior assembly run](../mvp-wol-assembly-bindings-20261124/README.md). It emits a problem only when the bound map callback has one formal and a direct `return` of that formal. It requires the request formal, `request.args.args`, an unmodified `parts` initializer, literal-space `join`, binary concatenation, and a source-declared `fs.popen` import. A fixed executable comparison is reported separately in the message; it does not suppress the result. The real quoted helper and a partially quoting helper are outside this positive predicate.

## Revisions and source-first expectations

- Producer `main`: `104a398468f214961168d2edc9a10be45b80062f`. It was fetched into a disposable checkout and clean before adding this testing query. There was no QL or extractor delta from the prior binding run at that same revision. [Producer #50](https://github.com/lucas-albers-lz4/codeql-ucode/issues/50) keeps production taint on `Models` pending sources, sinks and resolution; [#54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54) owns gated M4 command-injection work and disallows unsupported path claims.
- LuCI `b2e0be4b46ec0fd43394c081fa7c50657af14011`, clean; WOL source Git blob `fd9e9f0485ab6baec96ae089caf1089a6d471c99`, SHA-256 `51214ec57bcbd8d50e65016efda2a05e8eb7822dc7e510d014965834c61ef92b`. Its source-stage bytes matched. These are upstream source bytes staged at an installed-looking path, with no package-byte comparison.
  The retained `work/stage6-luci` checkout was independently checked on
  2026-11-25 with `git rev-parse HEAD`, `git status --porcelain=v1` and
  `git hash-object` for the WOL file: the commit and blob matched, and status
  was empty. The run's own stage hashes bind the extracted bytes.
- CodeQL CLI 2.27.4, executable SHA-256 `bb3a754e126ed061b5f3356531cd5501872ab3864bd665b2d1afdbf8a67a146d`. The copied macOS extractor SHA-256 `6ed90de2e6b352daa939ad1d0c627f847383307f212168ad11d9dd06f4faf15b` has the prior [build provenance](../mvp-producer-grammar-integration-20261124/receipt.json) and matched current source, grammar, schema and locks. The QL lock hash was `bce2891940f09fcac3337b250707047ba9fd06d307abdbc7cb42c2ed193751a3` for both packs. Locked dependencies were copied into this run's private `HOME`.
- The [source-first oracle](source-first-oracle.json), SHA-256 `b2d12f9444744c4df7ca5e60dfe1198add5a6aac938ee2980509a8ac59a96861`, was prepared before compilation or output inspection. It pins all 22 stage hashes and expected result multiplicities. The query SHA-256 is `03f6aa08140c3f67000c8e58fff23694f42147d9eb1bb217ba857290f06804ce`.

## Fresh run

The isolated run is under ignored `work/wol-rule-candidate-20261125-a`, with its own stage, database, output, `HOME`, `TMPDIR`, and caches. The [normalized receipt](run-receipt.json) records exact CodeQL commands, exit statuses, wall times, routing, source identities, output hashes and result locations. Available disk was 91 GiB. Peak RSS was unavailable because the macOS timing facility was denied in the earlier run and was not retried. All 11 commands exited 0: compile 4.024 s; database init/index/finalize 2.525 s; successful-file and error queries 3.059 s plus 0.464 s decode; candidate query 5.356 s plus 0.240 s decode; SARIF 3.687 s. The command wall-time sum was 19.355 s. No full-corpus timing is inferred.

Compilation and SARIF generation warned that this testing problem query
does not declare `@severity` or `@problem.severity`. The commands exited 0,
but the SARIF rule has no severity and its results have no level. This
metadata is insufficient for production use.

All 22 stage paths routed once as `plain_route_selected` under `rpcd_raw_mode_full_path`, extracted once each, with zero diagnostic rows. The query and fresh SARIF each had exactly two results:

| Source | Sink line | Callback | Fixed-path comparison |
|---|---:|---|---|
| `identity.uc` | 7 | Direct `return s` | No matching comparison |
| `identity_fixed_guard.uc` | 42 | Direct `return s`, retaining the real WOL guard | Matched |

The real `luci.wol:42` uses the single-quoting callback and produced no result. The other 19 source controls also produced no result, including fixed arguments, wrong callback, no join, callback/parts shadowing and writes, mixed parts, wrong import, local `popen` shadow, builtin shadows, nonreturned handler, request write, partial quote, altered guard with quoted callback, and mixed quoted parts. The exact two-row path/line/multiplicity oracle was checked against both BQRS decode and SARIF.

## Boundary

This rule recognizes one explicit identity-callback assembly. An unknown or partially quoting helper is **unclassified**, not proven safe; other unquoted callback forms can be false negatives. The callback-use link relies on spelling plus whole-file exclusions rather than a resolved declaration read. Those exclusions may also suppress valid cases. The fixed-path label reports a syntactic comparison in this source shape, not a runtime guarantee about the executable or a shell-word quote barrier. The query does not establish runtime callee identity, shell parsing, deployed bytes, handler registration, reachability, authorization, impact, or vulnerability. Keep it testing-only pending broader model and control review under #50/#54; do not add it to the default suite on this evidence alone.
