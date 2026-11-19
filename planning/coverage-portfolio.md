# Coverage claim portfolio

Inventory date: 2026-11-18 UTC. This is a prioritized working map, not a
coverage denominator or a new test result. See [the later pinned-source batch](batch-20261118.md) for newer revisions and claims 015–016. It draws on isolated snapshots of
[ucode `d3588ca`](https://github.com/lucas-albers-lz4/codeql-ucode/tree/d3588ca6821fe983d240fcbb2e80692fabcc6aab)
and [OpenWrt `a8bdef3`](https://github.com/lucas-albers-lz4/codeql-openwrt/tree/a8bdef3c22c8d5ba9999baa978052b59bd22907e),
and the open issue titles/bodies inspected on that date. These were the remote
`main` heads when checked; assess deltas and issue changes for any later run.
The projects remain the owners of their contracts, implementation and issues.
Claim 012 additionally records a fresh declaration-query-to-consumer comparison
at producer `094a163` / consumer `faf95a4`; it is scoped to that run and does
not exercise the separate retained direct-exec grant-join path.

## Selection heuristic

Start with a named analysis or decision and trace its prerequisites. Prefer a
claim when (1) its outcome would clarify a consequential uncertainty,
(2) an exact expected identity and a valid discriminating control can be
established independently, and (3) existing evidence can be reused or a run
is proportionate. Priorities below are judgment calls, not numerical coverage
scores. Do not promote historical tests or fixture tables to fresh paired runs.
When a question is already owned, link the issue and document the boundary
instead of creating a duplicate finding. Revise the list when project changes
make an assumption or priority stale.

## Representative paths

| Path and why it matters | Evidence chain and present ledger state | Next useful question / existing ownership |
|---|---|---|
| **getBlockDevices**: first small producer–consumer trace, direct imported `popen` source shape. | [001](../claims/001-staged-root-extraction.md) demonstrates one selection/extraction run; [002](../claims/002-getblock-query.md) and [003](../claims/003-getblock-handoff.md) now have bounded fresh query and handoff runs. The table records syntactic containment and an `fs` import, not lexical binding or registration. | Refresh against a newly selected revision pair when needed. [ucode #54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54), [ucode #55](https://github.com/lucas-albers-lz4/codeql-ucode/issues/55), and [OpenWrt #65](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/65). |
| **setBlockDetect**: similar handoff but tests a different language dependency, builtin `system` versus visible shadowing. | [004](../claims/004-system-shadowing.md) demonstrates a narrowly scoped language/model check through the real table query. A separate typed exporter, adapter and offline handoff checker exist. | Fresh [CSV](../claims/007-setblock-csv-handoff.md) and [typed](../claims/008-setblock-typed-handoff.md) handoffs now have bounded runs; the existing [handoff checker](https://github.com/lucas-albers-lz4/codeql-openwrt/blob/a8bdef3c22c8d5ba9999baa978052b59bd22907e/docs/setblock-handoff-checks.md) checks consistency but does not prove execution or freshness. |
| **setInitAction**: important boundary for request arguments reaching an imported helper. | [005](../claims/005-imported-callee-boundary.md) demonstrates the bounded source-to-call observation and remains partial for fresh retained interpretation. The documented same-file experimental jump does not resolve this imported target. | The existing imported-callee smoke checks a message substring, not exact source/sink identities or a complete negative; design controls before treating it as sufficient. [ucode #50](https://github.com/lucas-albers-lz4/codeql-ucode/issues/50) and [#54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54) own broader work. |
| **setLocaltime**: a richer six-row source construction and consumer with an independent oracle. | [006](../claims/006-setlocaltime-construction.md) records a bounded fresh paired observation and consumer rejection control. The existing consumer documentation records a paired run with an owner-accepted deviation and independent review marked `INCOMPLETE`; it does not provide the output report. | Historical raw artifacts were not found in the inspected snapshots or workspace; the fresh run is separately recorded. Do not silently promote the historical run or imply that six rows are six calls. [ucode #54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54), [OpenWrt #64](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/64). |


Additional bounded inventory paths: [009](../claims/009-luci-sys-status.md)
checks the two named `luci.sys` status-helper and wrapper shapes; [010](../claims/010-ubus-call-inventory.md)
checks direct `ubus.call` syntax. [011](../claims/011-same-file-jump-local.md)
checks an experimental same-file flow shape; [012](../claims/012-backend-declaration-comparison.md)
compares backend declarations with a pinned grant catalog, and [013](../claims/013-getfeatures-direct-calls.md)
inventories direct `getFeatures` calls. [014](../claims/014-fs-binding-guard.md)
checks selected conservative `fs` binding controls. None establishes runtime binding or a
cross-file taint path. These are examples selected for existing fixtures and
discriminating controls, not an inventory of all candidate analyses.

These paths overlap in the pinned LuCI fixture; they are not a representative
sample of all OpenWrt software or ucode syntax. The inventory deliberately
separates source extraction, model/query behavior, consumer handling and policy
interpretation. A successful earlier step is a prerequisite, not proof of a
later step. Deferred markup and dispatcher coverage remain owned by
[ucode #56](https://github.com/lucas-albers-lz4/codeql-ucode/issues/56),
[#57](https://github.com/lucas-albers-lz4/codeql-ucode/issues/57) and
[#58](https://github.com/lucas-albers-lz4/codeql-ucode/issues/58)
and [OpenWrt #68](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/68)
and [#70](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/70); do
not infer coverage from their presence in this list.

## Working order and refresh

1. Claim 005 has no identified existing fresh query-to-record path at the pinned
   pair. Keep the source-to-call evidence partial and revisit an interface only
   if it serves a concrete analysis need; do not relabel the historical snapshot.
2. Keep the completed setBlockDetect CSV and typed handoffs scoped to their
   recorded runs; revisit them when their contracts or selected revisions change.
3. On refresh, record the new SHAs, inspect changes to selected queries,
   models, fixtures, adapters and issue disposition, and rerun affected claims.
   Prior evidence remains scoped to its original pins.
