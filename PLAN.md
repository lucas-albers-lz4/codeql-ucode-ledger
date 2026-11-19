# Next batch: refresh pins and examine a real-source slice

The first bounded batch under this plan is recorded in [planning/batch-20261118.md](planning/batch-20261118.md). The steps below remain a reusable workflow, not a claim about future runs. Resume by
reading [AGENTS.md](AGENTS.md), the [claim index](README.md#claim-index), and
[coverage portfolio](planning/coverage-portfolio.md). The most recent ledger
runs used producer `d3588ca6821fe983d240fcbb2e80692fabcc6aab` and consumer
`a8bdef3c22c8d5ba9999baa978052b59bd22907e`; their results remain scoped to
those revisions and named fixtures. On 2026-11-18 UTC a read-only remote-head
check returned producer `094a163db1138c83820197180501bd7c78bd9051` and
consumer `c45d0c4f36e66e7927d610d5a92c1186bb910f1f`. These are observations,
not pins for a later run: fetch again and choose explicit full SHAs at launch.

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

If delegation is authorized and the exact route is available, have
`gpt-6-luna` inventory changes and candidate paths, coordinate and reproduce
runs with `gpt-6.1-terra`, and use `gpt-6.2-sol` for a bounded adversarial
review of expectations, controls and conclusions. Resolve and smoke-test
routes before use; report unavailable routes rather than silently substituting.
A same-model second pass is not independent-model corroboration. This is an
optional efficiency aid, not a prerequisite or an instruction to run scans in
parallel.
