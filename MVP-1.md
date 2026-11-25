# MVP-1: historical checks to continuous OpenWrt scanning

Initial planning snapshot: 2026-11-23 UTC; progress refreshed 2026-11-25.
The historical checks have since produced bounded local alerts, but the
Linux release and operational gates remain open. Read [AGENTS.md](AGENTS.md),
[PLAN.md](PLAN.md), [the case dossier](planning/mvp-historical-security-20261123.md)
and the relevant claims before each run. The case dossier pins source revisions,
advisories, digests, current model gaps and source-first oracles.

Current release-path checkpoint (2026-11-25): producer PR #157
merged as `b43592a8748557dae9f862644e1ddd3c5c60d5ce`. The tag-bound
publication workflow in [PR #159](https://github.com/lucas-albers-lz4/codeql-ucode/pull/159)
then passed Linux R2, Cargo and M3/M4 smoke and merged to producer `main` as
`9166af76cf6944e1b3ea5856a9176366a1f7a6ee`. Release immutability must
be enabled and confirmed before creating a version tag. The producer Releases
API currently lists no release. Consumer
[PR #154](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/154)
merged as `e3b99cd7c03ca410bba0b9bae5d9095f21b11647`; its null lock
keeps the live job skipped. Stacked
[PR #155](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/155)
prepares the 111-path Linux current-corpus stage in that same job. Its
`817c4a3` head passed hosted contract and repository tests, with live execution
skipped by the null lock. It remains draft until its live gate passes; its
retained #154 base branch and stacked dependents need reconciliation with
consumer `main`. Stacked
[draft PR #157](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/157)
advances that job's frozen manifest to
[128 paths](planning/mvp-bounded-corpus-v0.6.md). Its current head `c278312`
integrates #155's routing failure receipt with v0.6 route counts; 21 focused
tests and `actionlint` passed locally. Hosted `contract`, `lock-state`,
`unittest` and `typed-handoff` passed. The live job skipped on the null lock.
No versioned
release or R3 live handoff has occurred. The independently tested
[v0.5 local manifest](planning/mvp-bounded-corpus-v0.5.md) selects 123 paths.
An attempted [v0.6 source-staged run](evidence/mvp-corpus-v0.6-local-run/README.md)
at a newer captured OpenWrt head selected 128 paths and stopped on two
parse-failed wifi sources; it produced no suite SARIF. A subsequent refined
grammar pack extracted all 128 paths once with no errors and zero suite
alerts in a local macOS source-staged run. Neither result is an installed-byte
or released Linux Gate 6/7 result. Stacked draft
[PR #156](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/156)
prepares a manual incoming PR identity and bounded source-drift preflight;
it does not scan incoming changes yet. Producer
[PR #161](https://github.com/lucas-albers-lz4/codeql-ucode/pull/161)
adds newer grammar support and pinned native CLI provenance; Linux R2,
Cargo and M3/M4 smoke passed at reviewed head `b25bdd3` (smoke run
`45498511096`). It merged as
`104a398468f214961168d2edc9a10be45b80062f`.
Downstream
[draft PR #160](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/160)
prepares a same-job released event and clean-control scan; its offline hosted
checks pass, but both live scans skip on the null release lock.
Downstream [PR #161](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/161)
merged its manual installed-byte experiment; run `45503598387` began a
Linux build but failed in an executing dry-run probe before package
compilation. Fix PR #163 merged; manual rerun `45513606386` completed
successfully and yielded a bounded installed-byte `luci-base` receipt
documented below. Downstream
[PR #162](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/162)
adds read-only incoming discovery with no scheduled scan. A manual live
[v3 discovery snapshot](evidence/mvp-incoming-poller-live-20261124/README.md)
captured 1,651 OpenWrt and 198 LuCI open PR rows plus two default tips
across 81 successful API requests. It is discovery only; selected PR
trees and a released scan remain unresolved. Hosted `unittest` and
`typed-handoff` passed at final head `a417fb9` in run `45510746930`;
#162 merged as `cd6c5c1f8d53edf6436ba34091106e5ff0d84382`.
Producer [draft PR #163](https://github.com/lucas-albers-lz4/codeql-ucode/pull/163)
adds a bounded source-declared unary `fs.stat` model for the read-side family.
Its Linux R2 and Cargo checks passed at `93aadfe`, while M3/M4 smoke was still
running at this checkpoint. It adds no production query or default-suite rule
and does not alter the release gate.

Current execution sequence: (1) confirm the authenticated GitHub release
immutability toggle, then publish and independently verify the producer's
versioned asset; (2) fill the consumer release lock from those exact bytes
and run fresh R3 and 128-path Linux corpus jobs; (3) complete a released
incoming-event known-alert/control drill and only then consider durable
polling. The manual discovery snapshot and completed `luci-base` installed-byte
receipt do not replace steps 2–3.

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

An explicitly qualified source-staged R3 run can establish a narrow internal
producer-to-consumer pilot. It cannot satisfy the actual installed-byte
coverage required for a maintainer-ready Gate 6, even if its staged path
matches an install rule. The two-file `luci-base` IPK comparison is a
transformation check for `http.uc` and `header.ut`; it cannot establish the
128-path installed denominator or the historical OpenVPN/Tailscale package
bytes. Keep those claims separate in the final acceptance decision.

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

Use the current [AGENTS.md](AGENTS.md#model-routing) routing rule at execution
rather than treating an earlier smoke test as a permanent service result.
`gpt-6-luna` handles bounded inventories and receipts; `gpt-6.1-terra`
handles ordinary coordination and verification; `gpt-6.2-sol` is available
for difficult non-security semantics and final evidence-boundary review.
For defensive security-sensitive historical shell review, use the user's
Daybreak-capable `gpt-6-sol` or `gpt-6-terra` route, and do not silently
substitute an unavailable route. Check actual route availability for each
worker and verify its output against source and commands. A same-model
second pass is not independent-model corroboration. Do not switch
subscription/API authentication or infer billing from a model alias.

Earlier 2026-11-24 worker attempts to `gpt-6.1-terra` and `gpt-6.2-sol`
returned Daybreak 403 before work. Later separate tasks in this session
completed through both requested routes for ordinary work, so the earlier
403s are historical observations, not a current unavailability claim. The
runtime does not attest an independent server-side model ID. The
`gpt-daybreak-blue-latest` alias was tested but is not used for this plan
because the user identified its routing/cost ambiguity.

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
the route probe classified 20 plain and one markup-inconclusive file. This was
neither an installed-image scan nor Gate 6 completion. At this early pin the
default suite resolved to two diagnostics and emitted no security SARIF. The
explicit Tailscale candidate query exceeded 187 seconds on this small slice
and was interrupted. A later independent 21-file query-plan revision took
3.196 seconds at its own pin; neither timing is a full-corpus cost estimate.
A second source-first
[17-file LuCI rpcd slice](planning/current-rpcd-second-slice-20261124.md)
then extracted all selected files once, recorded 17 raw-mode plain routes,
and ran the local draft suite with zero candidate results. Claims 084–086 add
four disjoint package ucode files, a 69-path LuCI source census, and a
24-file route/extraction batch (22 markup-inconclusive templates and two plain
shebang scripts). These are source-staged observations, not installed bytes or
a completed corpus manifest. The selected
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

The [incoming CI implementation sequence](planning/mvp-incoming-ci-design-20261124.md)
defines the first explicit upstream-SHA drill, bounded scheduled discovery,
source-policy delta and fail-closed event states. It is design preparation;
draft consumer PR #156 provides a manual API-bound upstream-PR identity
preflight, and draft PR #158 adds full-tree candidate inventory to that
workflow. No scheduled trigger or released incoming-source scan exists yet.

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

**Gate 8:** a verified incoming upstream change with a known alert and an
independently checked clean control pass through the released event resolver,
full selected-corpus scanner and actual SARIF consumer. The alert's exact
source location, file/route/extraction identities and maintainer-visible
disposition must match the predeclared oracle; failures and coverage gaps
must also be visible. The clean-only PR #26933 path is a prerequisite, not
this gate. No authorized canonical-upstream known-alert event source has
been confirmed yet. A schedule-only job can be an interim mode but does not
prove PR-time detection.

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

## Historical resume snapshot before release PRs (2026-11-24)

This section records the earlier decision point; the current execution
sequence is at the top of this plan. Ledger `main` was
`13e6b0415c165070db329e178556b921803da80d`, clean when checked, with
claims 075–086 reconciled against Security-40 claims 035–074. The four remote
branch heads below were checked with `git ls-remote` on 2026-11-24; neither
project had an open PR at that earlier check. A pushed branch is not a merged change,
a Linux CI result, or a release. Fetch and recheck heads, dirty states, issue
ownership and PR/CI state before execution; the named heads are resume pins,
not moving-branch assumptions.

| Track | Repository and checked remote head | Current evidence | Next reviewable result |
|---|---|---|---|
| Producer release, critical path | `codeql-ucode` `mvp/direct-rpc-release-candidate` at `b3da1030d09096fc7016701277106696f857b974` | Reviewed direct RPC rule in draft default suite, historical regressions, pinned Linux workflow and candidate bundle verifier; focused static tests and `actionlint` pass. No hosted Linux run or immutable release. | PR and green hosted Linux gate with exact extraction, suite/SARIF, matrix, tool/pack and bundle receipts; then versioned immutable release and documented consumer pin. |
| Downstream acceptance, parallel preparation | `codeql-openwrt` `mvp/sarif-acceptance-prototype` at `ac6b03a8900770ef9c1b46ef91f81327fc36b8f1` | Parser and nine offline tests pass; claim 082 is an actual local macOS draft producer-to-consumer handoff. No released-producer Linux job. | PR adding isolated Linux acceptance workflow and manifest; fresh released-producer SARIF passed to the actual parser with exact alert/fix and file identities. |
| Historical experiments, separate from release promotion | `codeql-ucode` `security/helper-shell-word-experiment` at `3111982595ab5cc873d95db09bb0ae71057d63e8` and `security/openvpn-metadata-shell` at `c4829ff1d30225ca758b0f7979f47c3265cf882d` | Testing-tagged, bounded local matrices. Neither supplies an additional default-suite check. | Preserve as separate experimental review work; promote only after independent current-source eligibility, controls, precision and performance review. |

**Dependency and concurrency:** producer PR/CI fixes → immutable producer
release → pinned downstream Linux handoff → R3 receipt. In parallel, prepare
the consumer workflow against an explicit candidate contract, build the
source-derived corpus manifest, and inspect installed-byte transformations.
Run CPU/memory-heavy CodeQL jobs serially or on isolated runners with unique
databases, outputs, `HOME`, `TMPDIR` and caches; metadata inventory, review,
tests and CI preparation can proceed concurrently. When the release changes,
recheck the candidate contract and rerun the downstream job against the
immutable release. Local draft output cannot be substituted for that job.
When merging a PR that is the base of a stacked draft, retarget the draft
to `main` before deleting the base branch, or retain that branch until the
draft has been rebased. The #157 merge deleted #158's base and GitHub
closed #158 automatically, requiring the reviewed publication diff to be
rebased and reopened as #159. Record old and new PR/head identities so CI
evidence is not silently transferred across that change.

### Work packages for R2 and R3

1. **Producer (`codeql-ucode`):** open the candidate branch as a PR, inspect
   its delta from current `main`, and run the hosted pinned Linux workflow.
   Inspect every failure and retain phase exits/timing/memory, exact selected
   and extracted identities, diagnostics, resolved suite, historical alert
   tuples and both fixed negatives. Review the bundle manifest, archive digest,
   dependency locks and installed CLI/pack bytes. Fix the branch and repeat
   only failed or affected gates. Merge after CI/review, publish an immutable
   versioned artifact, and verify fetching that artifact by its pin and digest.
   A run-scoped Actions candidate is not this release.
2. **Consumer (`codeql-openwrt`):** while R2 runs, turn the offline SARIF
   acceptance prototype into a Linux workflow and explicit manifest/receipt
   contract. Prepare isolated source fixtures, the expected source-to-stage
   map, exact extraction multiset and known rule/URI/range tuples. Test
   malformed/missing/multiplied SARIF and extraction records fail closed. Once
   the immutable release exists, pin its version and digest, run fresh
   extraction/default-suite/SARIF, pass those same bytes to the consumer, and
   review the accepted record. The OpenVPN parent/fix is the default-suite
   known alert/control; retain the Tailscale matrix as a separately named
   release regression unless its query earns default promotion.
   The exact [R3 Linux handoff contract](planning/mvp-r3-linux-handoff.md)
   records the release lock fields, source pins, job sequence and receipt
   requirements for this work.
3. **Ledger:** record producer and consumer full SHAs, dirty states, actual
   release identity, source/corpus pins, tools, commands, exits, elapsed/peak
   memory where supported, raw-artifact hashes and normalized small receipts.
   Update R1–R3 status only from actual CI and handoff output. Review the final
   alert wording and exclusions against the historical source oracles.

### Parallel current-corpus work for Gates 6 and 7

1. **Selection and coverage (`codeql-openwrt` plus ledger):** choose a
   versioned bounded current OpenWrt/LuCI corpus first, then a larger candidate
   corpus. Inventory ucode-bearing OpenWrt core, LuCI and relevant feed/package
   roots by owner and clean full SHA. Deduplicate blobs and overlaps with
   claims 077, 081, 084–086. Record every intended source path, digest,
   extension/route, expected installed path, and inclusion/exclusion reason
   before extraction. Separate plain ucode, extensionless scripts, markup,
   JavaScript and generated or transformed files. Reconcile OpenWrt #68 so
   `markup_not_modeled` stays visible as unsupported even when extraction
   reports a successful file; keep #69's JS UCI work off this ucode release
   path until its own hold is resolved.
2. **Installed-byte provenance (`codeql-openwrt`):** inspect package build and
   install scripts before running them. For selected files, compare pinned
   source blob, staged path/bytes and actual package-installed bytes after
   transformations. Record hashes and any unmatched paths. If installation
   cannot be reproduced, qualify the corpus as source-staged and leave the
   installed-byte part of R3/Gate 6 open; do not silently rename that evidence
   an installed scan.
3. **Rule eligibility and gaps (`codeql-ucode`):** inspect current-source sites
   eligible for the promoted direct RPC rule, including the two quoted LuCI
   near misses in the 17-file rpcd slice. Predeclare a sample and denominator
   for missed eligible patterns. Track imported callees, helper-mediated
   commands, collection/concatenation, nested shells, markup and other
   unsupported flow by source example and owning issue. The helper and
   Tailscale experiments can inform this review but stay outside the default
   suite until their own controls and cost justify promotion. Do not turn zero
   current alerts into a safety or precision claim.
4. **Linux scale run (`codeql-openwrt`, after a pin is available):** use a
   fresh owned runner/database for the versioned selected corpus. Compare the
   source-first manifest against routing, successful extraction identities,
   diagnostics and SARIF with multiplicity. Measure bootstrap, extraction,
   query, conversion and consumer phases separately, plus peak memory and
   runner resources. Do not extrapolate from the 21-, 17-, 4- or 24-file
   smokes. Triage each new alert against source and rule intent; publish an
   immutable baseline keyed by source commit, rule ID, URI/range and result
   identity, with owner/rationale/expiry for accepted exceptions. Keep the
   job informational until the baseline and failure policy are reviewed.

**Exit for this work block:** R2 and R3 have clean hosted Linux receipts tied
to an immutable release; Gate 6 has a versioned exact coverage manifest; Gate
7 has one reproducible selected-corpus Linux run with measured cost and
reviewed alert dispositions. If a CI or installation gate blocks, record the
specific failure and continue independent inventory, source mapping, rule
eligibility and consumer tests. Gate 8's actual incoming-upstream trigger,
and Gates 9–10, remain later work; a passing R2/R3 job alone does not scan
incoming OpenWrt/LuCI changes.

### Execution update, 2026-11-24

- Producer [draft PR #157](https://github.com/lucas-albers-lz4/codeql-ucode/pull/157)
  opened at `b3da1030d09096fc7016701277106696f857b974` and triggered the
  hosted Linux R2 job. Run `45424329825` failed before extraction in the
  CodeQL download step: the workflow's printed SHA-256 has 63 characters
  (missing its final `d`), so `sha256sum --check --strict` rejected the line.
  This is a workflow typo, not evidence of a bad downloaded CodeQL archive.
  The corrected 64-character checksum is committed locally as `e6fb3a8` in
  the isolated producer checkout. GitHub rejected the push because the current
  OAuth credential lacks `workflow` scope for modifying `.github/workflows/`.
  An existing GitHub SSH authentication route subsequently pushed the
  prepared workflow fix; the earlier OAuth rejection is retained here as
  failure provenance, not a current blocker. A browser-editor fallback was
  unavailable because computer-use permissions were not granted in this
  session.
- Security review found that the runner accepted zero-exit CodeQL commands
  despite query warnings. A narrow warning check now allows only the known
  low-heap query-cache performance warning and rejects other CodeQL warnings
  from query/database/resolve commands. Its pure classifier passed focused
  local checks. This non-workflow fix was pushed to PR #157 at
  `177ec0eec3cf9da3807348675fb76d37298f905c`; its new Linux run
  `45425088471` still stopped at the unchanged checksum typo. The review
  also noted that the Linux gate lacks the direct-rule synthetic control
  matrix from claim 080, and that the bundled candidate is verified/resolved
  but not itself used for extraction/SARIF. Keep both as R2/R3 review items.
- [Bounded corpus v0.1](planning/mvp-bounded-corpus-v0.1.md) aggregates
  existing source-first local evidence into 76 deduplicated selected paths:
  65 LuCI and 11 OpenWrt `utils/cli`, with four explicit LuCI exclusions.
  All 76 source bytes were rehashed from clean isolated source checkouts and
  matched the prior digests. Of the selected paths, 34 have
  markup-inconclusive routes and 42 prior plain routes. This is a predeclared
  oracle for a future combined Linux run, not a fresh Gate 6 pass; actual
  package-installed bytes and packages-feed selection remain unverified.
- The direct-rule 21-fixture control matrix is now part of the producer Linux
  runner on draft PR #157. Security review identified a missing `endLine`
  comparison; it was corrected and pushed at
  `721f830` (full SHA to recheck when resuming).
  A pinned source-first manifest predeclares all fixture hashes and five exact
  positive SARIF locations; the remaining fixtures must produce no rule row.
  Focused local checks passed, but this new path has not run to completion on
  hosted Linux. The checksum fix has been rebased as a single fast-forward
  local fast-forward branch `mvp/workflow-fix-ready-2` at
  `0681a937e707929f20c244b7e58948eefe8c5198` in
  `work/direct-rpc-release-bundle-producer`.
  It also makes changes to the direct-control fixtures trigger this gate.
  The OAuth credential still lacks GitHub `workflow` scope, but the existing
  SSH route successfully pushed the fast-forward branch. At that point PR
  #157 was at `0681a937e707929f20c244b7e58948eefe8c5198`. The preceding
  run `45427905215` failed at the pre-extraction checksum step.
  Run `45431988122` then passed the workflow's archive verification but
  failed immediately in the Python runner because its own `CODEQL_ZIP_SHA256`
  constant still had the 63-character typo. That constant was corrected and
  pushed at `3b16a3b28b12ac445c65318fc889cd777d0a70ec`; its Linux run
  `45432379803` was in the source-pinned gate step when last checked. Neither
  prior failure establishes any extraction or query result.
  Run `45432379803` subsequently failed while checking the cloned grammar's
  expected dirty state: `git_output()` stripped the leading porcelain space,
  so the observed `M Cargo.toml` did not match the script's ` M Cargo.toml`.
  The script's subsequent byte check for the pinned dev-dependency edit was
  not reached. The status comparison was corrected and pushed at
  `72b3cc18028710379140b8d2b4cbeb2f33e6b126`. This earlier failure
  was before extraction; no R2 pass is claimed.
  Run `45432828278` then built the extractor and reached the first OpenVPN
  extraction diagnostic query, which exited 2. Its downloaded CI artifact
  shows that `pack install` put the eight locked dependencies under the
  run-owned `HOME/.codeql/packages`, while the query's separate
  `--common-caches` path had no packages. The runner now copies the installed
  pack cache into each case-owned common cache before query execution; that
  fix was pushed at `2e32670eaa62a110384a8fa3c906e568248a1823`.
  Linux run `45434365301` then reached the first OpenVPN default-suite
  analysis, but failed when the runner tried to hash `trap/ucode/routing.json`
  after database finalization removed it. The runner now retains the checked
  route receipt before finalization and hashes that copy. This fix was pushed
  at `c79a37a`. [Linux run `45435176723`](https://github.com/lucas-albers-lz4/codeql-ucode/actions/runs/45435176723)
  passed. The downloaded artifact contains 104 recorded commands with exit 0
  and peak RSS, a verified bundle SHA-256
  `65c0367440daff9ba965af7cbf9b0643afd0cf7908fd81fe47b1f6c5b46b3691`,
  three exact default-suite source identities and zero extraction errors. Its
  OpenVPN parent has one `ucode/m4/direct-rpc-shell-word` result at line 71,
  UTF-16 columns 115–132; the fixed case has zero. The 21-file direct control
  matrix has five expected results, and the separate Tailscale regression has
  one parent candidate and zero fixed candidates. This is a passing R2
  candidate on PR head `c79a37a08e05567249b3a928b14527133ddbfd4e`;
  the PR checkout used GitHub's synthetic merge commit
  `f5afea857b1a469ac94c0fa58d446e2320dbab54`. The bundle still declares
  `artifact_kind: ci-candidate`; PR review, all checks and an immutable
  release remain open. A security review then found that the Tailscale
  regression checked the rule descriptor and location tuples but not each
  result's rule ID, location multiplicity or end line. That validator and a
  stale workflow-status sentence were corrected at `3ba4fd7`; the passing
  run above predates this change. Linux run `45436961181` reached the
  Tailscale parent validation and failed because CodeQL omitted `endLine` for
  its single-line SARIF region. The check now treats absent `endLine` as
  `startLine` but rejects a differing explicit end line; this was pushed at
  `7c62553`. [Linux run `45438052249`](https://github.com/lucas-albers-lz4/codeql-ucode/actions/runs/45438052249)
  passed on that head. Its downloaded receipt records 104 zero-exit commands,
  the expected OpenVPN parent/fix results, five direct-control results,
  separate Tailscale parent/fix results and exact extraction identities. The
  archive hash matched the receipt and its 290 manifested files passed the
  producer verifier. The [reviewed-head evidence index](evidence/mvp-r2-linux-reviewed-head-20261124/README.md)
  records ten raw artifact hashes. The [earlier candidate](evidence/mvp-r2-linux-candidate-20261124/README.md)
  remains distinct. PR #157 was marked ready for review. Its M3/M4 smoke
  check later passed in [run `45438052136`](https://github.com/lucas-albers-lz4/codeql-ucode/actions/runs/45438052136)
  and it merged to `main` as
  `b43592a8748557dae9f862644e1ddd3c5c60d5ce` on 2026-11-24.
  Neither Actions artifact is an immutable release.
  [Draft producer PR #158](https://github.com/lucas-albers-lz4/codeql-ucode/pull/158)
  is based on #157 and prepares a tag-bound two-job release workflow and
  versioned bundle verifier at `97513f6`, with a publication-boundary
  tag-policy recheck at `6437022`. Static bundle tests and
  `actionlint` pass locally. Repository tag ruleset `28002678` was created
  active for `refs/tags/v*`, blocking tag update and deletion while allowing
  initial creation. `main` has no branch protection, and the immutable-release setting
  has not been confirmed. The GitHub REST repository response and GraphQL
  repository/update input do not expose that setting; the available Playwright
  import also failed, so no settings-page observation is claimed. The workflow requires an explicit repository policy
  variable and checks the published release's `isImmutable` field. Review,
  hosted validation, protective settings and an actual release still remain.
  Its [R2 run `45441384349`](https://github.com/lucas-albers-lz4/codeql-ucode/actions/runs/45441384349)
  passed on the PR merge ref: the downloaded candidate has 104 zero-exit
  commands, matching outer archive digest, one OpenVPN parent alert, zero
  fixed alert, and the expected separate Tailscale matrix. This validates
  candidate packaging on the #158 diff; the tag-triggered publication job has
  not run and the PR's M3/M4 smoke remains pending.
  After the policy recheck commit, [R2 run `45443972721`](https://github.com/lucas-albers-lz4/codeql-ucode/actions/runs/45443972721)
  also passed on #158's new head; its Cargo check passed and smoke remains
  live. GitHub's [immutable-release guidance](https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases)
  says the repository setting must be enabled before publication and applies
  only to future releases. That setting still awaits confirmation; no tag is
  created.
  When #157 merged and its feature branch was deleted, GitHub automatically
  closed draft #158 because that branch was its base. GitHub would not change
  the base of a closed PR. The two publication commits were rebased onto the
  verified merged `main` SHA, retested (seven bundle tests, `actionlint` and
  diff whitespace), and pushed with an exact force-with-lease. Replacement
  [draft PR #159](https://github.com/lucas-albers-lz4/codeql-ucode/pull/159)
  now targets `main` at `91e22839092c697843f40dd37ca795a036e49ebf`.
  Its diff has only the intended release workflow, bundle/verifier code,
  tests and documentation. Its [fresh R2 Linux run
  `45453107382`](evidence/mvp-r2-linux-main-pr-20261124/README.md) passed
  on that head; the downloaded candidate bundle and 104 zero-exit commands
  were independently checked, with exact OpenVPN parent/fix and Tailscale
  regression results. Cargo passed. M3/M4 smoke passed in 1h0m44s. PR #159
  merged at `9166af76cf6944e1b3ea5856a9176366a1f7a6ee` on 2026-11-24,
  and producer `main` matched that SHA afterward. Its Git tree
  `2ca7459e0f1198303d3eeafff90c3a6697208413` exactly matches the
  reviewed PR head tree. No version tag or release
  exists yet. The repository's release-immutability setting still needs
  confirmation before the publication workflow can be exercised. A fresh
  remote check found `v0.1.0` unused; active tag ruleset `28002678` blocks
  update/deletion of `refs/tags/v*`, while the required
  `RELEASE_POLICY_CONFIRMED` repository variable remains absent. The tag
  ruleset does not itself establish immutable release assets.
  The
  [R3 release-lock pin procedure](planning/mvp-r3-release-lock-pins.md)
  records how to derive each consumer field from the eventual immutable
  release and independent downloaded bytes. A bounded field inventory
  clarified which lock values remain fixed consumer policy, that `SHA256SUMS`
  is an extra independent comparison rather than an R3 runner input, and
  which runtime release and suite checks the populated lock must pass.
- Consumer [PR #152](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/152)
  opened at `ac6b03a8900770ef9c1b46ef91f81327fc36b8f1` to run hosted
  checks on the strict offline SARIF parser. Both hosted `M2 policy` jobs
  passed in run `45427709901` on an earlier head.
  The PR now also contains a source-first OpenVPN parent/fix oracle at
  `3a21981`, with independently checked LuCI commit:path blobs, source hashes,
  stage identities, exact rule/descriptor expectations and one parent SARIF
  tuple. It intentionally leaves producer release identity unset and does
  not claim package-installed bytes. Ten focused parser tests pass locally;
  the new head's hosted `typed-handoff` and `unittest` jobs both passed in
  run `45441997127`. PR #152 merged as
  `a1c9875575814329e5abdc70bc36e30f5ef0b987` on 2026-11-24. The
  released-bundle Linux R3 job was not part of that merge.
  [Consumer PR #154](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/154)
  prepared that job at `745f28f` and merged as
  `e3b99cd7c03ca410bba0b9bae5d9095f21b11647` on 2026-11-25. Its lock has
  null release pins and fails before network use; PR CI runs 13 offline
  contract tests while fully null, rejects partial pins, and runs live R3
  once all pins are filled. It verifies the immutable release, exact
  producer/CodeQL/source identities, separate fresh databases, routing,
  diagnostics, SARIF and same-job consumer acceptance. Local tests and
  `actionlint` pass. Hosted run `45444889701` passed `contract` and
  `lock-state`; its live `released-openvpn-pair` job was correctly skipped
  because all release pins are null. The repository's `typed-handoff` and
  `unittest` jobs also passed on this PR head. Before merge, the exact PR
  head was merged with then-current consumer `main` in a disposable checkout;
  13 focused tests, `actionlint` and diff checks passed on the combined tree.
  The stacked #155 base branch was retained. No release or live R3 result
  exists yet.
  This is parallel R3 preparation, not a released-producer Linux
  handoff; an actual pinned release and fresh job remain required.
  Stacked [draft consumer PR #155](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/155)
  now targets #154's retained branch at `817c4a301f4710cff6f0018c1b8fd3321f0b3b66` (initial implementation
  `e9c0b487fb44446cbbc2252573737047636ac4e1`, followed by a
  post-handoff symlink guard and a per-file coverage manifest).
  It adds the frozen 111-path v0.4 source oracle and a second stage in the
  same released-producer Linux job: independent source checkouts, stage,
  database and cache; exact route/extraction checks; fresh default-suite
  SARIF passed to the strict consumer with a zero-result baseline. It writes
  `out/coverage-v0.4.json` with each selected, extracted,
  markup-inconclusive and excluded identity and pins its hash in the receipt.
  A new Linux alert fails for review. The latest commit retains the raw routing
  report in the job artifact even when database indexing fails after writing
  it or route validation rejects it; two focused tests exercise those failures.
  Local 21-test contract suite and `actionlint` pass, and Sol review found no
  high-confidence false-pass. Hosted run `45527919355` passed `contract` and
  `lock-state`; run `45527919477` passed `typed-handoff` and `unittest` on the
  exact latest head. The live corpus job correctly skipped while the release
  lock is null. PR #155 remains draft, with its own acceptance criterion
  requiring a live Linux gate before it is ready to merge. Its retained base
  branch and stacked #156/#157 must be reconciled when that gate is available.
  A disposable replay on 2026-11-25 cherry-picked #155's four exact commits
  (`e9c0b48`, `7cdcba9`, `82c4aef`, `817c4a3`) onto consumer `main`
  `e3b99cd7c03ca410bba0b9bae5d9095f21b11647` without conflict. The
  resulting private head `1bdbd18` passed 21 focused tests, `actionlint` and
  `git diff --check`. This establishes a feasible replay path, not hosted CI
  or a reason to rewrite the branch while #156/#157 depend on its old graph.
  Neither draft proves Gate 6/7 until the immutable release lock is filled
  and the actual Linux job passes.
- The [current direct-rule eligibility census](planning/mvp-direct-rpc-current-eligibility.md)
  fixes the 17-file LuCI rpcd source denominator at LuCI
  `b2e0be4b46ec0fd43394c081fa7c50657af14011`. Its exact 24-site
  path/line table has two quoted `swconfig` near misses, no supported raw
  direct-field positives, nine fixed literals and 13 unsupported helper or
  assembled-command forms. This is source inspection, not a new CodeQL run
  or a safety/precision result. The next bounded claim needs exact AST
  witnesses and a raw sibling positive control.
  [Claim 087](claims/087-current-luci-quoted-switch-ast.md) now supplies that
  bounded follow-up: a fresh isolated local database extracted the pinned
  current LuCI `luci` file and synthetic controls exactly once with zero
  errors; two distinct quoted AST source/substitution/template/sink witnesses
  appeared at lines 343 and 400, and the eligible raw sibling produced one
  exact SARIF alert while the quoted sites did not. The synthetic quoted
  `other` field is excluded by the testing witness's `switch` filter; it is
  not an independent direct-rule field guard. This
  remains source-staged local evidence, not installed-byte, release or
  incoming-change coverage. A separate Sol review checked source hashes,
  entity multiplicity, the fixture's returned methods-table shape and exact
  SARIF; it corrected the control interpretation above.
- [Bounded corpus v0.2](planning/mvp-bounded-corpus-v0.2.md) now records a
  source-first 93-path denominator: the prior 76 paths plus 17 conditional
  wifi-scripts Ucode paths under `CONFIG_WIFI_SCRIPTS_UCODE=y`. The corrected
  route oracle yields 59 plain and 34 markup-inconclusive paths. An isolated
  clean-checkout verifier matched all 93 source hashes and Git blobs and five
  excluded identities. A [fresh local macOS aggregate run](evidence/mvp-corpus-v0.2-local-run/README.md)
  matched all 93 routes and successful extraction identities exactly, with
  zero errors and zero current-suite SARIF results; its nine phase times sum
  to 23.106 seconds, without peak RSS. This prepares a single
  released-producer Linux run; it is not Gate 6/7 completion or a security
  negative. Actual installed bytes and the rest of core/packages-feed
  candidates remain open.
- [Bounded corpus v0.3](planning/mvp-bounded-corpus-v0.3.md) adds six OpenWrt
  `unetmsg` files under the pinned package copy rule. A fresh isolated
  [99-file local run](evidence/mvp-corpus-v0.3-local-run/README.md) matched
  all 65 plain and 34 markup-inconclusive route decisions and all 99
  successful-file identities exactly, with zero extraction errors and zero
  default-suite results. Its nine phase times sum to 24.637 seconds without
  peak RSS. This is a larger source-staged denominator; Linux execution,
  actual installed bytes and remaining package candidates are still open.
- [Bounded corpus v0.4](planning/mvp-bounded-corpus-v0.4.md) adds 12
  packages-feed base `prometheus-node-exporter-ucode` files, with eight
  separately packaged optional collectors excluded. Its source-first
  111-path oracle passed a [fresh local aggregate run](evidence/mvp-corpus-v0.4-local-run/README.md):
  76 plain and 35 markup-inconclusive routes, 111 exact successful-file
  identities, zero errors and zero current-suite SARIF results. The nine
  phase times sum to 24.641 seconds, without peak RSS. Installed bytes,
  Linux cost and broad package coverage remain unverified.
- [Bounded corpus v0.5](planning/mvp-bounded-corpus-v0.5.md) adds 12
  recipe-mapped OpenWrt sources to the prior 111-path selection, for 123
  selected sources and 13 explicit exclusions. Its first local attempt
  stopped on two incorrect route reasons before finalize; pinned source
  shebangs explained the mismatch, and the corrected oracle was frozen before
  a new run. The [fresh macOS source-staged receipt](evidence/mvp-corpus-v0.5-local-run/README.md)
  records 88 plain and 35 markup-inconclusive routes, all 123 exact
  successful identities once, zero extraction errors and zero default-suite
  SARIF results. Nine phase times sum to 46.868 seconds (39.423 seconds for
  suite analysis), with no peak RSS. This does not establish installed bytes,
  a Linux Gate 6/7 run, or broad OpenWrt coverage.
- [Bounded corpus v0.6](planning/mvp-bounded-corpus-v0.6.md) moves the
  OpenWrt pin to the captured PR #26933 head and reviews the five candidates
  unresolved by v0.5. Source rehash found 29 changed previously selected
  OpenWrt files and one changed excluded shell file across the old and new
  pins. The first [128-file local run](evidence/mvp-corpus-v0.6-local-run/README.md)
  matched all route decisions but failed exact extraction: 126 successful
  identities and four parse diagnostics across `lib/wifi/mac80211.uc` and
  `usr/share/ucode/wifi/utils.uc`. It stopped before default-suite analysis,
  so there is no v0.6 SARIF result. This is a concrete extractor coverage
  gap at the newer source pin; installed-byte and Linux gates remain open.
  The [pinned grammar investigation](planning/mvp-ucode-newer-wifi-parse-gap-20261124.md)
  identifies its known dynamic `import()` and exported-function semicolon
  boundaries, with focused controls and AST implications for a producer fix.
  A patch still needs its own grammar, producer and exact-source regression
  run before the v0.6 corpus can pass.
  A [disposable grammar prototype](evidence/mvp-wifi-grammar-prototype-20261124/README.md)
  now builds and passes 244 plain, 89 markup and 151 documentation corpus
  cases. Its generated parser accepts both exact failed sources and two
  controls. Producer AST/schema integration and CodeQL extraction remain
  unverified; the failed v0.6 receipt is still the current producer result.
  A [focused disposable producer probe](evidence/mvp-wifi-producer-prototype-20261124/README.md)
  compiled the modified grammar and regenerated the database schema and QL
  AST bindings. Its fresh four-file CodeQL database extracted both previously
  failed wifi sources and two controls once each with zero errors; AST queries
  found the dynamic import and semicolon-free exported function at their
  source locations. This is a local override, not merged producer behavior;
  release regressions still need testing. A fresh
  [128-file local prototype run](evidence/mvp-corpus-v0.6-prototype-local-run/README.md)
  matched all exact routes, extracted each selected source once with zero
  errors, and resolved the three-query default suite. SARIF contained zero
  results on this bounded current-source set. This is macOS source-staged
  modified-grammar evidence; merged producer bytes still fail on the two wifi
  files, and Linux, installed-byte and release gates remain open. The local
  producer `cargo test --offline --locked` regression also passed 12 unit,
  three grammar-load and one doc test against the modified checkout.
  The separate [direct-RPC control matrix](evidence/mvp-grammar-direct-controls-20261124/README.md)
  also passed under the prototype pack: 21 exact fixture identities extracted
  once, zero errors and five exact expected SARIF locations. Fresh
  [historical real-source regressions](evidence/mvp-grammar-real-source-regressions-20261124/README.md)
  under the same local override also passed: OpenVPN parent one exact default
  suite alert and fix zero; Tailscale parent one exact separately named query
  candidate and fix zero; 11 Tailscale controls produced the one declared
  positive and no near-miss results. These were macOS modified-grammar checks
  before producer PR #161 merged; they do not establish a released Linux
  corpus run.
  The producer's `clone-grammar.sh` still pins upstream grammar commit
  `4a243af329fae2f4ff01e0fc80133cbab8314600`; its Linux release gate
  checks that the grammar checkout differs only by the documented Cargo
  dev-dependency adjustment. The prototype therefore cannot be promoted by
  copying its generated pack alone. The then-required step was to land the grammar source, corpus
  cases and generated parser/node-type changes in a reviewable grammar
  revision (or explicitly pin and verify an equivalent producer-owned patch).
  Then update the producer grammar pin, generated dbscheme/QL AST bindings,
  release-gate grammar identity checks and exact wifi positive/near-miss
  regressions together. The later producer PR #161 did land and pass a Linux
  candidate R2 gate; the full v0.6 Linux corpus remains pending on a
  versioned release.
  A [disposable producer-owned integration checkout](evidence/mvp-producer-grammar-integration-20261124/README.md) under
  `work/producer-grammar-integration-20261124/producer` now applies a
  source-only patch to the pinned grammar and regenerates parser outputs.
  Upstream grammar main `f177807675c9e6996c9368f74ee75e70cd0728a0`
  differs from the pinned grammar only in documentation, so it does not
  supply these syntax forms. The integration patch preserves the existing
  explicit-semicolon export tree while adding the semicolon-free form;
  its local grammar corpus (244 plain, 89 markup, 151 docs), producer unit
  suite (12 extractor, three grammar-load, one doc), bootstrap test and
  seven bundle tests passed. The release-gate draft verifies the source
  patch, regenerated parser hashes, and archived-versus-built QL schema;
  candidate and publication bundle metadata carry an effective grammar
  fingerprint. A refined-pack v0.6 corpus and historical regression rerun
  were required before a producer release. Producer
  [PR #161](https://github.com/lucas-albers-lz4/codeql-ucode/pull/161)
  introduced the pinned grammar patch and Linux gate changes. The
  [refined-pack v0.6 local run](evidence/mvp-corpus-v0.6-refined-local-run/README.md)
  now passed all 128 exact routes and extraction identities with zero errors
  and zero default-suite results. The refined pack also passed the separate
  [historical parent/fix and control rerun](evidence/mvp-grammar-refined-historical-regressions-20261124/README.md)
  at exact OpenVPN and Tailscale SARIF locations. Both remain macOS
  source-staged evidence; released Linux corpus and installed-byte gates remain open.
  The producer release-gate work included a
  [plain and markup typed AST smoke](evidence/mvp-grammar-syntax-smoke-20261124/README.md):
  both fixture files extracted once, and five projected dynamic-import and
  exported-function rows matched exact source locations. The release-gate
  function itself passed locally through a macOS wrapper; hosted Linux CI
  first ran it in [PR #161's earlier R2 candidate gate](evidence/mvp-producer-pr161-linux-r2-20261124/README.md).
  That source-pinned Ubuntu job passed both historical parent/fix matrices,
  direct and Tailscale controls, the new syntax fixture and candidate bundle
  verification at its synthetic merge checkout. PR #161's Cargo check and
  M3/M4 smoke also passed; smoke took 57m12s in run `45488088107`.
  Final diff review found that npm's locked Tree-sitter wrapper downloaded an
  unpinned native CLI. PR #161 commit `b25bdd3` disables npm install scripts,
  verifies the native archive SHA-256 before extraction, and checks the Linux
  executable digest before its first release-gate invocation. A fresh macOS
  ARM64 bootstrap passed all 484 grammar cases and reproduced six generated
  digests; an invalid-archive control failed before npm or CLI execution.
  Seven bundle tests and shell syntax passed. The final exact-head
  [Linux R2 receipt](evidence/mvp-producer-pr161-final-linux-r2-20261124/README.md)
  independently records run `45498511187` at `b25bdd3` and clean synthetic
  merge `7aba3e7`: 116 zero-exit commands, exact OpenVPN and Tailscale
  parent/fix/control results, one plain and one markup syntax success, and a
  verified `ci-candidate` bundle. Cargo and M3/M4 smoke also passed at
  `b25bdd3`; the PR merged as `104a398`. This does not transfer the earlier
  `d39b1e1` receipt to the final head. A versioned release, installed-byte
  mapping and downstream acceptance are still open.
- Stacked downstream [draft PR #157](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/157)
  advances #155's same-job Linux current-corpus gate from the frozen v0.4
  manifest to the source-first v0.6 manifest. It pins the captured OpenWrt
  PR #26933 head and checks 128 selected identities, 13 exclusions, 93 plain
  routes, 35 markup-inconclusive routes, exact extraction multiplicity, zero
  extraction errors, resolved suite IDs and consumer-accepted SARIF. The
  manifest digest is `9c004ed477665f6567a071eac45051445c61019af927bfa4e51bae4c50ebd490`;
  19 downstream contract tests passed locally at the earlier `36a4f6e` head.
  After #155's routing-report fix, replaying that head onto #155
  `817c4a3` exposed one conflict in `tools/current_corpus_linux.py`: the old
  inline route check had 128/93 v0.6 counts while #155's new retained-report
  helper still had 111/76 v0.4 counts. The reviewed resolution keeps the
  retained-report helper and sets its expected counts to 128/93. Draft PR
  #157 was updated to `c278312e59e5fafc891bac2777e50bee0bc9d9f3`,
  directly atop #155's current head; 21 focused tests, `actionlint` and diff
  checks passed locally. Fresh hosted `contract`, `lock-state`, `unittest` and
  `typed-handoff` passed on that head. The release
  lock remains null, so PR CI cannot yet perform the released Linux handoff or
  v0.6 scan.
- The [remaining packages-feed install inventory](planning/mvp-packages-feed-install-mapping-20261124.md)
  reconciles all 25 candidates outside v0.4: 22 product sources and three
  test mocks. It separates eight optional exporter collector packages from
  base-package selection and identifies two rewritten installed files
  (`adblock-fast.uc` and `librespeed-aggregate`) that require actual
  package-byte comparison. This mapping is source-rule evidence only.
- A separate Sol read-only review identified
  [WOL command assembly](planning/mvp-next-wol-assembly-check-20261124.md)
  as the strongest next bounded query candidate after the release gate. Its
  current source has request-derived expressions in an assembly that calls
  `map(shellquote)`, `join` and `popen`, with a fixed-executable guard and
  quoted arguments. Binding identity and data flow across those expressions
  are still unproved. Treat that
  source as an alert near miss and require an unquoted synthetic sibling,
  exact AST identities, reviewed flow/quote semantics and fresh SARIF before
  considering a new check. Open ucode #54 and #50 own the broader model work.
- [Claim 088](claims/088-current-luci-wol-assembly-ast.md) completed the
  source-staged AST prerequisite at clean LuCI
  `b2e0be4b46ec0fd43394c081fa7c50657af14011` and producer
  `977331713b4b8b5574813bee0884245bf6db2752`. Its testing query found
  the real WOL line 41–42 assembly and an unquoted synthetic sibling, with
  nine distinct entity ranges per row; three eligible synthetic near misses
  produced no row. Both staged files extracted once with zero errors. This
  establishes syntax identities only. The local diff from that producer SHA
  to merged `b43592a8748557dae9f862644e1ddd3c5c60d5ce` changes no `ql/src`
  file; the changes are release tooling, workflow, docs and one query test
  expectation. Before query implementation, resolve binding and flow through
  `map`/`join`, model quoting and the fixed-executable guard, and test fresh
  SARIF with positive and near-miss controls. No WOL alert is ready for the
  default suite.
  A later [testing-only WOL binding table](evidence/mvp-wol-assembly-bindings-20261124/README.md)
  on clean producer `104a398468f214961168d2edc9a10be45b80062f`
  expanded that prerequisite: 21 source-staged files were routed and
  extracted once each with zero diagnostics; the real WOL handler and three
  discriminating controls yielded four expected rows with 12 distinct AST
  ranges each, and 17 further controls yielded no row. It independently
  labels the quote-body shape and fixed-path comparison. The exact 10-command
  run took 15.356 seconds; peak RSS was unavailable. This is bounded
  binding/assembly evidence, not reusable `map`/`join` flow, quote safety,
  a production alert, SARIF acceptance or consumer handoff. Keep #54 and #50
  as the production-model owners.
  A subsequent [testing-only unquoted WOL rule candidate](evidence/mvp-wol-unquoted-rule-candidate-20261125/README.md)
  ran on 22 source-staged files at the same producer/LuCI pins. All extracted
  once with zero errors. Its exact BQRS and SARIF results were the synthetic
  identity callback at line 7 and that callback with WOL's fixed-path source
  comparison at line 42; the real quoted WOL source and 19 controls produced
  no result. The query uses narrow spelling and lexical exclusions, leaves
  partial quoting unclassified, and its testing SARIF lacks severity metadata.
  This does not justify default-suite promotion or a vulnerability claim;
  resolved callback identity, flow/quote semantics and a real consumer
  acceptance step remain under #50/#54.
  A [testing-only resolved-callback follow-up](evidence/mvp-wol-resolved-callback-rule-20261125/README.md)
  added an experimental shared `FunctionDeclaration` variable binding in a
  disposable producer. On a new 22-file database it retained the two exact
  synthetic SARIF results and zero real-WOL/control results, while a separate
  five-row audit distinguished the callback shadow and write cases. Luna
  checked exact stage, route, extraction, BQRS, SARIF and receipt identities.
  Review found same-scope binding ambiguity and missing function-value flow
  integration in the shared model. The patch and query remain evidence only;
  production-model regression controls and downstream acceptance are still
  needed before a producer PR or suite decision.
  A [33-file function-binding regression matrix](evidence/mvp-wol-function-binding-regression-20261125/README.md)
  compared baseline, broad patch and narrower prototype on fresh extraction:
  exact matrix rows were 5/15/11, all 33 files extracted once with zero
  errors, and three existing Variable/flow/SSA query tuple sets were unchanged
  on this slice. The narrow prototype removes the measured duplicate bindings
  but suppresses some valid declaration-order cases under Ucode's permissive
  redeclaration semantics. It also leaves forward declarations, imports,
  same-body formal collisions and function-value flow unreviewed. This is a
  stop condition for shared-model promotion, not a production-ready fix.
- Stacked draft consumer [PR #156](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/156)
  (`mvp/incoming-ci-drill` at `3a2197c`, based on #155) now has
  a manual incoming-event **identity preflight** on top of PR #155. It
  requires an explicit full PR head SHA and clean control SHA, captures the
  upstream GitHub pull response, binds its open PR/base/head identities to
  the fetched `refs/pull/<number>/head` checkout, and records commit/tree
  identities. Thirteen local resolver tests and `actionlint` pass. This
  branch had not yet been pushed at that stage or run in Linux CI; it did not discover changed
  source candidates across the full tree, run CodeQL or pass SARIF to the
  consumer. Its bounded drift report rehashes the v0.4 identities at the
  event commit, compares the exact API base and head trees despite shallow
  checkouts, and flags new or removed candidate paths and selected-owner
  package policy changes for review. It records ordinary source edits and
  unrelated package policy edits without treating them as coverage failure.
  The later 22 local tests cover shallow history, source edits and package scope;
  `actionlint` and diff checks pass. The branch was pushed by the authorized
  SSH route after HTTPS rejected workflow changes for missing OAuth `workflow`
  scope; the draft PR's `typed-handoff` and broad `unittest` hosted checks
  passed in run `45463203926`. The unittest log includes the incoming PR
  resolver and shallow-checkout drift regression among 1,107 policy tests.
  The manual dispatch workflow itself has not
  run in hosted CI. Full
  dynamic selection remain open. Gate 8 remains open. Keep #155's base branch
  until #156 can be retargeted after the release-backed R3 and corpus gates.
  A [local live PR identity smoke](evidence/mvp-incoming-pr-identity-20261124/README.md)
  then used OpenWrt fork PR #26933: its captured API head matched a fresh
  `refs/pull/26933/head` checkout, and a separate pinned control checkout
  matched its recorded tree; both were clean. A fresh bounded drift report
  against the API base SHA exited 0 with 34 selected OpenWrt identities, 22
  historical content changes, zero candidate path drift, and an unrelated
  bzip2 Makefile change explicitly reported. This validates the resolver and
  bounded drift logic on one real PR, not a hosted workflow or source scan.
  The [full-tree dynamic selector design](planning/mvp-dynamic-ucode-discovery-design-20261124.md)
  defines the next Gate 8 implementation: enumerate candidate signals and
  install-recipe mappings at both base and head, classify every identity as
  selected, excluded or unreviewed, stop on unresolved coverage, and scan
  ordinary edits to reviewed selected files. Its counts are inherited from
  existing pinned inventories; it is a design, not executed coverage.
  A full-tree selector prototype at `453da0d` tested that direction on
  the exact OpenWrt PR #26933 base/head pair and pinned LuCI source. The
  [portable inventory summaries](evidence/mvp-full-tree-inventory-20261124/README.md)
  record 52 OpenWrt candidates (34 selected, one excluded, 17 unreviewed),
  so the OpenWrt event fails closed; LuCI had 69 candidates (65 selected,
  four excluded) with none unreviewed. Seven focused controls pass. The
  prototype does not infer install recipes, run CodeQL or
  establish Gate 8. The 17 OpenWrt identities need review and policy
  disposition before this selector can feed an event scan. A second inventory
  at the exact v0.4 OpenWrt pin found 47 candidates: 34 selected, one excluded
  and 12 unreviewed; the other five later-PR paths did not exist at that pin.
  Stacked downstream [draft PR #158](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/158)
  now carries the bounded selector, pinned v0.5/v0.6 manifests, and a check
  that the parsed policy matches its pinned bytes. Twelve local selector
  controls passed. A fresh invocation against the captured OpenWrt PR
  #26933 base/head pair classified 52 candidates at each revision, with 51
  selected, one excluded and none unreviewed at the head. This is source
  candidate inventory, not a released event scan; #158 stacks on #156 and
  will need shared v0.6 manifest reconciliation with parallel #157.
  A follow-up commit in #158 wires that inventory into the manual incoming
  event workflow after API-bound PR identity and bounded source drift checks,
  retaining the candidate report even on failure. Local `actionlint`, 14
  event resolver tests and 12 selector tests pass. The manual workflow has
  not been dispatched in hosted CI; it still does not run CodeQL or hand off
  SARIF. A further #158 commit added a PR-triggered contract job for those
  controls; the hosted contract job passed in run `45491468225` at head
  `c6bd826`. The manual resolver job was correctly skipped on the PR event.
  The next Gate 8 code step is a separate source-first event manifest from
  the reviewed v0.6 policy and independently read base/head trees. It must
  refresh selected hashes and source-derived routes, preserve owner/install
  conditions, and bind selector, manifest and R3 release identities before a
  same-job scan. The current corpus runner's fixed manifest digest, source
  pins, counts and zero-result SARIF expectation cannot simply be relaxed for
  event use; a distinct validated event contract is needed.
  Stacked downstream [draft PR #159](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/159)
  now prepares that separate source-first event input contract in the manual
  drill. It rechecks the exact candidate report against Git, refreshes
  selected Git blobs/hashes at the event head, derives routes before
  extraction, rejects selected-owner recipe/config drift and route changes,
  and records the frozen policy and input digests. Historical extraction
  observations are removed from refreshed rows. A local
  [PR #26933 control](evidence/mvp-event-manifest-pr26933-20261124/README.md)
  yielded 128 selected identities and 13 exclusions; 23 combined event/resolver tests,
  14 selector tests and `actionlint` passed. PR #159 is an input-oracle stage,
  not a released CodeQL event scan or Gate 8 pass.
  [Draft PR #160](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/160)
  combines #159's oracle stack with parallel #157's v0.6 corpus runner and
  adds the release-gated event runner. The manual workflow replays captured
  PR inputs in a clean job, checks the immutable R3 release and route-source
  digest, extracts the event's selected identities, runs the released suite,
  and sends its actual SARIF to a separate generic-event triage consumer.
  Valid new tuples retain their exact multiplicity with `triage_required`;
  the historical exact-result consumer remains strict. The captured PR
  #26933 event has 128 selected identities. Local `actionlint`, 47 focused
  contract tests and 14 selector tests pass. At PR head `6b7c8e3`, hosted
  contract and typed-handoff checks passed in runs `45496222110`,
  `45496222482` and `45496222272`; the broad unittest job subsequently
  passed in run `45496222272`. The release scan correctly skipped because the release
  lock is null. A subsequent commit `33a27a4` on #160 adds a separately
  isolated released clean-control scan to the same job, requiring an exact
  empty triage result and retaining control failures. The control still runs
  after R3 when the event scan fails. Local `actionlint` and 50 focused
  contract tests passed. A clean-checkout
  [PR #26933 control preflight](evidence/mvp-event-control-preflight-pr26933-20261124/README.md)
  accepted the captured canonical base at `727d8d2` with 128 selected and
  13 excluded identities, but did not run CodeQL. The historical OpenVPN
  positive path is outside the v0.6 selected policy; a real incoming
  known-alert drill needs its own reviewed event source. No hosted released
  event/control runs or positive/control Gate 8 drill have occurred. Review
  then found that route-validation failures lost the raw routing report and
  that post-triage integrity failures could be mislabeled as clean-control
  assertion failures. PR #160 commit `c97ea4d` retains raw routing before
  validation, reports provisional triage accurately, and preserves the
  preflight artifact name after an earlier step fails. Local `actionlint` and
  24 focused tests passed on that fix; hosted contract, typed-handoff and
  unittest checks passed in runs `45498258911`, `45498259013` and
  `45498258686`. The release-dependent jobs skipped on the null lock.
  Follow-up review found that indexing could emit routing before failing;
  commit `e2b2715` retains that raw report in `out/` even on index failure,
  with a focused failure-path test. Hosted contract, typed-handoff and
  unittest checks passed in runs `45499871509`, `45499871663` and
  `45499871502`; release-dependent scans still skipped on the null lock.
  Commit `2096f1d` then labels and validates the control manifest and scan
  receipt as `event.source_role: clean_control`, preventing its commit from
  being read as the PR head. A local canonical-base oracle replay passed at
  128 selected/13 excluded, with 51 focused and 14 selector tests passing;
  hosted contract, typed-handoff and unittest checks passed in runs
  `45500743224`, `45500743278` and `45500743128`. The live scans skipped
  because the release lock is null.
  Draft #160 now has base-tree commits `17efa31` and `1b42fdc` on its exact
  head `1b42fdc99492867df76d6ff074379c9c1053db21`. The resolver fetches
  the captured API base SHA from the hardcoded canonical upstream into an
  isolated temporary Git repository, verifies the commit and tree, and
  records both in its receipt. The event manifest checks that tree against
  a fresh source inventory; the control adapter separately binds its frozen
  policy base tree. Missing/mismatched objects, inherited Git URL rewrites,
  timeouts and receipt/inventory tree drift have focused rejection controls.
  An independent live helper check fetched pinned OpenWrt commit
  `4e9642517b48bae612ff10fb72fb9199e559500e` and returned tree
  `328d4df01c038d365176b72753b778e10c3ff413`, matching GitHub's Git
  commit API. Hosted contract, unittest, typed-handoff and lock-state checks
  passed on the new PR head; live resolution and released scans skipped on
  the null lock. The workflow still replays captured PR API bytes rather than
  re-fetching the PR in the scan job, and no trusted completion issuer exists.
  A separate [inert local feasibility probe](evidence/mvp-inert-positive-local-20261124/README.md)
  placed an unreachable direct-RPC shell-word pattern at the v0.6-selected
  LuCI `example.uc` path and an otherwise matching quoted control in isolated
  single-file databases. The experimental producer/default suite returned
  one exact positive SARIF tuple at line 53, columns 26–44 and zero control
  tuples, with one successful extraction and no errors per file. Its earlier
  handwritten route expectation was wrong and is retained; the final route
  expectation matches the pre-existing v0.6 policy, but the rerun followed
  observed output. This is a candidate for an independently predeclared
  controlled incoming drill, not a release-backed Gate 8 result. A dedicated
  upstream drill PR would require separate authorization and a verified
  maintainer-facing policy before creation. The
  [Gate 8 drill sequence](planning/mvp-gate8-positive-drill-20261124.md)
  separates the clean PR #26933 run, internal fixture feasibility and a
  genuine canonical-upstream known-alert event.
  Downstream [PR #162](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/162)
  adds an isolated, read-only incoming-discovery prototype that inventories
  observed OpenWrt and LuCI open PR heads and default-branch tips, retains
  response bytes and a bounded pending queue, and requires an explicit prior
  checkpoint or genesis. The initial `9f1172e` draft passed 19 offline
  controls and hosted `unittest`/`typed-handoff` in run `45505257051`.
  The later live-derived revisions passed 27 offline controls, adding
  pagination, cross-repository metadata, retry and resource-bound cases.
  Early live probes found GitHub API quota, per-response size, aggregate
  receipt, transient HTTP and cross-repository metadata boundaries; their
  [failure receipts](evidence/mvp-incoming-poller-live-preflight-20261124/README.md)
  are preserved. The revised v3 prototype produced one complete
  [manual discovery checkpoint](evidence/mvp-incoming-poller-live-20261124/README.md)
  at `05312d6` with 1,851 pending decisions and no HTTP retries. This is
  one non-atomic API snapshot, not a guarantee of every upstream transition.
  The final documentation-only head `a417fb9` passed hosted `unittest` and
  `typed-handoff` in run `45510746930`; #162 merged as
  `cd6c5c1f8d53edf6436ba34091106e5ff0d84382` without a schedule.
  The prototype does not
  schedule work, authenticate
  completion, resolve default-tip events into the consumer, or guarantee
  transient heads between polls; these remain Gate 8 work before an incoming
  scanning service can be claimed.
  A separate [offline queue draft PR #164](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/164)
  builds on that poller at `51923e56fa858d0f07f374a2859031d54352fa4b`.
  It prototypes a transactional predecessor, stable PR-head identity,
  bounded reservations, first-attempt priority, recovery and audited retry
  preemption. Twelve queue and 27 poller tests pass locally. The hosted
  `unittest` and `typed-handoff` checks passed in run `45516924286`, but that
  earlier run did not execute the new queue tests. A workflow-file edit was
  locally verified but could not be pushed because the available token lacks
  workflow-file permission. Draft PR #164 now has a discovery loader at
  `b47c92eb5df0729e8e7ecfaa8af886e540ecff53` under the existing
  `policy/tests` CI root. It ran all 27 poller and 12 queue tests locally;
  hosted Linux run `45529885754` passed `unittest` and `typed-handoff`, and
  the `unittest` log explicitly includes both modules' test cases (1,118
  conformance tests total). This closes the offline CI wiring gap. The
  prototype has no trusted production signer, verified same-job artifact
  handoff, released event scan or authenticated live completion. Its earlier
  1,851-row replay reserved identities without scanning, and predates the
  final in-flight capacity rule. Keep #164 draft and unscheduled until these
  gaps and the exact CI gate are resolved; it is not Gate 8 evidence.
  A separate stacked [default-tip draft PR #165](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/165)
  now at `19be819be60673528f6c5c67e00012b3003ac3ea` prepares an offline
  source-first path for a selected default-branch tip and a distinct earlier
  recorded tip of the same repository and branch. It independently checks
  canonical commit/tree identities in fresh checkouts, pins the source policy,
  builds separate manifests and retains binding digests. Security review
  found and fixed real v3 repository-name handling, ambient Git configuration,
  redirect and run-path boundaries. Thirty-eight focused local tests pass.
  Earlier hosted checks did not run the new resolver tests. A discovery loader
  at `ec3ccb70159e25e2b201091f6cfb71db287af8c7` now brings both
  default-tip modules into the existing policy CI job. Their 15 tests pass
  locally; hosted Linux run `45530467801` passed `unittest` and
  `typed-handoff`, and its conformance log names test cases from both modules
  (1,128 total conformance tests). After #160's base-tree change, #165's four
  commits were replayed onto the new base and its adapter now derives the
  frozen policy base tree from its inventory. Forty-eight combined focused
  tests passed locally. Hosted run `45532175245` passed `unittest` and
  `typed-handoff` on the restacked head, including the base-tree and
  default-tip module tests. The earlier tip is only a control candidate.
  No live upstream fetch, authenticated checkpoint history, clean-control
  result, released scan or consumer replay has occurred, and #165 remains
  draft and unscheduled. Integrating its event kind and actual SARIF into the
  released consumer path is still Gate 8 work.
  The [same-job completion issuer contract](planning/mvp-incoming-completion-issuer-contract-20261125.md)
  specifies the trusted job boundary, exact event/control artifact links,
  queue reservation binding, failure transitions and rejection controls needed
  before a completion can be signed. It is a design, not an implemented issuer.
  A local offline link probe was reviewed but kept out of the repo because
  its passing fixture does not pass the actual SARIF consumer and does not
  establish producer or consumer execution. A valid queue MAC alone cannot
  turn that synthetic packet into Gate 8 evidence.
  The [12-path recipe mapping](planning/mvp-openwrt-full-tree-candidates-v0.5-mapping-20261124.md)
  identifies conditional product install paths used by the source-staged
  v0.5 expansion, with no installed-byte claim.
  A local [v0.5 selector control](evidence/mvp-full-tree-v0.5-20261124/README.md)
  added an exact v0.5 policy digest to the disposable consumer prototype.
  On the unchanged pinned OpenWrt tree it classifies all 47 detected
  candidates: 46 selected, one excluded and none unreviewed. The v0.4 policy
  leaves exactly those 12 additions unreviewed and fails closed. Nine local
  selector tests pass. The bounded selector is now in draft PR #158; recipe
  inference, actual installed bytes and a real incoming-change scan remain
  open.
  On the captured OpenWrt PR #26933 base/head pair, the same v0.5 selector
  [fails closed](evidence/mvp-full-tree-v0.5-20261124/README.md): 52
  candidates at each revision, 46 selected, one excluded and five newer
  unreviewed identities. No selected source changed. Those five need recipe
  review before an event policy can proceed; this is not a CodeQL scan or
  Gate 8 pass.
  The subsequent [v0.6 selector control](evidence/mvp-full-tree-v0.6-20261124/README.md)
  classifies the captured PR pair's 52 candidates as 51 selected and one
  excluded, with no unresolved identity; the LuCI same-SHA control has 65
  selected and four excluded. This resolves that source-policy inventory for
  the captured pair only. The refined grammar patch later resolved the two
  extraction failures in a separate 128-file local run. An event-triggered
  released Linux scan and consumer SARIF result remain open.
- [Installed-byte mapping inspection](planning/mvp-installed-byte-mapping-20261124.md)
  identifies the pinned LuCI `luci.mk` copy and `.ut` substitution rules and
  OpenWrt CLI copy rule. It specifies a narrow package/IPK byte-comparison
  experiment; no package output was built, so installed-byte provenance
  remains open.
  A [package-build preflight](planning/mvp-installed-byte-build-preflight-20261124.md)
  identifies `luci-base` `http.uc` versus version-substituted `header.ut`
  as the smallest discriminating IPK comparison. Homebrew GNU Make 4.4.1
  satisfies OpenWrt's Make requirement, but this `work/` volume is
  case-insensitive while OpenWrt requires a case-sensitive filesystem.
  A dedicated volume or Linux runner, exact pinned feeds and target config
  are needed before any package-byte claim.
  An [experimental Linux runbook and byte comparator](experiments/luci-ipk-byte/RUNBOOK.md)
  now specify an x86/64 `luci-base` build and compare the pinned Git source,
  prepared file, package staging file and IPK member for direct `http.uc` and
  version-substituted `header.ut`. The original scaffold's 14 synthetic tests
  passed but modeled the wrong outer IPK format; source review invalidated
  that parser. The corrected ledger comparator has 18 tests covering the
  pinned gzip-tar shape. The pinned OpenWrt defaults
  to APK, so the IPK runbook explicitly disables APK and verifies x86/64,
  `luci-base=m`, and local pinned feed links. Its feed `src-link` entries use
  `../../luci` and `../../packages` because the links resolve from the
  OpenWrt `feeds/` directory. The preparation receipt records
  clean source pins and the local case-insensitive filesystem limit; no
  package build or IPK result exists, and feed/config/staging resolution
  remains for the Linux experiment.
  A reviewed downstream [PR #161](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/161)
  staged a manual Ubuntu `luci-base` build at consumer `main`
  base `a1c9875`. It explicitly builds host tools and toolchain, retains a
  run-owned IPK, and checks both selected files against Git, prepared,
  staging and exact archive bytes. Source review found the pinned OpenWrt
  IPK uses a gzip-compressed outer tar, contradicting the earlier ledger
  experiment's `ar` parser. The ledger scaffold and PR now use the corrected
  format and verify
  package control metadata; 18 comparator tests, `actionlint` and shell
  syntax pass locally. Hosted contract and repository checks passed; PR #161
  merged as `8215fc7931fa62309bc2a5dd861ebfa10ba07a24`.
  [Manual run `45503598387`](https://github.com/lucas-albers-lz4/codeql-openwrt/actions/runs/45503598387)
  passed its contract job, host-tools build and toolchain build, then
  [failed before the intended package build](evidence/mvp-installed-byte-first-linux-failure-20261124/README.md).
  The supposed `make -n` target probe executed recursive OpenWrt recipes and
  hit an opaque `libjson-c` dependency failure without verbose output.
  No IPK or byte comparison exists. Downstream
  [PR #163](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/163)
  removed that probe and runs one verbose serial package build; hosted checks
  passed and it merged as `9018c7633e9dce303d48e2a3ee8d9d78054d03de`.
  [Manual rerun `45513606386`](https://github.com/lucas-albers-lz4/codeql-openwrt/actions/runs/45513606386)
  completed successfully. Its retained IPK and
  [independent two-file byte review](evidence/mvp-installed-byte-luci-base-20261125/README.md)
  show that `http.uc` matches source through preparation, package staging and
  IPK, while `header.ut` matches source through preparation and then changes
  during staging when the package version replaces a template token. The
  staging and IPK bytes match for both files. This establishes two actual
  package-member byte identities at the pinned LuCI/OpenWrt/packages commits;
  it does not establish the remaining installed corpus denominator, a CodeQL
  scan of those bytes or the R3 released Linux handoff.
  A follow-up [complete suffix-member inventory of that same IPK](evidence/mvp-luci-base-ipk-inventory-20261125/README.md)
  finds 16 regular `.uc`/`.ut` members: 14 equal to pinned LuCI source bytes,
  one version-substituted `header.ut`, and one generated `version.uc`. This is
  an exact denominator for the single `luci-base` package and suffix rule,
  established retrospectively from the retained artifact. It does not cover
  extensionless files, other packages or actual CodeQL extraction.
  A further [local actual-IPK extraction check](evidence/mvp-luci-base-ipk-extraction-20261125/README.md)
  staged those exact 16 member bytes into a private database. All 16 routed
  and appeared once in `SuccessfullyExtractedFiles`, with zero extraction
  errors. Eight routes were plain; seven `.ut` and content-marked `uhttpd.uc`
  were markup-inconclusive. The pre-output oracle and raw outputs matched
  exact identities, decisions and multiplicity. This macOS build used
  separately recorded copied grammar-generated assets whose regeneration
  from current source was not proven; no separate source-byte control,
  released Linux scan, SARIF or consumer handoff was run.
- A [source-only census](planning/mvp-openwrt-packages-candidates-v0.1.md)
  of pinned OpenWrt core and packages-feed source found
  35 additional OpenWrt candidates beyond the 11 CLI paths and 37
  packages-feed candidates, including three test mocks. These are candidate
  inventories, not installed or extracted denominators. The first coherent
  OpenWrt source-first expansion is the 17-file
  [wifi-scripts slice](planning/mvp-wifi-scripts-next-slice.md). Its install
  recipe selects the Ucode variant only under `CONFIG_WIFI_SCRIPTS_UCODE=y`
  and can overwrite a shell script at the same installed path; the config
  and actual package bytes must be frozen before a Gate 6 claim.
- Security review of consumer PR #152 found that duplicate identities could
  be placed in both the expected extraction manifest and receipt while one
  source record still passed. The parser now rejects duplicate expected
  extraction identities; ten focused tests pass locally. The fix was pushed
  at `401ee68fc14acd715335a974cbe551864ec181dc`; both hosted `M2 policy`
  jobs passed on this head in run `45428761114`. The offline parser still
  cannot authenticate a producer receipt or prove indexed database bytes;
  the fresh R3 Linux workflow must bind those inputs in one job.
- A fresh [76-file local aggregate probe](evidence/mvp-corpus-v0.1-local-run/README.md)
  used bounded corpus v0.1 as its pre-run oracle in an isolated macOS database.
  All 76 projected installed-path inputs matched exact source hashes and
  route decisions; 42 routed plain and 34 markup-inconclusive, all appeared
  once in successful-file diagnostics, with zero extraction errors. The draft
  default suite resolved to one direct RPC rule plus two diagnostics and
  emitted zero SARIF results on this selected current-source corpus. All nine
  CodeQL phases exited zero; total phase wall time was 14.209 seconds, with
  peak RSS unavailable under this sandbox. Earlier attempts are retained as
  noncanonical failures/limitations. This is source-staged local evidence,
  not actual installed bytes, a Linux Gate 7 cost result or a security
  negative.
- The next [wifi-scripts source slice](evidence/mvp-wifi-scripts-extraction-20261124/README.md)
  found three mistaken route expectations in its initial 17-file oracle:
  three `.uc` files also have Ucode shebangs, which the pinned extractor
  checks first. The original mismatch is retained. A corrected source-first
  oracle preceded a fresh isolated run: 17 exact plain routes (12 extension,
  five shebang), 17 successful-file identities once each and zero extraction
  errors; all eight commands exited zero. This conditional
  `CONFIG_WIFI_SCRIPTS_UCODE=y` source-staged result does not establish
  actual package-installed bytes or query/security coverage.

## Ledger reconciliation with Security-40

The ledger main branch already uses claim IDs 035–074 for Security-40.
The original MVP remap batch was recorded as claims 075–086; the later
current-source/grammar batch adds claims 087–090. Related topics are
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
