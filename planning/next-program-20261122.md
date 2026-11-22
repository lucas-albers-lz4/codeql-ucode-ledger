# Next evidence program: 24 ordered work packages

This is a **plan**, not an instruction to run every query or a promise of 24
new claims. It scales the last three-claim effort to 24 small work packages
(eight times as many packages), including decision gates, independent oracles,
runs and reviews. A useful package can end with a documented stop rather than a
claim. Execute in order; if a gate fails, record why and move to the next
independent eligible package. Reassess after each four packages and when an
upstream contract changes. One or more closely related packages may support a
single claim; no claim number or status is reserved in advance.

## Planning-time findings and priorities

On 2026-11-22, GitHub `main` returned producer
`6010ff2c0f101f7629c6fe117a421f671c311a2b` and consumer
`32c3551b2ceab3ec8781b5621b50032f6d709863`. These are observations, not
future run pins. Compared with the producer `0a6612f` and consumer `5f8bd26`
used in the prior decision map, the producer has ten new commits containing
bounded markup CFG/creation modules and a direct-copy receiver experiment;
the consumer has one new commit with an experimental read-only v2 assessment
boundary. Inspect exact diffs, current owners and documented supported subsets
before relying on any change. The old progress log accurately describes the
older revision, but its statement that only a CFG proposal existed is no longer
a description of the newer producer head.

