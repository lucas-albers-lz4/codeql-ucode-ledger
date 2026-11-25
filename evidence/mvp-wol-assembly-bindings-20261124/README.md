# Returned WOL handler assembly bindings

A testing-only CodeQL table matched the assembly in the pinned LuCI WOL
handler and three controls. The query observes the returned method table,
handler formal, map callback and local declaration/use, join, concatenation
and argument 0 of source-declared imported `fs.popen`. It records the
callback body and fixed-path comparison independently.

| Input | Source → sink | Callback body | Fixed-path comparison |
|---|---|---|---|
| `luci.wol` | 41 → 42 | Single-quote body | Matched |
| `identity.uc` | 6 → 7 | Identity | No matching comparison |
| `partial_quote.uc` | 6 → 7 | Unknown | No matching comparison |
| `altered_guard.uc` | 41 → 42 | Single-quote body | No matching comparison |

The 17 other fixtures produced zero table rows. They change the input
array, callback identity, join call or separator, local parts binding or
contents, source formal, builtin names, sink import, or returned method
identity. The [fixture generator](make-controls.py) and [source-first
oracle](source-first-oracle.json) record each control. The 21 staged paths
were selected once each as plain `rpcd_raw_mode_full_path` and extracted
once each with zero extraction diagnostics. The four output rows each
have 12 distinct AST ranges. The ranges were checked against the staged
source snippets, and the expected path, source line, sink line and labels
were compared as an exact multiset.

## Revisions and model contract

LuCI `b2e0be4b46ec0fd43394c081fa7c50657af14011` was clean. Its WOL
file was source-staged at `usr/share/rpcd/ucode/luci.wol` from Git blob
`fd9e9f0485ab6baec96ae089caf1089a6d471c99`, SHA-256
`51214ec57bcbd8d50e65016efda2a05e8eb7822dc7e510d014965834c61ef92b`.
An independent check of the retained `work/stage6-luci` checkout on
2026-11-25 ran `git rev-parse HEAD`, `git status --porcelain=v1`,
`git hash-object` and `shasum -a 256` for that source file: the commit, clean
status, blob OID and SHA-256 matched these values. The canonical run's own
preflight recorded the source dirty status and staged-file hashes, but not a
separate source-checkout `rev-parse HEAD`; this independent check closes that
recording gap for the retained source checkout.
Producer `104a398468f214961168d2edc9a10be45b80062f` was fetched from
`main` into a disposable checkout and had one local testing query at
run time. The matching macOS extractor was copied from the [PR #161 build
receipt](../mvp-producer-grammar-integration-20261124/receipt.json).
The frozen grammar base is `4a243af329fae2f4ff01e0fc80133cbab8314600`
with the merged Wi-Fi grammar patch. The copied binary's SHA-256 is
`6ed90de2e6b352daa939ad1d0c627f847383307f212168ad11d9dd06f4faf15b`.
The manifest comments were refreshed from current `main`. CodeQL 2.27.4
and the exact locked packs ran with a private database, HOME, TMPDIR and
cache. The mechanical diff from claim 088's preserved producer copy
showed generated schema/AST changes, request-argument scope changes and
new smoke queries. Models and the default direct shell rule matched.

The [testing query](WolAssemblyBindings.ql) uses existing lexical reads for
the returned table, request formal, map result and callback parameter.
Conservative whole-file token checks reject ambiguous callback and array
uses and competing declarations, imports and writes to the assumed builtin
names. The recognizer requires map and join in the same supported handler
assembly and recognizes only the direct initializer-to-initializer shape,
with a literal space separator and a direct named import at the sink.
The fixed-path label is specific to the two WOL source comparisons in the
same branch as the sink. The quote-body label matches the exact helper AST,
including its escape token.

OpenWrt `4e9642517b48bae612ff10fb72fb9199e559500e` was consulted for
the ucode source pin. At that pin, the library implementation passes each
array element to the callback as argument 0 and stores its result in a new
array. Join stringifies those resulting elements with the requested
separator. That source contract supports reviewing a narrowly scoped
element-to-result model. The table does not add a reusable flow or
sanitizer model. [Pinned ucode library source](https://github.com/ucode-lang/ucode/blob/b885dd0fe1e974551fb1233ca5f3aa74d80b74d9/lib.c)

## Run record and limits

The [normalized receipt](run-receipt.json) carries exact commands, exits,
phase timings, input and output hashes, route identities and result ranges.
It substitutes `<RUN_ROOT>`, `<PRODUCER>` and `<CODEQL_2_27_4>` in commands.
All ten canonical CodeQL commands exited 0. Raw logs, fixtures and the
database remain under ignored `work/wol-bound-assembly-run-g`. To regenerate
the fixture manifest, place the pinned real WOL file in
`stage/usr/share/rpcd/ucode/luci.wol` relative to a copy of the fixture
generator, and run the generator from that run directory.

The initial manual compile setup had a malformed temporary path, followed
by an import error fixed by explicitly importing the AST internals. Runs
A and B compiled and extracted but failed dependency resolution during the
diagnostics query because the command used a different cache directory
from the populated locked-pack cache. An exploratory run C passed with
18 inputs. Tightening attempts D and E stopped on compile errors. Attempt
F returned zero rows because the initial static-key check excluded quoted
object keys. The canonical run fixed that and added duplicate-method,
escaped-separator and quoted-array mutation controls. Peak RSS was
unavailable because macOS `/usr/bin/time -l` was denied by the sandbox.

This source-staged table provides binding and assembly evidence. Runtime
callee identity, shell behavior, deployed bytes, registration and
authorization remain unmeasured. This run has no production query,
security alert, SARIF acceptance or consumer handoff. Broader flow and
query work remain with the existing owners. [Producer #50](https://github.com/lucas-albers-lz4/codeql-ucode/issues/50), [producer #54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54)
