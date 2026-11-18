# Claim 002: getBlockDevices source-table query

**Status: Demonstrated for the bounded run recorded below.**

## Claim to investigate

For the pinned LuCI fixture, a clean extraction followed by `GetBlockDevicesEffectTable.ql` yields the expected named-column source observation for the direct literal `popen` call inside `getBlockDevices.call`. The focused controls distinguish that source shape from relevant near misses.

## Existing starting points

- Reference producer revision: [`7a1ded90962cc85a3e3a94949584c64214426aed`](https://github.com/lucas-albers-lz4/codeql-ucode/tree/7a1ded90962cc85a3e3a94949584c64214426aed).
- [Query contract and limitations](https://github.com/lucas-albers-lz4/codeql-ucode/blob/7a1ded90962cc85a3e3a94949584c64214426aed/docs/m4-getblock-effect-table.md); [query](https://github.com/lucas-albers-lz4/codeql-ucode/blob/7a1ded90962cc85a3e3a94949584c64214426aed/ql/src/m4/GetBlockDevicesEffectTable.ql); [focused smoke](https://github.com/lucas-albers-lz4/codeql-ucode/blob/7a1ded90962cc85a3e3a94949584c64214426aed/scripts/m4-getblock-effect-table-smoke.sh).
- [Ucode #54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54) tracks the broader gated query work; do not treat this narrow observation as completion of that issue.

## Evidence to collect

1. Read the query and current focused test first. Pin the producer and exact LuCI fixture bytes; establish the independently expected full row, source path, span and multiplicity from the pinned source and documented contract, not from the resulting table.
2. Using an owned fresh database, demonstrate successful extraction of the intended input and zero unintended extraction errors. Preserve routing receipts when available.
3. Execute the real query and decode its actual output. Compare every named column and exact row identity with the expectation. Record commands, exit statuses and output artifacts.
4. Use a relevant wrong-module or wrong-command near miss that is valid and successfully extracted. The table contract does not establish general lexical resolution; a conservative shared `fs` guard excludes some competing-binding shapes (see [claim 014](014-fs-binding-guard.md)). Check the pinned predicate and exact control before expecting any particular exclusion. Confirm the actual predicate/consumer contract before selecting the control; do not claim broader lexical or literal handling than the pinned implementation supports. Include an eligible positive witness; an empty negative by itself is insufficient.

## Boundaries

This is a bounded syntactic source observation. It does not prove callback registration, runtime execution, a taint path, or an authorization violation. Unsupported/no-match cases remain unknown. No consumer execution is claimed here.

## Run record

See the bounded run below and [the template](TEMPLATE.md) for future runs.

### Run: 2026-11-18 UTC

**Status: Demonstrated for the pinned fixture and named controls.** Producer
`d3588ca6821fe983d240fcbb2e80692fabcc6aab`, CodeQL 2.27.4, Python 3.15.2,
fixture SHA-256 `6f9d972958d9cfb8a7ba421f38f0a5b03718ffeb0e30d460b64c9faf725fc54e`.
The existing extractor pack and isolated home from claim 001 were reused;
both databases and outputs were fresh. The producer's `fs` import and call
at line 481, plus the query and contract, established the expected row before
the run. The [runner](../evidence/002-003/run-producer.py) was invoked with
producer checkout and fresh run-directory arguments and exited 0. It records
all actual CodeQL commands and exit codes in the local run directory.

The installed-root database selected and successfully extracted exactly
`usr/share/rpcd/ucode/luci`, with zero extraction errors. Its
[actual CSV](../evidence/002-003/main-effects.csv) contained exactly one row:
`callback_body_call`, `getBlockDevices`, `popen`,
`/sbin/block info 2>/dev/null`, that relative path, and span `481:18–481:54`.
The CSV SHA-256 was `8ba3a5dc591c4672f5c91ac4da4060bddd2bc5e44aba0f2f8ed43cf6ad735579`.
[Routing](../evidence/002-003/main-routing.json) was captured before
finalization; [successful-file](../evidence/002-003/main-extracted.csv) and
[error](../evidence/002-003/main-errors.csv) outputs were decoded separately.

A second fresh database extracted exactly the three identified positive,
wrong-command, and wrong-import fixtures with zero errors. Only the positive
produced the expected row at `4:5–4:41`; both near misses were valid input and
reached the corresponding source-shape guards. See the
[control results](../evidence/002-003/controls-effects.csv),
[extracted identities](../evidence/002-003/controls-extracted.csv),
[errors](../evidence/002-003/controls-errors.csv) and
[routing](../evidence/002-003/controls-routing.json). Local absolute prefixes
in reviewed copies are replaced by `<PRODUCER_RUN>`; the effect CSVs and error
CSVs contain no such substitution. Full command logs, raw BQRS and databases
remain under ignored `work/` and are not portable evidence. This does not
establish binding, registration, execution, taint or authorization.
