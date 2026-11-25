# Working in the coverage ledger

This repository is an independent incubation workspace for bounded evidence
about `codeql-ucode` and `codeql-openwrt`. Read [README.md](README.md),
[PLAN.md](PLAN.md), and the relevant claim and portfolio before starting work.
Keep work useful alongside active development in both projects.

## Isolation and revision discipline

- Do not use or modify active development checkouts. Create disposable project
  checkouts, writable CodeQL databases, outputs and caches under ignored
  `work/`; give every run its own database and artifact paths. Use disposable
  consumer copies for adapters that rewrite reports. Inspect scripts first.
- Fetch and record the full SHA and dirty state of each project actually used,
  plus corpus/fixture pins and relevant tool versions. Check available
  resources and avoid concurrent heavy runs or shared database paths. The
  fixture-era commits in earlier claims are historical evidence, not current
  assumptions. Inspect the relevant delta and current issue ownership before
  transferring conclusions to a new revision.
- Record exact commands, exit statuses, source and result identities,
  multiplicity, controls and observed outputs. Measure elapsed time for
  extraction, queries and any consumer step; retain peak memory where the
  timing tool supports it. Do not infer a full-corpus scan time from a smoke.
- Keep large/generated artifacts in `work/`. Commit only small reviewed
  evidence, documenting any normalized paths and the relationship to raw
  output. Do not commit keys, credentials, private data or databases. Link to
  portable evidence rather than claiming another machine can access `work/`.

## Run preflight and verification

- Before launching a run, verify the chosen checkout SHAs and dirty states,
  source and lock digests, tool executable/version, free resources, and that
  database, outputs, `HOME`, `TMPDIR` and writable caches are owned by that run.
  Distinguish pinned upstream source staged at an installed path from actual
  installed bytes; inspect any build/install transformations first.
- If a previously built extractor pack and dependencies match the selected
  source, grammar, toolchain and locks, copy them into the new run and record
  their build provenance and digests. Check dependency readiness before a
  network install; use a timed bootstrap when missing or incompatible. Reuse
  never means sharing a writable database or cache, and an interrupted command
  is not a pass. Poll a live long-running process before retrying.
- Prepare and retain the source-derived oracle before inspecting output. At
  run completion compare source hashes, each routing decision, exact successful
  file identities, diagnostics and output rows including multiplicity. Record
  mismatches and phase timings even for failures. A successful command or a
  matching row count alone does not establish a claim. If distinct AST entities
  can project to identical rows, select their identities or count entities per
  tuple; a CSV row count does not establish entity uniqueness.
- Prefer the small checks in [scripts](scripts/README.md) for portable receipt
  validation and exact tuple comparison. They do not verify source truth,
  provenance, execution freshness or semantic correctness. Keep claim-specific
  expectations and consumer assertions explicit; do not abstract away controls.

## Claims and evidence

- Start from a specific analysis decision and make the smallest testable claim.
  Follow selection → extraction → language/model support → query → consumer
  as applicable. Use [claims/TEMPLATE.md](claims/TEMPLATE.md); assign status
  only after inspecting the evidence. A two- or three-claim batch is a useful
  default, but one cross-repository or difficult semantic claim can be enough.
- Establish expected source and output identities independently before
  inspecting results. Include a valid positive and a discriminating eligible
  near miss, checking exact extraction identities and diagnostics. An empty
  result is not negative proof; intentional malformed-input tests must identify
  their expected extraction errors separately.
- For a live handoff, run the actual producer and pass its actual output to
  the actual consumer. Historical tables, synthetic inputs, offline validators,
  source hashes and snapshot matches do not establish a fresh handoff or
  authenticate execution. Report what was observed and the provenance limits.
- Preserve the distinction between source observations, model/query behavior,
  policy interpretation and runtime behavior. Do not infer completeness,
  safety, reachability, taint, authorization or vulnerability without specific
  supporting evidence. Keep known gaps with their existing owning issues.
- Claim 005 remains partial: the pinned projects did not expose a fresh
  imported-callee query-to-record path. Do not relabel its historical record
  as freshly generated or create an upstream implementation merely to make the
  ledger green.

For producer/consumer, release, package-byte or queue trust-boundary changes,
use the compact [MVP review and run protocol](planning/mvp-review-run-protocol.md).
Before a costly run or implementation, record the decision, exact base/head
and affected contracts, source-first oracle, eligible near miss, test-to-CI
gate map, expected artifacts and resource budget. For code that reads or
writes untrusted artifacts, review the first I/O and credential boundary
before implementation. Give an independent reviewer the diff, relevant
caller/API context, oracle, raw receipts and known limits; record each found
gap with its added control. Revalidate only affected contracts after a base
change, then satisfy the required exact-head gate.

## Model routing

The user's requested routes are `gpt-6-luna` for bounded inventories and
receipts, `gpt-6-luna` at xhigh effort for coordination and non-security
verification previously assigned to Terra, `gpt-6-sol` for defensive
security-sensitive semantics and trust-boundary work, and `gpt-6.2-sol` for
difficult final evidence-boundary review when available. The
`gpt-6.1-terra` route returned Daybreak 403 in this session; do not assign
work to it until a fresh route smoke succeeds. These are optional task
roles, not mandatory stages. Resolve and
smoke-test the exact route at execution time. If a route is unavailable,
record the failed attempt and continue with the primary owner or explicitly
choose another route; do not silently substitute or claim that review
happened. Verify mechanical output against sources. A same-model second pass
is not independent-model corroboration. A requested route does not attest
the server-side model ID. Do not run concurrent scans against shared writable
artifacts.

The user's subscription-linked promotional API credits are separate from the
ChatGPT/Codex usage allowance. OpenAI's published guidance says that benefit
does not cover Codex usage through API keys. Do not switch authentication or
assume a billing route without the user's request and current confirmation;
never ask the user to put an API key in chat or a repository file. Refer to
[OpenAI's benefit guidance](https://help.openai.com/en/articles/20001626-api-credits-benefit-for-eligible-chatgpt-subscriptions)
for current terms.
