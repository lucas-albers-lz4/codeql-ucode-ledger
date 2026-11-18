# Claim 004: bounded builtin `system` shadowing

**Status: Demonstrated for the bounded run recorded below.**

## Claim to investigate

For the pinned `setBlockDetect` source-observation controls, the actual
`SetBlockDetectEffectTable.ql` reports the expected direct literal `system`
call sites whose relevant visible binding is the builtin, while excluding the
corresponding locally shadowed or formal-parameter call sites. The check is
limited to the named fixture shapes and exact rows, not a complete scope or
call-target engine.

## Starting points and dependencies

- [Query and contract](https://github.com/lucas-albers-lz4/codeql-ucode/blob/d3588ca6821fe983d240fcbb2e80692fabcc6aab/docs/m4-setblockdetect-effect-table.md),
  [focused smoke](https://github.com/lucas-albers-lz4/codeql-ucode/blob/d3588ca6821fe983d240fcbb2e80692fabcc6aab/scripts/m4-setblockdetect-effect-table-smoke.sh),
  and [lexical system smoke](https://github.com/lucas-albers-lz4/codeql-ucode/blob/d3588ca6821fe983d240fcbb2e80692fabcc6aab/scripts/m4-system-lexical-smoke.sh).
- In the pinned sibling-shadow fixture, the calls on lines 8 and 14 are
  expected positives; shadowed calls on lines 5 and 12 are controls. A separate
  formal-parameter fixture has a shadowed call on line 4. Reconfirm source,
  coordinates and query contract at the selected revision before running.
- Existing historical smoke and mutation notes are starting points, not this
  ledger's fresh run. Broader gated query work belongs to
  [ucode #54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54).

## Evidence required

1. Pin the producer, all fixture bytes and tools. Inspect the model and derive
   exact expected full rows and multiplicity from source before query output.
2. In a fresh owned database verify each intended file's exact extraction
   identity and zero errors, then run and decode the real query.
3. Compare all named columns and locations. Confirm the same command and
   method appear in valid, extracted shadowing controls, so their absence
   tests binding rather than a different command or failed extraction. Retain
   a positive sibling in the same run.
4. Record commands, outcomes and reviewed evidence; inspect existing tests and
   issues before proposing changes upstream.

## Boundaries and run record

The model approximates lexical bindings and source ordering; it does not prove
runtime builtin identity, global reassignment behavior, registration,
reachability, authorization or completeness for all scopes. Nested functions
are syntactically contained by this query. See the bounded run below.

### Run: 2026-11-18 UTC

**Status: Demonstrated for the named fixture shapes.** In the disposable
producer at `d3588ca6821fe983d240fcbb2e80692fabcc6aab`, with CodeQL 2.27.4,
ran `bash scripts/m4-setblockdetect-effect-table-smoke.sh` using the isolated
home and previously built pack from claim 001; exit 0. The script created a
fresh database and ran the actual diagnostics and table query. Its complete
expected rows were established from the fixture and query before running.

The [extracted identities](../evidence/004-20261118/extracted.csv) contain
exactly all 14 intended fixtures and [errors](../evidence/004-20261118/errors.csv)
contains no rows. The [table](../evidence/004-20261118/effects.csv) contains
exactly the five expected full rows: the real source, two positive fixtures,
and the sibling fixture's unshadowed calls at `8:7–8:54` and `14:5–14:52`.
It excludes that same fixture's locally shadowed calls at lines 5 and 12 and
the formal-parameter call at line 4. These controls retain the same method,
call and literal command; the eligible positive siblings show that absence
is not an empty or failed extraction. Sibling fixture SHA-256
`97353f888f4663bd7cd7b2cf5a7d697121c81d7b88dad3a46ac848646a7c2890`;
formal fixture SHA-256
`14af49d0d4c2653e5e064aa7fd8d9eef357eb5684666c832b0a0b7e1bf567b26`.
The temporary prefix in the reviewed extracted CSV is normalized; raw output,
database and log are local under ignored `work/`. This does not establish
runtime identity or general lexical resolution.
