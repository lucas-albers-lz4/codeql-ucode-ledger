# Claim 002: getBlockDevices source-table query

**Status: Proposed — not yet demonstrated in this ledger.**

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
4. Use a relevant wrong-module, shadowing, or wrong-command near miss that is valid and successfully extracted. Confirm the actual predicate/consumer contract before selecting the control: do not claim broader lexical or literal handling than the pinned implementation supports. Include an eligible positive witness; an empty negative by itself is insufficient.

## Boundaries

This is a bounded syntactic source observation. It does not prove callback registration, runtime execution, a taint path, or an authorization violation. Unsupported/no-match cases remain unknown. No consumer execution is claimed here.

## Run record

None yet. Use [the template](TEMPLATE.md) to record actual evidence.