The producer's [bounded CFG documentation](https://github.com/lucas-albers-lz4/codeql-ucode/blob/6010ff2c0f101f7629c6fe117a421f671c311a2b/docs/markup-cfg.md)
limits its graph to selected clean roots, and its
[direct-copy experiment](https://github.com/lucas-albers-lz4/codeql-ucode/blob/6010ff2c0f101f7629c6fe117a421f671c311a2b/docs/m4-receiver-direct-copy.md)
remains a bounded may-reach observation, not a production model. Issue
[#57](https://github.com/lucas-albers-lz4/codeql-ucode/issues/57) remains open;
verify owner scope before deciding what the new modules permit. Consumer
[issue #138](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/138)
and its [pilot documentation](https://github.com/lucas-albers-lz4/codeql-openwrt/blob/32c3551b2ceab3ec8781b5621b50032f6d709863/docs/v2-readonly-pilot.md)
limit the v2 work to an opt-in, read-only boundary. The real mounts result
remains unassessed pending independently reviewed scope and authority; the
Linux libc gate is unknown on Darwin. Existing archived producer evidence is
not a fresh v2 producer execution.

## Execution rules

- First fetch into disposable checkouts under `work/`; record full SHAs,
  dirty states, tool versions, relevant source/lock/pack digests and issue
  ownership. Review scripts before execution. Validate available resources and
  own every database, output, temporary path and writable cache. Respect
  higher-priority environment restrictions when configuring isolation; do not
  repurpose `HOME`. If ownership cannot be demonstrated, stop and record it.
- For each actual run, fix an independent source-derived expected multiset and
  valid positive and eligible near miss before viewing results. Check exact
  routing, extraction identities, diagnostics and multiplicity first; retain
  commands, exits, elapsed times and peak memory where supported. Keep heavy
  runs serial and use fresh database and artifact paths. Large raw artifacts
  stay in `work/`; retain small reviewed, normalized evidence.
- Check an actual producer output with an actual consumer only when the
  supported interface and a distinct decision exist. Retained inputs,
  snapshots and synthetic records are not fresh handoffs. Never invent an
  exporter or infer runtime behavior, reachability, taint, authorization or
  vulnerability from syntax, source-model or CFG observations.
- User direction allows a named upstream analysis need without a downstream
  consumer. Documented intent is the starting policy authority; missing intent
  requires an owner decision. Existing JS UCI execution hold remains: planning
  does not lift it. Claim 005 stays partial until its real supported
  query-to-record and retention path is observed.

## Ordered packages

| # | Decision and deliverable | Gate, controls and stopping rule | Lead role |
|---|---|---|---|
| 1 | Refresh producer, consumer, corpus and issue ownership; create a concise delta/impact map for the changes above. | Do not reuse these observed heads as run pins. Map changed APIs, tests, contracts, tools and issue state; skip stale refreshes with no relevant delta. | Luna collects; Terra verifies. |
| 2 | Inspect new markup CFG and creation module contracts, implementation and existing smoke oracles; identify one unanswered ledger decision. | Distinguish an implemented bounded graph from a complete markup CFG and from dataflow. Stop if upstream already answers the exact proposed decision. | Sol semantic review; Luna inventory. |
| 3 | Independently enumerate a minimal supported markup source and an eligible unsupported near miss, with exact root, AST and expected node/edge identities. | Establish source oracle before results; include valid unsupported syntax and separately identify any intentional malformed diagnostics. | Sol designs; Luna transcribes; Terra verifies. |
| 4 | If 2–3 pass, run the supported bounded CFG decision in a fresh database and compare the complete selected node/edge multiset. | No inferred rendering, flow, runtime or security; preserve query identities and diagnostics. Defer if owner scope or controls do not support a distinct test. | Luna runs; Terra verifies. |
| 5 | Review the separate markup creation graph for a real or independently justified bounded decision and its existing upstream controls. | Stop if its documented subset or existing smoke already answers it; do not conflate creation graph with ordinary markup CFG. | Sol reviews; Luna inventories. |
| 6 | If 5 yields a distinct case, prepare creation-scope node/edge and unsupported-case oracle and run one fresh isolated check. | Exact source and root identities, a supported positive and valid near miss; no claims about general callable execution or flow. | Sol designs; Luna runs; Terra checks. |
| 7 | Screen actual selected LuCI markup for one source shape inside the bounded graph subset and one excluded shape. | Raw staged bytes are not necessarily installed bytes. Stop if no eligible real source or no distinct analysis decision beyond upstream smoke and packages 2–4. | Luna inventories; Terra verifies. |
| 8 | If 7 passes, test the named real-source graph decision with the predeclared controls; otherwise record why it is unsuitable. | Check full graph identities, unsupported status and diagnostics. Markup routing can remain inconclusive; no consumer or dispatcher inference. | Luna runs; Sol reviews boundaries. |
| 9 | Inspect the new direct-copy receiver experiment and #48 ownership; compare its current oracle with claim 014 and prior receiver provenance and alias evidence. | The experiment is may-reach and does not resolve member-call targets or lift the production hold. Stop if no distinct downstream decision exists. | Sol reviews; Luna collects. |
| 10 | Search pinned real sources and named queries for an alias case whose modeled outcome would change a concrete analysis decision. | Record precise source and query; a target count or a synthetic alias alone is insufficient. Stop if no affected case exists. | Luna searches; Terra verifies. |
| 11 | If 10 passes, specify source/copy/receiver/call identities and reassignment, conditional merge, shadow and unrelated-object controls. | Preserve may-reach vs must-reach; independently predeclare all selected sites, including negative call inventory. | Sol designs; Terra reviews. |
| 12 | If 11 passes and owner scope permits, run the bounded observation and compare exact identities and multiplicity. | No production model promotion, resource identity or runtime target claim. Otherwise document the decision gate. | Luna runs; Terra verifies. |
| 13 | Inspect v2 pilot source, tests, exact context selection, inputs and #138 acceptance against current consumer pin. | Separate v1 history, archived neutral evidence, v2 invocation and actual live producer. Retain Linux/Darwin platform distinction. | Terra coordinates; Luna maps. |
| 14 | Independently map synthetic second-package identity and expectation resolver contract, including same name/version from a different feed. | Positive and independently valid negatives for provider, caller, context and selected authority; do not infer real package authentication. | Sol reviews; Luna transcribes. |
| 15 | If 13–14 pass, exercise an opt-in synthetic v2 path and the named feed/provider and context controls in a disposable consumer copy. | Observe actual output, identity and test exits; no producer handoff or real authorization claim. Verify pre/post retained-artifact hashes. | Luna runs; Terra verifies. |
| 16 | Check one independently chosen resolver failure family: duplicate IDs before applicability, conflicting authorities, or missing operation among several. | Each negative must pass earlier checks and assert error/conflict/unknown exactly; avoid duplicating upstream tests without a distinct decision. | Sol selects controls; Luna runs. |
| 17 | Inspect the real mounts input chain and candidate authority scope against independent source and documented policy. | Real allow stays unassessed until scope and authority are separately reviewed; ACL/source alone do not establish intended policy or a live route. | Sol reviews policy boundary; Terra verifies. |
| 18 | If 17 supports a distinct test, exercise the read-only real-input v2 boundary and platform-appropriate checks. | On Darwin report Linux libc gate unknown; only a real Ubuntu workflow establishes its Linux result. No new paired run unless actual producer output is separately generated and consumed. | Terra coordinates; Luna collects. |
| 19 | Reconcile current producer/consumer/exporter/adapter changes with the last actual handoffs and v2 input contract. | If no relevant delta or named new decision, skip live rerun. Keep typed, CSV and v2 paths distinct. | Luna maps; Terra verifies. |
| 20 | If 19 finds a supported changed handoff, run the actual producer and actual consumer with a source-derived identity oracle and rejection control. | Use isolated consumer copy and retain timing and all intermediate actual outputs. Synthetic records or archived tables are not a live handoff. | Terra coordinates; Luna runs; Sol handles ambiguity. |
| 21 | Review the JS UCI proposal and the upstream hold, and determine what independent source oracle and approval would be required. | Planning only unless the withdrawn execution approval is separately restored; do not treat this program as lifting the hold. | Luna inventories; Sol reviews. |
| 22 | Only if the hold is explicitly lifted, independently enumerate the full pinned 88-file expected site multiset and review receiver, computed-name and shadow controls. | Re-pin manifest and sources; partial three-anchor oracle is not a completeness oracle. Stop before query output if enumeration is incomplete. | Luna enumerates; Terra verifies; Sol reviews semantics. |
| 23 | Only if 22 passes, execute the supported JS syntax inventory with fresh extraction and exact entity/multiplicity comparison. | Property access is not invocation, binding, runtime effect or authorization. Do not promote Track A. | Luna runs; Terra verifies. |
| 24 | Reconcile results, portable receipts, issue ownership and remaining gates; choose the next batch only from a named new decision or relevant delta. | Claim 005 remains partial without its actual fresh supported path; record unexecuted gates explicitly and do not inflate package count into coverage. | Terra coordinates; Sol reviews ambiguous boundaries. |

Carry forward the other deferred decisions: template-argument work needs a
distinct analysis need; direct cursor-write modeling needs an actual eligible
write site and its own semantic evidence; and the retained direct-exec grant
join needs a supported fresh record interface and independent policy oracle.
No package here removes those gates.

## Model and cost routing

Use `gpt-6-luna` for bounded source inventories, receipt collection and
reviewed mechanical runs; `gpt-6.1-terra` for isolation, coordination and
independent verification; `gpt-6.2-sol` for semantics, discriminating controls
and policy/evidence boundaries. These are optional roles, not mandatory
handoffs. Resolve and smoke-test each exact route at execution time; report an
unavailable route rather than silently substituting. Verify mechanical output
against the pinned sources and do not describe a same-model second pass as
independent-model corroboration. No cost or time savings are assumed without
measurement.
