# Claim 005: `setInitAction` imported-callee boundary

**Status: Partial — source-to-call observation demonstrated; fresh retained interpretation not established.**

## Claim to investigate

On an exactly pinned LuCI fixture, the producer's actual imported-callee query
observes the supported `request.args` source shape reaching the `init_action`
call imported from `luci.sys`, and its retained interpretation remains
inconclusive about the imported callee body and downstream sink. Determine the
exact source/call identities and multiplicity from source and query before
asserting results; do not assume that the historical report's single record
maps one-to-one to query rows.

## Starting points and dependencies

- [Imported-callee contract](https://github.com/lucas-albers-lz4/codeql-ucode/blob/d3588ca6821fe983d240fcbb2e80692fabcc6aab/docs/m4-imported-callee.md),
  [query](https://github.com/lucas-albers-lz4/codeql-ucode/blob/d3588ca6821fe983d240fcbb2e80692fabcc6aab/ql/src/m4/ImportedCalleeTaint.ql),
  [smoke](https://github.com/lucas-albers-lz4/codeql-ucode/blob/d3588ca6821fe983d240fcbb2e80692fabcc6aab/scripts/m4-imported-callee-smoke.sh),
  and [historical record](https://github.com/lucas-albers-lz4/codeql-ucode/blob/d3588ca6821fe983d240fcbb2e80692fabcc6aab/docs/m4-imported-callee-findings.json).
  The existing smoke checks a message substring, not exact row identity.
- [ucode #50](https://github.com/lucas-albers-lz4/codeql-ucode/issues/50) and
  [#54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54) own the
  broader data-flow and query work.

## Evidence required

1. Pin source bytes, revision and tools; inspect query predicates and the
   source to establish independently expected source and call spans and row
   multiplicity. Identify whether the historical record's assumptions match
   the actual extraction set used in this run.
2. Verify exact selected and successfully extracted identities and diagnostics
   in a fresh database; run and decode the real query with entity locations.
3. Design a valid, successfully extracted near miss that reaches the relevant
   predicate and differs only in a supported property, alongside a positive.
   Check the implementation before selecting the control: `importedFrom` is
   a same-file named-import test, not proof of lexical binding. If an adequate
   control cannot be established, record partial evidence and the uncertainty.
4. Separately check the actual record or interpretation for `inconclusive` /
   `unresolved_call`; a query message alone does not prove a consumer retained
   that status. Record provenance and the limits of any historical artifact.

## Boundaries and run record

A source-to-call observation is not resolution of the imported body, a
confirmed downstream sink, `path_found`, `no_path`, runtime execution or an
authorization conclusion. A separate sys.uc extraction does not by itself
resolve the call. See the investigation below.

### Investigation: 2026-11-18 UTC

**Status: Partial.** At producer `d3588ca6821fe983d240fcbb2e80692fabcc6aab`,
CodeQL 2.27.4 ran the actual query against the clean, single-LuCI database
created for claim 002. Its source and diagnostic evidence are recorded there.
The query exited 0; [decoded entities](../evidence/005/real-observations.json)
show exactly two rows for the two direct argument sources at `85:28–85:44`
and `85:47–85:65`, each associated with the same `init_action` call at
`85:16–85:66`. The pinned source imports that name from `luci.sys`. These are
two query rows, whereas the committed historical record is one record.

A fresh separate [control run](../evidence/005/run-controls.py) used identical
minimal valid source shapes except for the named import module (`luci.sys`
versus `fs`). Both exact inputs [extracted](../evidence/005/extracted.json)
with [zero errors](../evidence/005/errors.json); the actual query produced
[one positive row](../evidence/005/observations.json) and no `fs` row. This
specifically tests the query's `moduleName != "fs"` condition, not lexical
binding or exclusion of every other module. The local temporary prefix in JSON
is normalized; raw artifacts and commands are in ignored `work/`.

The [committed historical record](https://github.com/lucas-albers-lz4/codeql-ucode/blob/d3588ca6821fe983d240fcbb2e80692fabcc6aab/docs/m4-imported-callee-findings.json)
labels the result `inconclusive` / `unresolved_call` and explicitly says its
M3 extraction set did not include the helper body. The current query run also
extracted only LuCI, but no fresh process generated or imported that historical
record. Thus the source-to-call observation is demonstrated; fresh retained
interpretation and consumer handling are not. The query's message is not proof
of resolution or of a downstream sink.

### Can the existing projects produce a fresh retained interpretation?

**Finding: no such path was identified at the pinned pair.** The producer's
[interchange documentation](https://github.com/lucas-albers-lz4/codeql-ucode/blob/d3588ca6821fe983d240fcbb2e80692fabcc6aab/docs/interchange.md)
explicitly says the classified JSON arrays are committed snapshots, not output
automatically regenerated by the queries or snapshot tests. The imported
callee smoke runs the query and checks a message; it does not write the typed
record. The opt-in typed exporter described in that document is for
`setBlockDetect`, not imported callees. Search of the pinned producer found
references to the imported-callee record in documentation, preservation tests,
fixtures and smoke, but no fresh query-to-record exporter.

The pinned consumer's [contract](https://github.com/lucas-albers-lz4/codeql-openwrt/blob/a8bdef3c22c8d5ba9999baa978052b59bd22907e/docs/pack-contract.md)
describes an offline interchange validator, not an imported-callee query-output
adapter. Its `reports/m4-imported-callee-findings.json` is a separate retained
copy, differing from the producer's committed snapshot in assumptions,
evidence references and wording of unknowns; neither was regenerated in this
investigation. On 2026-11-18 UTC, in the disposable consumer checkout, ran
`python3 -B -m policy.interchange_contract --snapshot --ucode-root
<disposable-producer-checkout>`; exit 0. The [output](../evidence/005/snapshot-validation.txt)
reports 19 records in five arrays validated as a **historical snapshot, not
live conformance**. The validator read the producer's committed docs, not the
fresh query results or the separate consumer report. It establishes contract
compatibility only within its documented scope, not query execution, source
truth, or fresh record production. The check does not write a retained record.

A ledger author can document a fresh bounded interpretation, as the preceding
investigation does, but that is not a newly emitted producer record or an
observed consumer import. To establish that stronger claim would require a
separately designed query-output-to-record interface and a real consumer path,
with source and diagnostic identity, an independent expectation, provenance,
controls, and explicit handling of the two query rows versus the historical
single record. That is possible work, not an existing capability demonstrated
here; coordinate any eventual change with
[ucode #55](https://github.com/lucas-albers-lz4/codeql-ucode/issues/55) and
[OpenWrt #65](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/65).
The unresolved imported-call modeling remains owned by
[ucode #50](https://github.com/lucas-albers-lz4/codeql-ucode/issues/50).
The claim remains partial; no `path_found`, `no_path`, policy grant, or runtime
conclusion follows from these observations.
