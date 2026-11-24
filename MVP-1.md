# MVP-1: historical checks to continuous OpenWrt scanning

Planning snapshot: 2026-11-23 UTC. This is an execution plan, not a claim that
either historical defect is detected. Read [AGENTS.md](AGENTS.md),
[PLAN.md](PLAN.md), [the case dossier](planning/mvp-historical-security-20261123.md)
and the relevant claims before each run. The case dossier pins source revisions,
advisories, digests, current model gaps and source-first oracles.

## Operational destination and first release decision

The long-term objective is a maintained CodeQL ucode scanner that checks
incoming OpenWrt and LuCI changes in CI, identifies analyzable files, reports
useful security findings at source locations, and makes missed or unsupported
areas visible. A passing two-case historical test is a **first release gate**,
not evidence that a large, changing OpenWrt corpus is comprehensively scanned.
The release must be followed by corpus-scale and incoming-change adoption
stages below. Treat LuCI and OpenWrt core/feeds as distinct source owners and
inputs; a job in `codeql-openwrt` does not automatically run on upstream PRs.

Deliver a versioned `codeql-ucode` release whose default code-scanning suite
contains at least one reviewed, reusable check and emits a meaningful SARIF
alert on a known historical vulnerable source while discriminating its actual
fix. Keep **both** OpenVPN and Tailscale vulnerable/fixed matrices as release
regressions, even if one remains in a separate explicit regression suite until
its semantics and performance warrant default promotion. Extract every
expected file exactly once. A clean Linux job
in `codeql-openwrt` must pin that producer release, execute it against pinned
source, verify exact extracted-file identities and alert rule/URI/range, and
consume the **fresh** SARIF. The cases may require separate narrow queries:
OpenVPN is direct missing argument quoting; Tailscale has quoted values within
an outer double-quoted `/bin/sh -c` command. Do not promote the existing
testing-tagged `ShellInjection.ql` merely because it emits candidate rows.

The first internal release track has three tickets, each with a reviewable exit
artifact. Passing them proves a narrow historical regression and downstream
handoff; it does **not** make the scanner ready to recommend to OpenWrt
maintainers:

| Ticket | Owner lane | Exit artifact and acceptance |
|---|---|---|
| R1: historical checks | `codeql-ucode` query/model | Two exact vulnerable/fixed matrices with source-derived controls, extraction and AST identity receipts, location-bearing query output, and reviewed security semantics. A missing alert, unexplained extra, or vacuous fixed-negative leaves this ticket open. |
| R2: producer release | `codeql-ucode` default suite and Linux CI | Pinned CodeQL/toolchain and pack/release identity; resolved default suite includes at least one reviewed reusable check and CI emits its known positive/fix SARIF. Both historical matrices run as release regressions with exact extraction, diagnostics and locations, whether in default or a separately named suite. |
| R3: downstream acceptance | `codeql-openwrt` Linux CI | A clean job pins the actual producer release and LuCI/package source, maps staged to installed bytes or explicitly qualifies them, runs the released default suite, checks exact file identities and a known alert/fix pair, and passes its actual fresh SARIF to the supported consumer. Retain the second historical matrix as a separate regression gate. |

