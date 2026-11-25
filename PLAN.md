# Next batch: prioritize bounded evidence leads

The active [MVP-1.md](MVP-1.md) plan uses three internal release tickets and
two historical shell cases as its first gate, then advances through
current-corpus scanning, incoming-change CI, maintained releases, alert triage
and a separate maintainer-ready decision. It records parallel lanes and
post-merge gates.

For the internal security-check release track, use the
[historical LuCI case selection and release gates](planning/mvp-historical-security-20261123.md).
That plan is source-backed triage, not a demonstrated alert or a replacement
for the evidence batches below.

The [24-package evidence program](planning/next-program-20261122.md) is the
current larger planning queue. It accounts for newer upstream markup CFG,
receiver-observation and read-only v2 changes. Its packages are conditional
decisions and checks, not promised claims or automatic execution.

Separate active program (opened 2026-11-24):
[Security-40](planning/security-40-20261124.md) — forty interface claims
(035–074) grounded in OpenWrt advisory history, executed sequentially with
local CodeQL. Its resume point is
[security-40/progress.md](planning/security-40/progress.md). It does not lift
any gate or hold of the 24-package program.

The [12-wave roadmap](planning/roadmap-12-waves.md) extends the [next four evidence decisions](planning/wave-next-20261121.md). Its ordered gates take precedence over the older generic batch outline below; later waves are conditional, not automatic runs.

The prior producer/consumer handoffs remain in [planning/batch-20261118.md](planning/batch-20261118.md). After the handoff branch merged to `main`, this
candidate-triage batch refreshed disposable snapshots and completed claims
017–019. Its pin set is producer
`8376a6d72a2879de24e68a28c6ef1e02b319df83`, consumer
`1d025213c102dfa68a0f1a5cb46de65f5b0c4e33`, LuCI
`b2e0be4b46ec0fd43394c081fa7c50657af14011`, and rpcd
`d99f703e4035d03fbcfbada3cb697db346c2b984`; these results remain scoped to
the exact files and tests recorded in each claim. The 2026-11-18
[candidate lead list](planning/claim-opportunities.md) has 17 distinct leads
and explicit ownership/blockers; it is not a proposal for 17 more claim files,
much less 100. Do not rerun the same pins absent a relevant delta. These are
observations, not pins for a later run: fetch again and choose explicit full
SHAs at launch.

The steps below remain a reusable workflow, not a claim about future runs.
Resume by reading [AGENTS.md](AGENTS.md), the [claim index](README.md#claim-index),
and [coverage portfolio](planning/coverage-portfolio.md). Claim 005 remains
partial until an actual supported fresh query-to-record path is observed. Claims
018–019 record producer output relevant to ucode #75, including an
8-source selected LuCI slice, but do not run a fresh consumer handoff.
Issue #75 is now closed; that status does not broaden those runs.

The requested typed setBlockDetect refresh is recorded in [claim 008](claims/008-setblock-typed-handoff.md#refresh-2026-11-21), at producer `8375887ed14825dd59addbfd0df43616d9e684fb` and consumer `33ff29f9f311fec078be8e2df04261529cba0e65`. It is a bounded fixture handoff, not an expanded real-source slice. Fetch and triage again before choosing another batch.

[Claim 020](claims/020-pinned-markup-call-syntax.md) adds a pinned LuCI `uhttpd.uc` markup AST call inventory with controls. It does not change the consumer's inconclusive routing status or establish dispatcher semantics.

## Objectives

Broaden the evidence beyond the single LuCI fixture while keeping the batch
small, isolated and useful to ongoing development. Target two or three bounded
claims or one paired integration claim if the evidence is more involved. Do
not attempt a coverage percentage or a whole-corpus claim from a small slice.

## 1. Refresh and triage

1. Confirm available disk, memory, CPU, CodeQL and build tools. Fetch both
   repositories into fresh or verified disposable checkouts under `work/`;
   select full SHAs, record clean/dirty state and relevant tool versions.
   Never use the active development checkouts or share writable databases.
2. Review changes since the previous producer/consumer pins, especially
   extractor routing, diagnostic queries, relevant models and query contracts,
   fixtures, consumer adapters, corpus lock and policy context. Check the
   current status and scope of the existing issues linked from affected claims.
3. Produce a small impact map: unchanged historical evidence, claims needing
   rerun, and changed or incompatible contracts. An earlier result is not a
   result for a new pair. Select reruns based on that map rather than rerunning
   every claim automatically.

## 2. Select one pinned real-source slice

1. Inspect the consumer's corpus lock, source acquisition and file inventory
   instructions at the chosen revision. Select one small, consequential slice
   for which the actual source bytes can be obtained at the pinned revision;
   distinguish upstream corpus bytes from checked-in test fixtures. Read the
   acquisition scripts before running them, and do not modify either active
   project.
2. Independently enumerate intended source paths and expected selection from
   the corpus/inventory and routing contract. Record the source revision,
   bytes/digests, source root, exact file identities, selection criteria and
   any omissions or unsupported layouts. Pick an eligible near miss and an
   actual positive before examining output. If the corpus or installed layout
   cannot be obtained, document the blocker and use only clearly labeled
   evidence; do not fabricate a corpus run.
3. In a fresh owned database, capture routing before finalization, query exact
   successful-file identities and extraction errors, and compare against the
   independently prepared inventory with multiplicity. Preserve small reviewed
   receipts. Report selected, successfully extracted, errored, excluded and
   unknown identities separately; do not infer semantic coverage from clean
   extraction. Create or update a bounded claim with the actual outcome.

## 3. Follow one meaningful dependency

From the selected slice, identify one query or language/model dependency that
matters to a named analysis. Inspect its implementation, tests and existing
issues; derive a positive and a valid discriminating near miss, then run the
real query with clean extraction evidence. Record exact observations and
unsupported shapes. If a real producer–consumer interface is relevant, use a
separate consumer copy and the actual fresh producer output; otherwise do not
invent an adapter. Keep claim 005 partial unless an actual supported fresh
record path exists and is observed.

## 4. Measure and report

Record wall-clock time separately for setup/build, extraction, query and any
consumer step, including the tool and version used to measure it. Capture peak
memory when available, run serially where database/cache ownership requires
it, and document failures or unavailable measurements. Existing focused runs
were generally short; the 52-second fs-binding query evaluation is not a
full-corpus benchmark. Distinguish elapsed time, CPU time and peak memory.

Update the claim record(s), [portfolio](planning/coverage-portfolio.md) and
README index. Record exactly what was demonstrated, what remains unknown and
what is owned elsewhere. Verify links, `git diff --check`, and the relevant
receipt formats; review anything staged for secrets or private paths. Do not
commit or push unless requested.

## Optional delegation and review

If delegation is authorized and the exact route is available, use
`gpt-6-luna` for inventories and receipts, `gpt-6-luna` at xhigh effort for
ordinary coordination and verification while Terra is unavailable,
`gpt-6-sol` for defensive security-sensitive
semantics, and `gpt-6.2-sol` for difficult final review when needed. Resolve
and smoke-test routes before use; record unavailable routes rather than
silently substituting. A same-model second pass is not independent-model
corroboration. This is an optional efficiency aid, not a prerequisite or an
instruction to run scans in parallel. For MVP work that crosses project or
trust boundaries, use the [review and run protocol](planning/mvp-review-run-protocol.md).
