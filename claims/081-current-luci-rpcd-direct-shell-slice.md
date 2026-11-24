# Claim 081: current LuCI rpcd slice extraction and suite observation

**Status:** Demonstrated

**Scope:** One fresh, isolated CodeQL 2.27.4 run over all 17 tracked LuCI files under `root/usr/share/rpcd/ucode` at LuCI `b2e0be4b46ec0fd43394c081fa7c50657af14011`. The claim covers source-to-stage byte identity, extraction identities and errors, the separate route probe, and the resolved default `code-scanning` suite's SARIF result for the experimental direct RPC shell-word rule.

**Out of scope:** Package installation or deployed-image contents; security-negative, completeness, or vulnerability conclusions; RPC registration/reachability, runtime behavior, and consumer acceptance. The zero-result rule observation does not establish that the slice is safe. Sol-reviewed WOL `popen` site is outside this template rule's supported scope and remains unknown.

## Revisions and context

- LuCI commit: `b2e0be4b46ec0fd43394c081fa7c50657af14011` (clean detached tree).
- Producer commit: `78590f24ab20a69eb1ac70258a00165f453d305d` (clean detached tree).
- Consumer corpus lock: `corpus/lock.json`, SHA-256 `b4cbdabb76df90a807aba7d42ae675198c7b7b09c3b84db259a3a4c941b0ea9a`, consumer checkout `66a9c78cd605dbe63645235074b9747ab57b187e`.
- CodeQL: `CodeQL command-line toolchain release 2.27.4`.
- Source-first selection oracle: SHA-256 `ef4abca47ed268c3ef59a64c5c4c33d289d147e6b0bd94695f728c9c77b50be1`.
- Direct rule query SHA-256: `a071facd947a65d3eb48906070cf17ad53d2bd62b54116991437f77fef5e52d8`; suite SHA-256: `6d343f93e37c309b8461da9fafcf67d089737980d7ac42a5409e75df3bd442e5`.
- Existing context: [next shell-family design](../planning/next-shell-family-20261124.md); this is an experimental rule observation, not a promoted security check.

## Evidence required

1. All 17 oracle-selected source files were matched by Git blob, source SHA-256, staged-source SHA-256, and the fresh run's stage SHA-256. The exact successful-file multiset contained those 17 expected installed-path identities once each; the extraction-error query returned zero tuples.
2. A separate direct route probe recorded 17/17 `plain_route_selected` decisions (`rpcd_raw_mode_full_path`), with no exclusions, uncertainty, markup-inconclusive decisions, or duplicate inputs. The route probe used the same staged bytes but is a separate invocation; it does not authenticate the database run.
3. The resolved suite contained `DirectRpcShellWord.ql`, `ExtractionErrors.ql`, and `SuccessfullyExtractedFiles.ql`. SARIF contained the single rule descriptor `ucode/m4/direct-rpc-shell-word` and zero results. This is not a negative security control: no eligible positive/near-miss pair is claimed.
4. This is a same-run local producer observation, not a producer-to-consumer handoff. Source mapping to proposed installed paths is not proof of package or image bytes.
5. The WOL site was reviewed by Sol as out of scope for this template rule and remains unknown; no security interpretation is inferred from its absence in SARIF.

## Run record

- Date and environment: 2026-11-24; isolated run directory `work/luci-rpcd-second-slice-20261124/run-a`, with a dedicated database, staged source, temporary path, output directory and writable cache. The LuCI checkout was clean at the pinned commit.
- Exact commands and exit statuses: `database init`, `database index-files`, `database finalize`, successful-file query and decode, extraction-error query and decode, suite resolution, and `database analyze` for SARIF all exited 0. Per-command wall times and peak RSS are in the normalized receipt. The separate route probe exited 0; its raw routing receipt hash is included there.
- Actual outputs / artifact locations and relevant hashes: [normalized run receipt](../evidence/081-20261124-luci-rpcd-slice/run-receipt.json), SHA-256 `419ab68bebf7878d4da3a5134d57bd69635cbe85b2775d5c90cf616ee2960494`. It records every source path, owner, Git blob, source/stage hash and proposed installed path, exact extracted identity counts, suite descriptor/result count, command exits/timings, and hashes of raw run outputs. Raw database and work artifacts remain under ignored `work/` and are not carried as portable evidence.
- Controls and results: no eligible positive/near-miss control is claimed. WOL is explicitly an out-of-scope unknown for this template rule.
- Status and its limits: Demonstrated only for byte-matched source staging, the exact extraction multiset, the independent route receipt, and the zero-result default-suite run on these inputs and revisions.
- Outstanding unknowns / follow-up: supported direct-handler flow and shell context for source candidates; package/build transformation and installed-byte mapping; eligibility and rule behavior on discriminating source controls; fresh downstream consumer acceptance.
