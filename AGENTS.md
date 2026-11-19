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

## Model routing

The user's requested model names are `gpt-6-luna` (Luna),
`gpt-6.1-terra` (Terra) and `gpt-6.2-sol` (Sol). Where delegation is supported
and authorized, use Luna for bounded inventories and receipts, Terra for
coordination and verification, and Sol for difficult semantics, control design
and evidence-boundary review. These are optional task roles, not mandatory
stages. Resolve and smoke-test the exact route at execution time. If a route
is unavailable, say so; do not silently substitute a different model. Verify
mechanical output against sources. A same-model second pass is not
independent-model corroboration. Do not claim delegation happened when it did
not, and do not run concurrent scans against shared writable artifacts.

The user's subscription-linked promotional API credits are separate from the
ChatGPT/Codex usage allowance. OpenAI's published guidance says that benefit
does not cover Codex usage through API keys. Do not switch authentication or
assume a billing route without the user's request and current confirmation;
never ask the user to put an API key in chat or a repository file. Refer to
[OpenAI's benefit guidance](https://help.openai.com/en/articles/20001626-api-credits-benefit-for-eligible-chatgpt-subscriptions)
for current terms.
