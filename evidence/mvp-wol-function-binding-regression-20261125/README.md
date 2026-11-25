# FunctionDeclaration binding regression matrix for the WOL candidate

The first resolved-callback [model patch](../mvp-wol-resolved-callback-rule-20261125/FunctionDeclaration-Variable-binding.patch) added every `FunctionDeclaration` to `VariableReadAccess`. This source-first matrix tests that shared-model change against collisions, ordering, scopes, formals and writes. The [narrower disposable patch](NarrowFunctionDeclaration-binding.patch) suppresses same-scope function/function and function/lexical-declarator collisions, requires a declaration to precede its use, and keeps an unmodeled inner function declaration from exposing an outer binding. It is a prototype for review, not a production patch.

## Pins and inputs

- Producer `main` `104a398468f214961168d2edc9a10be45b80062f`. Separate baseline and patched disposable copies had that HEAD; their only local changes were the matrix query and, in the patched copy, the experimental model/query changes. The narrower copy was derived from that patched copy. CodeQL CLI 2.27.4 executable SHA-256 `bb3a754e126ed061b5f3356531cd5501872ab3864bd665b2d1afdbf8a67a146d`; matching copied macOS extractor SHA-256 `6ed90de2e6b352daa939ad1d0c627f847383307f212168ad11d9dd06f4faf15b` with [prior build provenance](../mvp-producer-grammar-integration-20261124/receipt.json). QL dependencies and locks matched the earlier WOL run.
- The [source-first oracle](source-first-oracle.json), SHA-256 `a2b9b0ea694625dd97977e301d2a5b2da700ecc452090e26b0b366108ee13948`, pins 33 stage hashes and baseline/broad-patch expected matrix rows. It was written before the canonical database run. The [narrow oracle](narrow-oracle.json), SHA-256 `90dbcf21fd53508f7e27aa2e0be4250b4d2e9d417b31bbe478e025a092456e6f`, was written before the narrow-patch queries. The eight new [matrix controls](controls) are retained here. The remaining inputs are the prior 22 WOL files and the producer's `order.uc`, `ssa_pos` and `ssa_neg` fixtures.

## Results

The fresh database under ignored `work/wol-function-binding-regression-20261125-d` used private stage, database, output, `HOME`, `TMPDIR` and cache paths. All 33 files routed once as `plain_route_selected` (`rpcd_raw_mode_full_path`), extracted once each, and had zero diagnostic rows. The 25 canonical commands all exited 0, with 67.651 s total command wall time. The narrow patch ran on that unchanged database with a separate compilation cache; its ten commands all exited 0 in 38.992 s. The [normalized receipt](run-receipt.json) preserves exact commands, exits, timings, identities, raw output hashes and all normalized result tuples. Available disk was 91 GiB; peak RSS was unavailable on this macOS host. These timings are for this small source-staged slice only.

The [matrix query](FunctionBindingMatrix.ql) selected each `print(identifier)` read, its declaration line and declaration kind. Exact source-first row multisets matched:

| Control | Baseline rows | Broad patch rows | Narrow patch rows | Observation |
|---|---:|---:|---:|---|
| Function plus `let` in one scope | 1 | 2 | 1 | Broad patch binds the same read to both declarations. |
| Two functions in one scope | 0 | 2 | 0 | Broad patch binds the same read twice. |
| Use before function declaration, then after | 0 | 2 | 1 | Narrow patch leaves the earlier use unbound. |
| Nested function and sibling block | 0 | 2 | 2 | Inner read binds inner declaration; sibling read binds outer. |
| Formal shadowing | 1 | 2 | 2 | Inner read binds formal; outer read binds function. |
| Direct write to function name | 0 | 1 | 1 | Binding exists and the WOL rule separately rejects writes. |
| Write through nested closure | 0 | 1 | 1 | Binding exists; the WOL rule's write exclusion is whole binding. |
| Existing ordinary `let` shadowing | 3 | 3 | 3 | Exact rows unchanged. |

The producer's existing `VariableOrderBindings` result was 17 rows, `VariableOrderFlow` was 2 rows, and `SsaReachesSystem` was 21 rows. Each full decoded tuple sequence matched exactly across baseline, broad patch and narrow patch. The narrow-patch WOL rule still yielded exactly `identity.uc:7` and `identity_fixed_guard.uc:42`; real quoted WOL and the other controls stayed absent. The broad patch yielded the same two WOL rows. These unchanged queries are a measured regression check, not a proof that every Variable or SSA consumer is unaffected.

An exploratory run before the canonical run had two matrix-query compile failures (missing `UCODE` import, then use of `getArgument` on a raw AST call). Those commands exited 2 and were corrected; their output was not counted as a pass. The canonical run rebuilt a new database with the corrected query and retained command timings.

## Decision boundary

The broad shared-model patch is unsuitable for promotion: two source shapes
produce ambiguous `VariableReadAccess` rows. The [Ucode manual](https://ucode-lang.org/manual/)
describes ordinary declarations as not hoisted, supporting a cutoff before
declaration. It also describes later same-scope declarations winning in
permissive mode. The narrower patch removes the measured ambiguities and
preserves the tested WOL positives and existing query rows, but it suppresses
all function bindings in a same-scope collision, including reads before the
later declaration. Its nested-function guard can hide an outer binding even
before the inner declaration. These are conservative gaps, not a general
binding model. Forward declarations, import/formal collisions, more scope
forms and shared Variable/SSA value-flow effects remain untested. Shared-model
promotion therefore remains blocked. The WOL rule and model patch remain
testing-only under [producer #50](https://github.com/lucas-albers-lz4/codeql-ucode/issues/50)
and [#54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54); no
default-suite change or push occurred. No runtime shell, authorization,
reachability, deployed-byte, impact or vulnerability claim follows from
these results.
