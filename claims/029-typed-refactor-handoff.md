# Claim 029: strict typed handoff after validation refactor

**Status:** Demonstrated for the selected source, revisions and controls.

**Scope:** At the selected producer and consumer revisions, a fresh `setBlockDetect` source observation passes through the actual query, neutral typed exporter and the refactored strict v1 typed consumer, with valid binding controls and discriminating rejection controls.

**Out of scope:** Runtime execution or registration, authorization or policy correctness, a v2 live handoff, and arbitrary source or revision coverage.

## Revisions and decision

Producer [6010ff2c0f101f7629c6fe117a421f671c311a2b](https://github.com/lucas-albers-lz4/codeql-ucode/tree/6010ff2c0f101f7629c6fe117a421f671c311a2b) and consumer [48c6a65b7578234644c6b06780fc82ccf6d61a8b](https://github.com/lucas-albers-lz4/codeql-openwrt/tree/48c6a65b7578234644c6b06780fc82ccf6d61a8b) were clean at selection. The consumer refactored strict `validate_typed` to call `validate_typed_records` with parsed records, pinned source bytes, lock and selected corpus identity. This asks whether the previously demonstrated v1 path still accepts real fresh producer output through the changed seam; it is a regression refresh of [claim 008](008-setblock-typed-handoff.md), not a new v2 integration.

The [source-first oracle](../evidence/029-typed-refactor-handoff/ORACLE.md) fixes the checked-in LuCI byte-copy fixture, expected main and sibling-control rows, extraction identity and error expectations, and consumer controls before inspection. The consumer lock pins LuCI `b2e0be4b46ec0fd43394c081fa7c50657af14011`. Paired contract ownership remains with [ucode #55](https://github.com/lucas-albers-lz4/codeql-ucode/issues/55) and [OpenWrt #65](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/65).

## Observed run

The [portable run record](../evidence/029-typed-refactor-handoff/README.md) records exact commands, outputs, hashes, timing and isolation limits. The single main source and two controls routed as plain and extracted without reported errors. The main query returned the expected projected source row at `532:21–532:68`. The two control rows were the expected unshadowed sibling calls; same-method shadowed and formal-parameter controls were absent. These are exact projected rows, not proof of underlying entity uniqueness where projection could collapse entities.

The actual exporter consumed the fresh query table, extracted identities, diagnostics, source and lock, producing exactly one unassessed neutral record. Its unchanged bytes were passed to the real strict consumer. Both target artifacts acquired the expected source span, existing mounts assessment and grant references; unrelated rows and checked grants/policy bytes were preserved. Reimport was byte-idempotent across the four checked artifacts. The modified-span exporter control and consumer controls for policy-bearing input, `532.0`, and typed-to-CSV downgrade were rejected as expected. The record includes the full observed post-import artifacts and control results.

The producer phase took 13.39 seconds and the consumer phase 0.56 seconds on the recorded machine; neither is a corpus benchmark. HOME was inherited, and explicit run-owned caches do not establish that all writes were confined. This run does not authenticate provenance cryptographically or establish runtime behavior. Independent review matched the raw receipts to the source-first oracle and verified the actual exporter-to-consumer path.
