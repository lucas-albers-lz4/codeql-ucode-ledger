# codeql-ucode-ledger

A small, independent workspace for examining **specific coverage claims** across [codeql-ucode](https://github.com/lucas-albers-lz4/codeql-ucode) and [codeql-openwrt](https://github.com/lucas-albers-lz4/codeql-openwrt).

The ledger connects a claim to the source it concerns, the analyzer behavior it relies on, the tests or observations that support it, and what remains unknown. It is not an overall coverage percentage or a list of security guarantees.

## Start here

For the next batch, read [PLAN.md](PLAN.md); agent workflow guidance is in [AGENTS.md](AGENTS.md).

The initial claims and their current status are:

1. [Explicit staged-root extraction](claims/001-staged-root-extraction.md): demonstrated for one pinned fixture and root; see the run record.
2. [getBlockDevices query observation](claims/002-getblock-query.md): demonstrated for a pinned fixture and controls.
3. [getBlockDevices producer–consumer handoff](claims/003-getblock-handoff.md): demonstrated for a freshly generated table and pinned consumer.

Together these move from source selection through extraction, query, and consumer, but each claim stands on its own evidence. Claims **001–003** have bounded run records; reassess them when the selected revisions change. The [coverage portfolio](planning/coverage-portfolio.md) maps representative paths; the [candidate lead list](planning/claim-opportunities.md) records prioritization, ownership and stop conditions without inflating leads into claims. See [the claim template](claims/TEMPLATE.md) before adding a result.

## Claim index

| Claim | Current ledger status | Scope |
|---|---|---|
| [001](claims/001-staged-root-extraction.md) | Demonstrated | Explicit staging root and extraction |
| [002](claims/002-getblock-query.md) | Demonstrated | `getBlockDevices` source-table query |
| [003](claims/003-getblock-handoff.md) | Demonstrated | `getBlockDevices` CSV handoff |
| [004](claims/004-system-shadowing.md) | Demonstrated | Bounded `system` shadowing controls |
| [005](claims/005-imported-callee-boundary.md) | Partial | Imported-callee observation; no fresh retained-record path identified |
| [006](claims/006-setlocaltime-construction.md) | Demonstrated | `setLocaltime` source construction and consumer |
| [007](claims/007-setblock-csv-handoff.md) | Demonstrated | `setBlockDetect` CSV handoff |
| [008](claims/008-setblock-typed-handoff.md) | Demonstrated | `setBlockDetect` typed handoff, refreshed at the 2026-11-21 pair |
| [009](claims/009-luci-sys-status.md) | Demonstrated | Two LuCI status helper source shapes |
| [010](claims/010-ubus-call-inventory.md) | Demonstrated | Direct `ubus.call` syntax |
| [011](claims/011-same-file-jump-local.md) | Demonstrated | Experimental same-file argument-to-parameter flow |
| [012](claims/012-backend-declaration-comparison.md) | Demonstrated | Pinned source declarations versus catalog, with oracle qualification |
| [013](claims/013-getfeatures-direct-calls.md) | Demonstrated | `getFeatures` direct call inventory |
| [014](claims/014-fs-binding-guard.md) | Demonstrated | Conservative `fs` binding controls |
| [015](claims/015-pinned-luci-source-extraction.md) | Demonstrated | Three pinned upstream LuCI sources extracted |
| [016](claims/016-pinned-luci-status-query.md) | Demonstrated | Status source-shape query on the upstream slice |
| [017](claims/017-rpcd-login-negation-whitespace.md) | Demonstrated | Consumer login-ACL whitespace parity with pinned rpcd reference |
| [018](claims/018-pinned-luci-shellquote-candidates.md) | Demonstrated | Seven conservative candidate rows on one pinned LuCI source file |
| [019](claims/019-pinned-luci-shellquote-slice.md) | Demonstrated | Shell-injection query on eight selected pinned LuCI source files |
| [020](claims/020-pinned-markup-call-syntax.md) | Demonstrated | Markup AST call syntax on one pinned LuCI file and controls |
| [021](claims/021-pinned-luci-template-extraction.md) | Demonstrated | Extraction of 11 staged pinned LuCI templates and controls |

Every demonstrated status is limited to the run, inputs, controls and revisions
in that claim. These rows are not a coverage percentage.

## Scope and status

- **Proposed:** a question or expected contract; no current run is claimed.
- **Demonstrated:** supported by an identified run, exact revisions, commands, expected identities, observed outputs and relevant controls; scoped to those inputs.
- **Partial:** some, but not all, required evidence exists. State exactly what is missing.
- **Unknown:** insufficient evidence; this is not a negative result.
- **Deferred:** intentionally out of scope or owned elsewhere, with a reference and revisit condition.

A clean extraction does not prove semantic accuracy; a query result does not prove runtime reachability; an empty result does not establish safety; a matching fixture does not prove a fresh producer execution. Separate language support, analyzed source coverage and policy interpretation. Do not infer device behavior, authorization, taint, or vulnerability from a source observation alone.

## Working on another server

Clone this repository and create **separate disposable checkouts** of the two projects. Do not use active development checkouts or share writable CodeQL databases between runs. Each run needs its own workspace, database, outputs, and enough disk, memory and CPU. Local run artifacts belong under `work/`, which is ignored by Git; selectively retain small, reviewed evidence separately when useful. Do not commit credentials, raw private data, generated databases or unexplained host paths.

For lightweight receipt and local-link checks, see [the verification scripts](scripts/README.md). They do not authenticate runs or validate claim semantics.

This repository is a documentation and investigation starting point. **It does not yet contain an automated end-to-end runner or CI.** Follow the linked project instructions for the exact selected revisions; inspect scripts before running them. Build and test commands can modify their working directory, invoke network operations and consume substantial resources. Never run an adapter that rewrites reports against an active checkout: use a disposable consumer copy.

### Reference pair

The initial source links refer to a **historical reference pair**, not a recommendation to use stale code for every run:

| Repository | Reference commit |
|---|---|
| `codeql-ucode` | `7a1ded90962cc85a3e3a94949584c64214426aed` |
| `codeql-openwrt` | `a8bdef3c22c8d5ba9999baa978052b59bd22907e` |

When you start a new run, choose and record both commits explicitly. Fetch the branches first, then create detached checkouts at the chosen full SHAs in a private workspace. For example, after cloning each project into `work/codeql-ucode` and `work/codeql-openwrt`:

```sh
git -C work/codeql-ucode fetch origin
git -C work/codeql-openwrt fetch origin
git -C work/codeql-ucode checkout --detach <ucode-commit>
git -C work/codeql-openwrt checkout --detach <openwrt-commit>
git -C work/codeql-ucode rev-parse HEAD
git -C work/codeql-openwrt rev-parse HEAD
```

Replace the placeholders; do not paste the example unchanged. Record dirty state, tools/versions, fixture or corpus pins, commands and actual outcomes. Recheck the relevant source contracts and existing issues at those commits: the reference pair may differ from current `main`. Comparing different pairs requires an explicit delta review; an earlier pass does not automatically transfer.

## Optional model roles

For model-assisted work, keep the split simple:

- **Luna:** bounded mechanical collection, inventories, mapping paths to existing tests, and organizing run receipts. Check its output against the actual sources or commands.
- **Terra:** coordinate the paired pins and isolated runs, verify claims and reproduce candidate results, reconcile overlap with existing issues, and maintain the ledger.
- **Sol:** assess difficult semantic questions, choose discriminating controls, judge evidence boundaries, and synthesize the strongest unresolved coverage questions.

These are task roles, not separate mandatory stages or a requirement to run three models for every claim. Start with the simplest useful workflow. Resolve and smoke-test the desired model route at execution time; do not silently substitute another model. A second pass by the same model is fresh review, not independent-model corroboration.

## Relationship to the projects

This is an incubation workspace, not a submodule or a new authoritative implementation. Reuse existing project tests and issues. As the work matures, move producer-only regressions to `codeql-ucode` and consumer-only regressions to `codeql-openwrt`; decide separately where genuinely paired integration tests belong. Do not duplicate a finding already owned by an open issue.
