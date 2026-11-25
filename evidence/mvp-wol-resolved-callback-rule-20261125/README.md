# Resolved callback WOL rule candidate

This follow-up supersedes the callback-name check in the [first testing-only candidate](../mvp-wol-unquoted-rule-candidate-20261125/README.md). The producer's existing `VariableReadAccess` did not resolve `function shellquote`: `Variables.qll` omitted `FunctionDeclaration` from its declarations and scopes. The [disposable model patch](FunctionDeclaration-Variable-binding.patch) adds that lexical binding. The [candidate query](WolUnquotedMapJoin.ql) now requires `callbackUse` to be a unique `VariableReadAccess` of the exact callback `FunctionDeclaration` and rejects writes to that binding. It also declares `@problem.severity recommendation`. This patch is an experimental dependency, not a validated general function-binding model or a production change.

## Pins and source-first controls

- Producer `main` `104a398468f214961168d2edc9a10be45b80062f`, clean before the local model patch and two testing queries. There was no source, grammar or lock delta from the previous WOL run at this revision.
- LuCI `b2e0be4b46ec0fd43394c081fa7c50657af14011`, clean. Its `applications/luci-app-wol/root/usr/share/rpcd/ucode/luci.wol` Git blob was `fd9e9f0485ab6baec96ae089caf1089a6d471c99`; SHA-256 `51214ec57bcbd8d50e65016efda2a05e8eb7822dc7e510d014965834c61ef92b`. The stage matches these upstream source bytes at an installed-looking path; package bytes were not checked.
- CodeQL CLI 2.27.4 executable SHA-256 `bb3a754e126ed061b5f3356531cd5501872ab3864bd665b2d1afdbf8a67a146d`. The copied macOS extractor SHA-256 was `6ed90de2e6b352daa939ad1d0c627f847383307f212168ad11d9dd06f4faf15b`, with matching source/grammar/schema and [prior build provenance](../mvp-producer-grammar-integration-20261124/receipt.json). Both QL lock hashes were `bce2891940f09fcac3337b250707047ba9fd06d307abdbc7cb42c2ed193751a3`; dependencies were copied to the new run's private `HOME`.
- The [source-first oracle](source-first-oracle.json), SHA-256 `b2d12f9444744c4df7ca5e60dfe1198add5a6aac938ee2980509a8ac59a96861`, was prepared before this run. It pins 22 source hashes, extraction multiplicities, two expected candidate rows and 20 expected zero-result paths. A separate [binding audit oracle](audit-oracle.json), SHA-256 `141ca960ef2ffedd28dca59ea17bdb4d0cf5a6c61184fe63b18dfdef3ca76d5d`, was prepared before the audit query. Candidate query SHA-256 `ee9a8864d96b30e8c026a3fa6111cbc2f96954e38bc81a85ef4503a13e83320f`; patched `Variables.qll` SHA-256 `83a8b73ec4cb56aba43a8c707c96fe8b49bb9f3b17ea8d5ef70f65808c45c74b`.

## Fresh isolated run

Run-owned stage, database, outputs, `HOME`, `TMPDIR` and caches are under ignored `work/wol-rule-candidate-20261125-b`. The [normalized receipt](run-receipt.json) lists exact commands, exits, wall times, route decisions, successful identities, results and raw artifact hashes. The new database did not reuse the prior database. Available disk was 91 GiB. Peak RSS was unavailable; the macOS timing facility had been denied in the earlier run and was not retried.

All 22 source paths routed once as `plain_route_selected` (`rpcd_raw_mode_full_path`), extracted once each, and had zero extraction diagnostic rows. All 11 canonical commands exited 0. Compilation took 4.636 s; database init/index/finalize 2.592 s; successful-file and error queries 3.610 s plus 0.502 s decode; the candidate query 6.144 s plus 0.266 s decode; SARIF 4.247 s. The sum was 21.997 s. These are small-slice timings only.

Candidate BQRS and fresh SARIF each contained the exact two expected results, once each:

| Path | Sink line | Callback binding | Executable comparison |
|---|---:|---|---|
| `identity.uc` | 7 | top-level `transform`, direct `return s` | no matching comparison |
| `identity_fixed_guard.uc` | 42 | top-level `shellquote`, changed to direct `return s` | fixed-path comparison retained |

The actual quoted `luci.wol:42` and 19 other controls yielded no candidate row. Those controls cover fixed arguments, wrong callback, no join, callback shadow/write, parts shadow/write/mutation, mixed parts, wrong import, local `popen` shadow, builtin shadows, nonreturned handler, request write, partial quote, altered guard with quoted callback, and mixed quoted parts. The fixed-path comparison is a separate label, not a quote barrier or suppression rule.

The [binding audit query](WolCallbackBindingAudit.ql) then ran against this same, unchanged run-owned database. Its two commands exited 0 in 2.401 s and 0.245 s. Five exact source-first audit rows confirmed: `identity.uc` use line 6 → declaration line 2 with zero writes; `identity_fixed_guard.uc` 41 → 11, zero; real `luci.wol` 41 → 11, zero; `callback_shadow.uc` 7 → inner declaration line 6, zero; `callback_write.uc` 7 → declaration line 2, one write. The latter two produced no candidate result. The severity metadata appears in SARIF as `recommendation` with default level `note`; there was no severity warning. CodeQL reported only its low-heap stage-cache warning.

## Boundary

The rule is restricted to this direct identity-callback map/join assembly. An unknown or partially quoting callback remains unclassified. Other unsafe callback forms and broader shell assembly can be false negatives. The patch changes the shared `Variable` and SSA universe: same-scope function and lexical declarations can yield ambiguous bindings, and function-declaration values have no reviewed downstream data-flow initializer. The WOL query rejects ambiguous reads, but these broader model effects and declaration-order/nested-scope controls remain untested. The syntax and reviewed ucode library source support the bounded map/join interpretation, but the run does not establish deployed bytes, runtime callee identity or shell parsing, registration, reachability, authorization, impact, or vulnerability. Keep the query and model patch testing-only under [producer #50](https://github.com/lucas-albers-lz4/codeql-ucode/issues/50) and [#54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54). No default-suite promotion or push occurred.
