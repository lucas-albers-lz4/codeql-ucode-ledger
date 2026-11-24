# Incoming OpenWrt/LuCI change scanning: implementation sequence

Status: design work after the first 111-path source-staged corpus gate was
prepared, 2026-11-24. Draft downstream PR #157 advances that gate to a
128-path v0.6 source manifest at captured OpenWrt PR #26933 head. Neither
version has run as a released Linux handoff. This does not assert that
upstream PRs are scanned.
The [MVP plan](../MVP-1.md) requires a real incoming-change trigger for
Gate 8. A PR in `codeql-openwrt` only tests the consumer repository itself.

## First operational slice

1. Keep the released producer and CodeQL CLI pinned exactly as in the R3
   consumer lock. Pin each upstream event to a **full source commit**, not
   a moving branch name. Record repository, PR number or scheduled ref,
   event time, source SHA and resolved Git tree SHA in the run receipt.
2. Start with an explicit `workflow_dispatch` input for one OpenWrt or LuCI
   PR head SHA and one clean control SHA. This is a controlled drill, not
   automatic incoming coverage. Independently confirm the SHA belongs to
   the stated upstream repository and PR before using it.
3. For automatic discovery without upstream repository write access, add a
   scheduled read-only poll of upstream PR metadata and default-branch
   commits. Store an auditable `(repository, PR, head SHA)` decision record
   per poll, including skipped and retried events. Keep a bounded queue and
   explicitly report backlog rather than silently dropping PRs. Define the
   polling interval and CI budget from measured Linux corpus cost before
   enabling it. A later upstream workflow or authorized dispatch can reduce
   latency, but needs maintainer approval and separate permission review.
4. On each selected event, run the **full** supported corpus at the event
   SHA. Recompute source hashes and Git blobs and compare the tracked
   install-path policy against the pinned 128-path v0.6 baseline. New, removed,
   renamed or newly extensionless Ucode candidates produce a coverage-drift
   record and fail closed until reviewed. Do not silently reuse the old
   source hashes as if they belonged to the new commit. Preserve package
   conditions and markup-inconclusive status in the event manifest.
   Generate that manifest from independently enumerated head source bytes
   before extraction: retain source repo, commit/tree, blob and SHA-256,
   reviewed install projection, owner and conditions, and a source-derived
   expected route for each selected path. Check destination collisions and
   bind the parsed policy to its pinned bytes. The current frozen v0.6
   manifest is a baseline, not an event oracle after selected content edits.
5. Run the released default suite and exact extraction diagnostics with
   separate run-owned databases and caches. Compare selected, routed,
   successful and errored identities with multiplicity. Record tool failure,
   coverage drift, new alert, disappeared baseline alert and clean scan as
   distinct outcomes. Keep SARIF and a small reviewed receipt available to
   maintainers; do not convert unknown results into accepted exceptions.
   Reuse R3's release verification and isolated-run mechanics, then bind the
   event manifest to the same-job selector receipt. Keep generic incoming
   alert handling separate from the first corpus gate's pinned zero-result
   expectation; a real new alert must be retained for triage rather than
   silently accepted or discarded.

## Gate 8 drill and promotion

The drill uses a known historical parent/fix or a controlled upstream test
commit with an exact known alert source location, plus a clean control. It
must exercise the **same event resolver, source selector, released scanner
and consumer path** intended for incoming changes. Verify the event SHA,
all selected/extracted identities, rule IDs, SARIF source URI/range, result
disposition, elapsed time and peak memory. An offline replay or manual job
with prebuilt SARIF is insufficient. After the drill, enable the bounded
poller as informational CI; only make it blocking after source selection,
baseline, alert ownership, cost and failure policy have a reviewed run.

The current 128-path v0.6 manifest is a frozen source oracle for the first
Linux Gate 6/7 run. It is **not** a dynamic selector. Stacked downstream PRs
#156–#160 now implement a manual PR identity resolver, bounded source-policy
delta, event manifest and release-gated event/clean-control scan, but their
released jobs have not run because the lock is null. The next gate is to
execute and review those jobs against the immutable release, then address
the durable queue and default-tip path below. Scheduling the frozen manifest
alone would keep scanning an old pin and miss incoming changes.

## Discovery prototype status, 2026-11-24

Downstream [PR #162](https://github.com/lucas-albers-lz4/codeql-openwrt/pull/162)
implements a manual, read-only portion of step 3. It records observed open
PR heads and default-branch tips for both upstream repositories, exact API
responses, head/base commit SHAs, a bounded pending backlog, and an explicit
prior checkpoint or genesis. The default tips have tree IDs; PR trees are
intentionally unresolved until a scan event revalidates them. Twenty-seven
offline tests pass after independent review. Earlier live probes found real
page-size, receipt-size, transient HTTP and cross-repository metadata cases;
the [failure preflight](../evidence/mvp-incoming-poller-live-preflight-20261124/README.md)
retains their limits. A fresh [v3 manual snapshot](../evidence/mvp-incoming-poller-live-20261124/README.md)
completed with 1,651 OpenWrt PR rows, 198 LuCI PR rows and two default tips.
The raw response checkpoint is local and its portable digest/count summary
does not independently authenticate GitHub's event history.
The reviewed tool merged as
`cd6c5c1f8d53edf6436ba34091106e5ff0d84382`; no schedule or scan was
enabled.

## Queue and resolver work after the live snapshot

The first completed manual checkpoint contained 1,851 pending decisions and
selected the lexically first two LuCI identities. Repeating the same poll
without a completion transition can select those identities forever. The
prototype must remain unscheduled until the following are implemented and
exercised together:

1. **Durable state with explicit predecessor.** Each poll records the hash of
   the previous accepted checkpoint, its own immutable output digest and a
   monotonic sequence or equivalent compare-and-swap identity. A new run must
   fail on missing, stale or competing predecessors instead of silently
   starting a genesis. Define retention, recovery and a single owner for
   write access; the current operator-supplied file is only a manual probe.
2. **Authenticated completion and retry.** A completion record binds the
   discovered event key, independently revalidated PR or default-tip commit
   and tree, released producer lock, selected-source manifest, exact extraction
   receipt, SARIF digest, consumer disposition and clean-control result.
   Tool/API/coverage failures remain visible pending work with bounded retry
   history. A selection alone never completes an event.
3. **Fair queue progression.** Preserve every observed event and explicit
   supersession or closure decision while choosing across both repositories
   and event kinds. Demonstrate on the retained 1,851-row checkpoint that a
   finite capacity advances beyond the first two after valid completions,
   that repeated failures do not starve later work indefinitely, and that
   backlog size and oldest age are reported. Measure released Linux scan
   cost before setting capacity or polling interval.
4. **Scan-ready event resolution.** For PRs, re-fetch detail and bind the
   exact head/base commits and trees through the existing #160 resolver,
   rejecting drift or unsupported head provenance explicitly. For default
   tips, add an equivalent independent resolver, source-first manifest and
   clean control. Both paths pass the actual released SARIF to the consumer
   in the same job. A source SHA with `tree: null` in discovery is never
   treated as scan-ready.
5. **Promotion drill.** Run a known positive and clean control through the
   released event path, inspect exact source location and all selected and
   extracted identities, then test a new head, unchanged head, closed PR,
   transient API error and coverage drift. Only after these checks and an
   alert owner/cost policy are reviewed should informational polling be
   enabled. A maintainer-facing blocking check is a later decision.

The manual PR event path in stacked PR #160 remains the separate first
Gate 8 drill path. The completed discovery snapshot narrows operational
unknowns; it does not replace that released scan and consumer handoff.