The internal proof milestone requires R1–R3. A maintainer-ready MVP also needs
the current-corpus, incoming-change, alert-quality and release-maintenance
gates in Stages 6–9, plus the breadth decision in Stage 10. OpenWrt [#68](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/68)
markup reconciliation runs in parallel for accurate coverage reporting, with
its own acceptance. OpenWrt [#69](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/69)
JavaScript UCI inventory remains on its existing execution hold.
`codeql-ucode` [#54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54)
continues as broader query coverage work; R1 has its own narrow acceptance and
does not wait for a general family to be ready.

After R1–R3, continue through corpus and incoming-change gates before calling
the scanner operational for OpenWrt. A historical alert demonstrates a narrow
rule and integration path; routine CI must also establish which current source
files were scanned, how new files enter the scan, whether the run finishes
within a measured budget, and who handles findings and failures.

The producer's inspected fixture CI (`ql-smoke.yml`, `m1-extractor.yml`) pins
CodeQL 2.27.4 for focused tests. Its `ucode-queries` and `ucode-all` pack
metadata say 0.1.0, but the inspected workflows do not publish an immutable
release artifact. Existing diagnostics helpers compare expected selected files
for named smoke runs; they are useful building blocks, not a corpus runner.
The official [CodeQL CLI `v2.27.4` release](https://github.com/github/codeql-cli-binaries/releases/tag/v2.27.4)
Linux zip asset currently reports
SHA-256 `393bf92b66596141ec93baf9b483f4a350f3749916c922fed0dd63c67706047d`
in the release API. A draft Linux gate should verify those bytes before use,
then record the downloaded tool and built extractor-pack identities.
The fresh consumer inventory at clean `codeql-openwrt`
`32b0c2f9b2d2e73de2839ef4c106aa2fa2d91797` found CSV and typed JSON
handoffs, but no SARIF import/acceptance interface or producer-driven CI job.
Its existing `corpus/lock.json` pins LuCI
`b2e0be4b46ec0fd43394c081fa7c50657af14011`, not the two historical
parent/fix pairs. R3 must define and implement a separate SARIF acceptance
contract and pin its input source map; replaying a typed handoff does not
satisfy it. The upstream CI trigger is also absent.

## Merge and revision gate

At the initial planning snapshot, the two open producer PRs were
[#152, bounded markup trim CFG](https://github.com/lucas-albers-lz4/codeql-ucode/pull/152)
at `c6feb7104ca802638b1ed1ec8125633f1051be59` and
[#153, swconfig flow prerequisite evidence](https://github.com/lucas-albers-lz4/codeql-ucode/pull/153)
at `67e1529c134dd0e51525316cf660fda6e8180842`. Both reported mergeable;
their `m3-m4-smoke` checks were still in progress when inspected. This is a
point-in-time observation. Both have since merged: #152 at
`bb2edcab7bf8cfbc44aa9feab485cb6405707a5f` on 2026-11-24 00:51:55 UTC,
and #153 at `18afe771568d373088edee7a790825ee46dec9e0` on
2026-11-24 01:10:10 UTC, after their QL smoke and cargo checks passed.
The observed post-merge `main` was `18afe771568d373088edee7a790825ee46dec9e0`.
#152 changes bounded markup CFG support, not shell-flow or security semantics.
#153 records swconfig flow prerequisites without changing the production model.
Neither PR supplies an OpenVPN/Tailscale detector or downstream SARIF gate.

The pre-merge independent work included source-first controls, model-gap
inventory, an isolated OpenVPN baseline, SARIF acceptance design and
packaging/CI review. After **both** merges, fetch into disposable checkouts,
record new full heads and dirty states, inspect their exact diffs against the
selected query/model/extractor/suite/workflow contracts, and decide whether
any earlier baseline must be rerun. A merged PR does not automatically
invalidate an unrelated source oracle; an unchanged query does not imply an
unchanged extractor. Do not pin the release to a moving branch name.

## Model assignments and worker boundaries

The user's requested routes for this wave supersede the older optional model
mapping in AGENTS.md. Use `gpt-6-luna` for bounded inventories/receipts.
Security-sensitive review of Luna output and historical shell semantics goes
to `gpt-6-sol` or `gpt-6-terra`, which the user identifies as the Daybreak
capable routes. `gpt-6.2-sol` is an optional final non-Daybreak evidence or
implementation review. `gpt-6.1-terra` was selected for ordinary coordination,
run verification and integration, but an attempted worker failed before work
began with a service 403: “Daybreak isn't available for this model. Turn off
Daybreak or choose another model.” The exact `gpt-6-terra` route is not exposed
in this session's worker roster. Use `gpt-6-sol` for security review now;
record Terra execution as unavailable until a usable exact route can be
smoke-tested. Do not silently substitute a model or describe `gpt-6.1-terra`
as a Daybreak security reviewer. Record the route actually used.
An attempted `gpt-6.2-sol` final implementation reviewer for the draft Linux
gate also failed before work with a Daybreak 403; no such review is claimed.
The parent performed static checks and a bounded manual audit instead.

Parallel workers get separate disposable checkouts, stage roots, writable
databases, caches, outputs and temp paths under ignored `work/`. They may read
the same pinned Git objects and oracles, but no two heavy CodeQL jobs run
concurrently on shared resources. Keep producers' PR/CI work and OpenWrt
consumer work in separate branches/worktrees; synchronize on explicit
versioned artifacts and contract hashes. Each worker returns source identities,
commands/exits, timings, output locations and blockers for review. Reviewer
approval is about evidence and scope, not model agreement.

| Lane | Parallel preparation | Model | Handoff |
|---|---|---|---|
| H: historical security | Review advisory mechanism, affected/fixed line, `popen` semantics, quote context, preconditions, source-to-sink path, false positives and exact discriminating controls for each case. | `gpt-6-sol` now; `gpt-6-terra` only if exact route becomes available | Frozen two-case control matrix and threat/alert wording to R1. A review was performed during planning; rerun review against actual query behavior. |
| I: inventories | Verify upstream Git blobs/hashes, branch/backport and package/feed mapping; inspect current producer suite, workflows, issue ownership, PR deltas and downstream consumer contract. | `gpt-6-luna` | Mechanical receipts for H, R1–R3 and #68; independent source verification required. |
| Q: query implementation | Implement bounded source/flow/sink/quote models and tests, likely distinct treatment of the two shell contexts. | `gpt-6-sol` for security-sensitive design and implementation; `gpt-6.2-sol` for final implementation review if needed | R1 query with exact matrix; do not infer helper safety by name. |
| E: execution and integration | Run source-first matrices, resolve suite, compare exact rows/SARIF, package and wire pinned Linux jobs, verify fresh producer-to-consumer handoff. | `gpt-6.1-terra` | R1/R2/R3 receipts and reproducible Linux jobs. |
| M: markup reporting | Reconcile #68's supported/unsupported markup status with actual extraction and report semantics. | `gpt-6-luna` inventory; `gpt-6.1-terra` verification | Separate #68 PR/evidence; no dependency on shell release path. |

## Autonomous stages and stop conditions

Within each stage, workers can advance independent tasks in parallel. A failed
gate produces a documented finding and the next eligible task; it is never
relabeled as a passed claim. Do not wait idly for CI when source or contract
work can proceed.

### Stage 0 — freeze inputs and contracts, now

1. Luna records PR #152/#153 CI and merge snapshots and current producer and
   consumer heads. Inspect relevant `AGENTS.md`, build/install scripts, locks,
   default-suite resolution, SARIF export interface, and OpenWrt import/job
   contract. Map which contracts the PRs touch.
2. Luna checks the OpenVPN and Tailscale Git blobs and independent source
   oracles in ignored `work/mvp-openvpn-oracle/` and
   `work/mvp-tailscale-oracle/`; resolve package/feed revision and installed
   transformation only if the exact chain can be established. The source
   revisions remain valid test pins even if release mapping is unknown.
3. Sol security review writes the expected source/sink identity matrix **before
   output**. OpenVPN controls cover `req` binding and optional access, raw
   `cl_meta` interpolation, patched quote wrapper, quoted sibling arguments,
   and an eligible same-sink unrelated constant. Tailscale controls cover both
   login fields through `trim` → `push` → `join`, per-value quoting inside the
   outer double quote, complete-command quoting in the fix, and an eligible
   same-pattern constant command. Include helper rebinding/unknown quote
   semantics and distinct AST entities that may project to identical rows.
   Attribute OpenVPN direct RPC input and Tailscale delegated ACL/NeedsLogin
   conditions to their respective advisories; do not infer those runtime
   conditions from the static model. Check both locally defined quote helpers
   by binding and actual implementation, not by spelling alone.
4. Freeze a small acceptance manifest: four upstream Git commits/files/blobs,
   source and sink locations, controls and expected multiplicity, selected
   tool/pack/lock versions, expected SARIF rule/URI/range, and the current
   unsupported gates. A target expectation is not an observed result.

**Gate 0:** reviewer accepts source truth and controls. If package-to-installed
mapping is unavailable, record that limit; do not label staged source as an
installed image.

### Stage 1 — isolated baseline and model design

1. When its exact route is available, Terra runs parent, fix and controls in
   separate owned databases using the current pinned producer. Check exact
   routing, successful file identities, extraction errors and AST witnesses
   before interpreting empty query output. Run the current candidate query and
   resolved default suite; record all rows, multiplicity, diagnostics, timings
   and peak memory where supported.
2. In parallel, Sol designs the narrow OpenVPN receiver/local-command path
   and Tailscale collection flow and nested-shell recognition. The current
   experimental `RequestArgsAccess` requires literal `request`, so OpenVPN's
   `req` is a prerequisite gap. Tailscale begins with `request.args.form_data`
   but passes through arrays and `join`; neither case is a proven current alert.
3. Luna inventories any existing query smoke/control overlap. Use existing
   issues for broader flow ownership and avoid adding a general taint claim to
   satisfy the MVP.

**Gate 1:** baseline receipts establish what the selected producer actually
extracts and reports. A zero-row query without successful extraction and
known-positive control is inconclusive.

### Stage 2 — R1: bounded query and security review

1. Implement only the supported sources, propagation and sinks needed to make
   each vulnerable-positive/fixed-negative distinction meaningful. Keep a
   testing query until its controls pass. Query tests assert exact source/sink
   entities and locations as well as CSV/SARIF row multiplicity.
2. Sol security review challenges quote boundaries, helper binding, shell
   nesting, path assumptions, same-function false flow, branch feasibility and
   cases that pass a user value to a different command. Record any excluded
   behavior in the rule help and issue owner. Alert wording should describe a
   potentially shell-interpreted value and exact sink; a CodeQL row alone does
   not assert a reachable exploit or root execution.
3. Terra reruns fresh isolated matrices and checks that both real vulnerable
   sources alert, both actual patched sites do not, positive controls alert,
   and eligible near misses do not. Explain every unexpected extra alert.

**Gate R1:** no promotion based only on advisory text, source diff, synthetic
fixtures or matching row counts. If one case needs a second rule, keep it
separate with its own ID and controls.

### Stage 3 — R2: producer default suite and pinned Linux release

1. Add at least one proven reusable rule to `code-scanning.qls` with a clear security tag,
   stable rule IDs, sensible precision/severity and bounded help text.
2. Build a reusable Linux workflow with pinned CodeQL and repository/release
   identities. It runs extraction, checks exact successful file multiset and
   zero unexpected diagnostics, runs the resolved default suite and emits
   SARIF. Validate rule IDs, source URIs, line/column ranges and multiplicity
   on its historical vulnerable file and absence at the fixed site. Run both
   historical matrices as release regressions, whether default or separately
   named. Fail
   on query warnings that invalidate alert interpretation: the current
   seven-column `ShellInjection.ql` testing query warns that a problem query
   must select an even number of columns, despite a zero exit and decoded CSV.
3. Run focused tests and one clean hosted job. Capture command, exit, elapsed
   and memory receipts; inspect failures rather than retrying blindly. Review
   the released pack, lock and workflow artifact identities.

**Gate R2:** a downstream maintainer can pin an immutable producer release and
run one documented command/job. The suite must actually contain the rule(s).

### Stage 4 — R3: fresh OpenWrt consumer acceptance

1. Pin the released producer and the selected LuCI inputs in an isolated
   OpenWrt checkout. Record source acquisition/installation steps and compare
   staged bytes with the package source and actual installed path after any
   transformation.
2. On Linux, run the actual producer; assert exact extracted files and fresh
   default-suite SARIF rule/URI/range for a known vulnerable input and absence
   at its fix. Keep the second historical matrix as a release regression. Pass
   that output to a newly implemented, consumer-owned SARIF acceptance step
   and assert its accepted record identity. The current CSV/typed adapters do
   not consume SARIF. Its manifest must pin producer release, source commits,
   expected file multiset and exact alert tuples; its run receipt must bind
   fresh output bytes, command/exit, suite and tool identities. Replayed SARIF,
   historical CSV and source hashes do not establish this handoff.
3. Publish CI documentation naming the release pin, coverage boundary and
   expected output. Keep large raw artifacts in run storage; commit only small
   reviewed receipts.

**Gate R3:** a clean run reproduces both case alerts and the consumer result.
The new SARIF acceptance step must be checked against the actual fresh output;
offline schema tests alone do not close R3.

### Stage 5 — reconciliation and release decision

After #152/#153 merge, refresh full heads and rerun only matrices affected by
their actual changed contracts. Reconcile #68 independently. Sol security
review checks that final results support only the named two-case scope;
`gpt-6.2-sol` may perform final evidence-boundary review if the implementation
or SARIF contract warrants it. Terra verifies all R1–R3 receipts against source
and actual outputs. Update ledger claims and portfolio with demonstrated,
partial and unknown boundaries; do not turn the two cases into a coverage
percentage. Create release PRs and merge only after CI and review gates pass.

### Stage 6 — inventory the actual OpenWrt/LuCI scan universe

The first source-tree inventory is recorded in
[current-corpus-first-slice-20261124.md](planning/current-corpus-first-slice-20261124.md).
It selects LuCI `luci-base` and OpenWrt `utils/cli` as the first bounded
extraction slice. A local source-staged run selected all 21 candidates and
reported 21 exact successful-file identities with zero extraction errors;
the route probe classified 20 plain and one markup-inconclusive file. This is
neither an installed-image scan nor Gate 6 completion. The default suite
still resolves to two diagnostics and emits no security SARIF. The explicit
Tailscale candidate query exceeded 187 seconds on this small slice and was
interrupted; its cost must be addressed before corpus-scale promotion.
A second source-first
[17-file LuCI rpcd slice](planning/current-rpcd-second-slice-20261124.md)
then extracted all selected files once, recorded 17 raw-mode plain routes,
and ran the local draft suite with zero candidate results. The selected
slice has no confirmed positive, so its empty SARIF is an inventory and
performance observation, not evidence of security coverage or precision.

1. Luna inventories current ucode-bearing roots across the selected OpenWrt
   repository, LuCI and relevant feeds/packages. Record ownership, revision,
   acquisition and installation/build transformations. Distinguish `.uc`,
   extensionless installed ucode, templates, JavaScript and other languages.
   Exclude unrelated language files explicitly; do not call them scanned.
2. Terra prepares a source-derived manifest for an initial bounded corpus and
   then a broader release candidate corpus. For every intended file, record
   selected route, expected extraction status, source digest and installed path
   if known. Check extracted-success identities and errors with multiplicity.
3. Sol reviews exclusions that affect the promoted check: imported callees,
   unsupported AST/flow shapes, nested shell patterns and markup boundaries.
   Track each gap with an owner and a concrete source example.

**Gate 6:** publish a versioned coverage manifest listing selected, extracted,
errored, unsupported and excluded identities. State the exact denominator for
any counts; never infer security coverage from file counts.

### Stage 7 — measure and harden corpus-scale Linux execution

1. Run a fresh Linux scan of the selected corpus with owned databases, caches
   and outputs. Measure bootstrap, extraction, query, SARIF and consumer phases
   separately, including peak memory where supported. Check exact file and
   diagnostic identities, not just successful exit or total row count.
2. Triage new alerts against source and rule intent. Retain an immutable
   baseline keyed by commit, rule ID, source location and result identity; note
   when renames or generated paths make location unstable. Human review decides
   true issue, benign pattern, model error or unknown; do not silently suppress
   unknowns to make CI green. Record alert owner, rationale, related issue and
   expiry for any accepted exception. Keep raw SARIF alongside a small reviewed
   manifest; a line-number change needs source-diff review before classifying
   an alert as new or resolved.
3. If resource use or alert volume is impractical, reduce the explicitly named
   selected corpus or adjust the rule before broadening. A smoke duration is
   not a full-corpus estimate. Record the actual budget and platform.

**Gate 7:** one reproducible current-corpus Linux run has known selection,
performance and alert dispositions. Historical pre/post tests continue to run
as regressions. Keep the first new-alert job informational until its baseline
and failure policy are reviewed; only then consider a blocking security gate.

### Stage 8 — incoming-change CI

1. Choose the real trigger for upstream changes: a workflow in the relevant
   upstream repository, an authorized mirror/dispatch that checks upstream PR
   SHAs, or a scheduled pinned scan. Specify who owns credentials, permissions,
   SARIF upload and notifications. A `codeql-openwrt` job on its own branch
   does not cover new upstream OpenWrt or LuCI commits.
2. Start with a full selected-corpus scan for each trigger unless a changed-file
   mode is proven to retain cross-file dependencies and installed-path mapping.
   If incremental mode is later added, compare it with periodic full scans and
   explicitly report files omitted by the fast path. New files and renamed
   extensionless installed ucode must enter the manifest or fail the gate.
3. Define actionable CI states: extraction or route regression fails; tool or
   dependency failure is distinct from a clean negative; a new alert receives
   a maintainer-visible SARIF annotation or triage item; known accepted findings
   have reviewed, expiring dispositions. Do not conflate no alerts with no
   analyzed files.
   Compare disappearance of a known alert and loss of a historical positive
   as triage events too: either can indicate a model or selection regression.
4. Exercise at least one actual incoming-change test with a known alert at a
   verified source location and one clean control. Verify the job reports its
   producer release, source SHA, exact selected/extracted files, rules run,
   SARIF artifact and status in a maintainer-accessible place.

**Gate 8:** an incoming upstream change is scanned by the released check and
produces a reviewable result; failures and coverage gaps are visible to the
same maintainer. A schedule-only job can be an interim mode but does not prove
PR-time detection.

### Stage 9 — ongoing release and rule expansion

1. Pin releases in CI and update deliberately. For each producer update, rerun
   historical pre/post matrices, controls, suite resolution, current-corpus
   extraction and alert diff before changing the consumer pin. Preserve a
   rollback path to the previous working release.
2. Add new checks by named source/sink family with independently documented
   positives, eligible near misses and at least one real-source or historical
   differential case. Review false positives and missed eligible shapes using
   sampled current source, with ownership in producer issues. Do not inflate
   the two shell cases into a general vulnerability benchmark.
   Inspect selected eligible non-alerting source/sink sites for missed modeled
   patterns, with a predeclared sample and denominator. Include independent
   variants of the historical controls after the first implementation passes.
3. Periodically reconcile current OpenWrt/LuCI source inventory, supported
   routes, extraction failures, alert dispositions, resource budget and stale
   baseline entries. Track trend as counts with explicit revision/denominator,
   not a single coverage percentage.

**Gate 9:** the team has a repeatable release/update and triage process that
keeps the scanner useful as the upstream code and query pack change.

### Stage 10 — decide whether the scanner is useful enough to propose

1. Review the current source inventory with OpenWrt/LuCI maintainers' actual
   code paths in mind. Rank named security analyses by current eligible sites,
   impact and model feasibility: direct and helper-mediated shell execution,
   relevant UCI/configuration effects, request/RPC input propagation and
   package-specific command construction. This is a selection queue, not a
   claim that all such families are supported. Tie each candidate to an owner,
   source examples, expected controls and a stop condition. Preserve claim 005
   and other known unsupported boundaries.
2. Add useful breadth only where source-first evidence and controls support it.
   Each new rule family needs a current-source eligible positive or controlled
   regression on a current source shape, an eligible near miss, scoped false
   positive and missed-pattern review, default-suite/SARIF acceptance and
   downstream CI receipt. A historic fix is a strong anchor but cannot stand
   in for a current-corpus usefulness decision.
3. Run at least one incoming ucode change through the actual PR-time or
   equivalent upstream-triggered CI path, including a controlled alert and a
   clean control. Exercise a producer release update and a current-source
   update separately; verify the baseline diff, extraction inventory, alert
   disposition and rollback. Keep the trigger informational until results and
   resource behavior are stable enough for a blocking policy.
4. Prepare a maintainer-facing pilot packet only after the above passes: exact
   repositories and revisions scanned, selected and unsupported file classes,
   rule contracts, sample alerts and known limits, measured Linux cost,
   release pin/update process, ownership for triage and a clear way to turn the
   job off or roll back. Ask maintainers to consider a pilot, not to rely on an
   unmeasured claim of broad OpenWrt vulnerability coverage.

**Maintainer-ready MVP gate:** R1–R3 and Gates 6–9 pass, the Stage 10 current
source and incoming-change demonstrations pass, and the pilot packet is
reviewed. If the corpus shows too few eligible sites or the alert burden is
unmanageable, keep this as an internal prototype and continue bounded rule
work. No arbitrary number of rules or historical CVEs substitutes for this
decision.

Report each gate with its exact source/producer pin and scope: historical case
outcomes separately (vulnerable alert and fixed-site absence), controls passed
by class, expected versus extracted file identities, unexpected diagnostics,
suite rule IDs, SARIF versus consumer records, reviewed/new/unreviewed alerts,
and phase wall time/peak memory. Counts require their denominators. Neither
two historical cases nor a reviewed alert sample yields a whole-OpenWrt
sensitivity, precision or coverage percentage. Imported-callee completion,
arbitrary cross-file flow, crontab/ACL/CGI/JavaScript analysis and runtime
exploit reproduction remain separately owned work unless a later scoped rule
needs them.

## Evidence and sequencing rules

- Preserve exact full SHAs, dirty states, source/lock/tool digests, commands,
  exits, file-routing decisions, diagnostics, AST/source/sink identities,
  multiplicity, timings and peak memory where supported. Each run owns its
  database, outputs and writable caches. Do not repurpose `HOME`.
- Source-first controls are frozen before inspecting results. Malformed-input
  tests have separately declared expected extraction errors. A shell alert is
  a static finding, not a claim of runtime exploitability or authorization.
- The maintainer advisories supply historical impact evidence; this wave
  checks whether the released static analysis finds the source pattern and
  distinguishes the fixes. It does not run a live exploit.
- If a PR, exact model route, release artifact, installed-byte mapping or
  consumer interface is missing, report the specific unmet gate and advance
  independent lanes. Do not silently weaken the release criteria.

## Status through 2026-11-24

- Done as source-first preparation: the two maintainer advisories and mainline
  parent/fix Git objects were inspected; OpenVPN and Tailscale source bytes,
  digests and pre-run oracles are staged under ignored `work/`. A `gpt-6-sol`
  worker reviewed the historical security mechanism and control risks; a
  `gpt-6-luna` worker checked current PR/CI and suite status. These are planning
  results. [Claim 075](claims/075-historical-openvpn-baseline.md) then ran
  local CodeQL 2.27.4 against isolated OpenVPN parent/fix/control databases:
  exact extraction and AST witnesses passed, the existing testing query
  returned no target row on either historical source, and its positive/near-miss
  controls returned one/zero rows. This is a bounded model-gap observation,
  not a security alert, SARIF result or consumer handoff.
- [Claim 076](claims/076-historical-tailscale-baseline.md) then used the
  post-merge producer `18afe771568d373088edee7a790825ee46dec9e0` for a
  local Tailscale parent/fix/four-control run. Exact extraction and AST
  witnesses passed. The current candidate query returned no nested-path rows
  and one direct positive-control row, as predeclared. This is a second bounded
  model-gap observation, not fix discrimination or a release alert.
- Done after that snapshot: PR #152/#153 CI passed and both merged. A disposable
  checkout fetched `main` at `18afe771568d373088edee7a790825ee46dec9e0`;
  the inspected extractor metadata/schema, shell query/model and default suite
  files were unchanged from the selected claim 075 producer pin. The changed
  contracts are markup CFG/test and #54 evidence, so claim 075 remains a
  historical result at its original pin; a new run is needed for any claim
  about the post-merge producer.
- Subsequent local work produced two testing-tagged historical
  fix-discrimination rules in disposable producer branches. OpenVPN has a
  six-case 1/0/0/0/0/0 matrix at `c4829ff1`; Tailscale has a 13-file
  parent/fix/11-control matrix at `2dde7010`, and its query-plan revision
  reduced a copied 21-file query from an interrupted 187.742 seconds to
  3.196 seconds. See
  [experimental-shell-rules-20261124.md](planning/experimental-shell-rules-20261124.md).
  Neither rule is default or a reusable incoming-issue check.
- The consumer has an offline SARIF acceptance prototype at local commit
  `a6f4956` with nine passing tests, but no trusted Linux CI handoff.
  [Claim 082](claims/082-local-direct-rpc-sarif-handoff.md)
  now demonstrates a fresh local macOS draft-suite producer-to-consumer
  handoff on OpenVPN parent/fix and a pinned LuCI near miss. A first
  source-staged LuCI/OpenWrt slice selected 21 exact files,
  with one markup-inconclusive route; see
  [current-corpus-first-slice-20261124.md](planning/current-corpus-first-slice-20261124.md).
  Installed package bytes and broader selection remain unknown.
- R1's two bounded historical explicit-query matrices and security reviews
  are demonstrated locally in claims 078–079. A less source-specific direct
  handler rule and its controls are demonstrated in
  [claim 080](claims/080-final-direct-rpc-rule.md); a local draft suite and
  same-machine consumer handoff are demonstrated in claims 081–082.
  [Claim 084](claims/084-current-luci-package-ucode-slice.md) adds a disjoint
  four-file source-staged LuCI package slice with exact route/extraction
  identities, but no supported current-source security positive.
  [Claim 085](claims/085-pinned-luci-ucode-source-census.md) inventories 69
  pinned LuCI source candidates and identifies 24 remaining install-shaped
  paths after exact overlap, mostly markup templates; it is source-only
  planning, not a completed extraction census.
  [Claim 086](claims/086-current-luci-markup-shebang-route-slice.md) runs
  that 24-file source batch: two plain shebang routes and 22
  `markup_not_modeled` inconclusive routes, with exact successful extraction
  identities and zero errors. The markup status remains a coverage gap.
  Pinned Linux producer release, trusted downstream CI acceptance,
  source-to-installed-byte mapping and a working requested Terra route remain
  open. Gates 6–10 are not yet met; the
  [direct RPC shell family](planning/next-shell-family-20261124.md) remains a
  scoped review candidate, not operational incoming-issue detection.
- An additive draft Linux R2 gate is committed only in the disposable producer
  branch `mvp/direct-rpc-suite-draft` at
  `977331713b4b8b5574813bee0884245bf6db2752`. It pins CodeQL 2.27.4,
  Rust 1.100.0, source blobs, locks, grammar, query and suite bytes; its
  workflow checks the historical OpenVPN pair and a LuCI near miss through the
  default suite, plus Tailscale through an explicit regression query. Python
  syntax and `actionlint` pass. The workflow has not run on Linux or produced
  a versioned release, so R2 remains open. A separate helper-flow rule passed
  its final bounded local matrix in [claim 083](claims/083-named-helper-shell-word-experiment.md)
  but remains testing-tagged and outside the default suite.
- A separate disposable producer branch at
  `b3da1030d09096fc7016701277106696f857b974` extends that draft gate
  with a candidate Linux bundle of the built extractor and both QL packs,
  per-file provenance, an outer archive digest, safe extraction verification,
  lock-pinned dependency bootstrap and extracted-suite resolution. Security
  review found and drove fixes for an initially permissive verifier, a
  Tailscale manifest lookup error, and a post-package variable typo. Six
  focused static tests and `actionlint` now pass. No Linux run, published
  immutable release, or downstream acceptance has occurred, so R2–R3 remain
  open. The Actions artifact is a run-scoped candidate only.

## Ledger reconciliation with Security-40

The current ledger main branch already uses claim IDs 035–074 for Security-40.
This MVP batch is therefore recorded as claims 075–086. Related topics are
complementary evidence at different boundaries: Security-40 claims 041, 042
and 044 are blocked at producer `734555a9f56893e89e678cdee63028fc17ea5bc8`
(P2), where application backends were not routed. MVP claims 081 and 084–086
use source-staged installed-path candidates at producer
`78590f24ab20a69eb1ac70258a00165f453d305d` and
`977331713b4b8b5574813bee0884245bf6db2752`; they establish bounded route and
extraction observations, not full application routing or semantic security
coverage. Likewise Security-40 claims 052 and 056 concern markup escaping and
template/include argument propagation. MVP claim 086 checks route/extraction
for 22 markup-inconclusive templates and two plain shebang scripts; it does not
resolve those semantic gaps. Different producer revisions and staging
contracts mean these results do not contradict each other.
The run receipts and source-first oracles retain their original local 035–046
labels where those labels were embedded in raw evidence. Their directories,
claim pages and index links use 075–086. The raw labels are provenance for the
pre-reconciliation runs, not references to Security-40 claims with the same
old numbers; rewriting hashed receipts would obscure their original bytes.

## Active work block after claims 075–076 (historical snapshot)

1. **Producer, two isolated lanes:** develop OpenVPN's receiver/command/quote
   rule and Tailscale's collection/nested-shell rule in separate disposable
   checkouts at `18afe771568d373088edee7a790825ee46dec9e0`. Each lane
   keeps a frozen source-first matrix, runs exact extraction and source/sink
   identity checks, and reports actual vulnerable/fixed/control output.
   Security-sensitive design and review use `gpt-6-sol`; no rule is promoted
   merely because one historical row appears.
2. **Ledger:** preserve the post-merge baseline and control receipts for both
   cases, compare any proposed patch against the independently staged upstream
   bytes, and keep unsupported flow/quote semantics explicit. Claims 075–076
   are current-query observations, not vulnerability detections.
3. **Consumer contract:** specify a fail-closed
   [SARIF acceptance manifest and fresh-run receipt](planning/r3-sarif-acceptance-contract.md)
   in `codeql-openwrt`, including source-to-installed path
   mapping, exact extracted-file multiset, rule ID/URI/range/multiplicity and
   fixed-site absence. Implement its parser and offline rejection tests only
   after the actual producer SARIF shape and stable rule IDs are known. A
   synthetic SARIF test does not establish the live R3 handoff.
4. **Decision gate:** review the two producer patches independently. If one
   cannot defensibly distinguish the historical fix, retain the concrete
   prerequisite as partial and continue the other eligible lane. Once one
   scoped rule passes, resolve and test the default suite and SARIF locally;
   then prepare pinned Linux R2 and fresh consumer R3 jobs. Full-corpus and
   incoming-change work remains in Stages 6–10.
