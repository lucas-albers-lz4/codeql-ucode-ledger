# Claim 076: historical Tailscale candidate-query baseline

**Status: Demonstrated for the selected source files, controls, post-merge producer pin and local run.**

## Claim and boundary

At clean producer `18afe771568d373088edee7a790825ee46dec9e0`, the
testing-tagged `ShellInjection.ql` returns no candidate for the upstream LuCI
Tailscale `do_login` source in either its vulnerable parent or actual fixed
revision. Both files extract exactly once without errors; CodeQL yields the
predeclared request-source and line-164 `popen` AST sites. The same query
returns exactly one row for a direct positive model control and none for the
nested-shell positive target, patched-form control or eligible unrelated-value
near miss. This is a bounded current-model gap, **not** detection of the
historical issue or recognition of its fix.

The maintainer [advisory](https://github.com/openwrt/luci/security/advisories/GHSA-xwc5-mx58-rh35)
attributes the historical command injection to individually quoted user
values inside an outer double-quoted `/bin/sh -c` argument. The
[mainline fix](https://github.com/openwrt/luci/commit/507ab5e45c304543d4111af9a331db0f03be6bcb)
quotes the entire `login_cmd + ' &'` command at line 164. These runtime and
access conditions come from the advisory, not this static run. The current
query's bounded same-function binding model does not follow the source through
`trim`, `push`, the `loginargs` array and `join`, nor does it model the nested
shell interpretation or the local `shell_quote` helper's semantics. That is a
source-model inspection, not a proof that any single change would make the
case detectable.

## Pins and source-first oracle

| Input | Git revision/path or fixture | SHA-256 | Predeclared target |
|---|---|---|---|
| Vulnerable parent | LuCI `46cd82328dfb7fbb15961c63f9e674a41cef2500`; `applications/luci-app-tailscale-community/root/usr/share/rpcd/ucode/tailscale.uc` | `3029c32d7ccd18efb95355aa915841e2bf467b0de147ce1a65b68c55fec9d280` | `request.args.form_data` 140:21–42; field reads at 152:28–48 and 153:36–64; `popen` 164:3–48; no current candidate expected. |
| Fixed | LuCI `507ab5e45c304543d4111af9a331db0f03be6bcb`, same path | `12bffca1f06aae14363f12d98680c0ca3a07223babd26131cc7c1612baf8fc4e` | Same source sites; `popen` 164:3–59; no current candidate expected. |
| Four controls | Source-first fixtures under `controls/usr/share/rpcd/ucode/` | See [oracle](../evidence/076-20261124-tailscale-baseline/source-first.json) | `model_pos.uc` one exact current-query row; `nested_pos.uc`, `nested_fixed.uc` and `nested_near_miss.uc` zero current-query rows, with the first two reserved as future detector discrimination controls. |

The oracle and control bytes were prepared **before** this CodeQL run. The
upstream Git blobs, stage digests, control source/sink spans and expected exact
tuple are in that oracle. `nested_pos.uc` preserves the vulnerable outer
double-quote while carrying the input through `trim` → `push` → `join`;
`nested_fixed.uc` changes only the outer quote form; `nested_near_miss.uc`
keeps the request read and vulnerable-form sink but pushes an unrelated
literal. The historical files are pinned source staged at installed-style
paths; no package build or installed-byte comparison was performed.

## Local run, 2026-11-24 UTC

The CLI was CodeQL 2.27.4 on macOS arm64. The selected post-merge producer
checkout was clean. A compatible OS X extractor pack built at
`8375887ed14825dd59addbfd0df43616d9e684fb` was copied into the run;
the selected producer and pack-build revision had no diff in the inspected
Cargo lock, extractor metadata, dbscheme, generated TreeSitter file and
build/grammar scripts. The copied extractor SHA-256 was
`c7bde2d31303127f6bf8ebbbb364a5a47840867b67962a013032a3b6bbe7f8d2`.
Each parent, fixed and four-control stage had its own database, stage,
writable caches and temporary directory. `HOME` was inherited under the
environment rule. All large raw output remains in ignored
`work/mvp-tailscale-baseline-20261124-a/`, which is **not** a portable path.
The [reviewed receipt](../evidence/076-20261124-tailscale-baseline/receipt.json)
normalizes this to `$RUN`; [commands](../evidence/076-20261124-tailscale-baseline/commands-normalized.json)
retain every argv, exit and phase duration. The [real-source](../evidence/076-20261124-tailscale-baseline/TailscaleAstWitness.ql)
and [control](../evidence/076-20261124-tailscale-baseline/TailscaleControlWitness.ql)
AST witness queries are preserved with hashes in the receipt.

For each stage, `database init`, `index-files --include=**/*.uc`, `finalize`,
both diagnostic queries and decodes, and `ShellInjection.ql` and CSV decode
all exited 0. The AST witness queries and decodes also exited 0. Exact
successful-file identities and zero errors were checked before candidate
results, and all six staged file hashes matched after the run.

The testing query's stderr warns that a problem query must select an even
number of columns; `ShellInjection.ql` selects seven. The BQRS/CSV output is
valid for this bounded observation, but the warning blocks treating it as a
SARIF alert contract. A low-heap query-loading cache warning also appears;
both are retained in the receipt.

| Stage | Exact successful files / errors | AST witness | Candidate rows |
|---|---|---|---:|
| Parent | `tailscale.uc` once / 0 | Three source properties at 140, 152, 153 paired with `popen` 164:3–48, once each | 0 |
| Fixed | `tailscale.uc` once / 0 | Same source sites paired with `popen` 164:3–59, once each | 0 |
| Controls | `model_pos.uc`, `nested_pos.uc`, `nested_fixed.uc`, `nested_near_miss.uc` once each / 0 | Seven predeclared source/sink control pairs at their exact file/line/column sites | 1 |

The sole candidate tuple was exactly
`(MemberExpression, "shell-injection candidate via popen in model_pos.uc", CallExpression, popen, probe, 6, 6)`.
The three nested controls emitted none. Parent index, finalize and candidate
query took 0.639 s, 1.286 s and 2.703 s wall; the candidate query's macOS
`time -l` peak resident size was 664,682,496 bytes. Full phase measurements
and exits are in the receipt. These are tiny selected files, not a full-corpus
cost estimate.

## What remains

The baseline establishes actual AST sites, exact extraction and a live current
model control, then observes the expected absence of nested-path candidates.
Zero rows on the fixed source do not establish the fix's safety or a valid
sanitizer model. There was no default-suite security query, Linux CI, SARIF,
consumer handoff, runtime test or whole-corpus scan. The next producer work is
to model both input paths and the outer shell context with binding-aware
quote controls, then rerun the real parent/fix and eligible near misses. The
release stages are in [MVP-1.md](../MVP-1.md).
