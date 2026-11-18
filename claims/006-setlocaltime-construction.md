# Claim 006: `setLocaltime` source-construction evidence

**Status: Demonstrated for the bounded fresh producer–consumer observation below.**

## Claim to investigate

For a pinned source and compatible producer–consumer pair, a fresh producer
query yields the exact six-row, 41-column source-construction observation,
and the actual consumer accepts it with its own source oracle and matching
context, producing the intended bounded annotation. The six rows describe one
construction, not six calls. First evaluate whether existing historical
artifacts can support a narrower claim before deciding to repeat the paired run.

## Starting points and dependencies

- [Producer contract and controls](https://github.com/lucas-albers-lz4/codeql-ucode/blob/d3588ca6821fe983d240fcbb2e80692fabcc6aab/docs/m4-setlocaltime-construction.md)
  and [consumer contract and historical run](https://github.com/lucas-albers-lz4/codeql-openwrt/blob/a8bdef3c22c8d5ba9999baa978052b59bd22907e/docs/setlocaltime-construction-provisional.md).
- The consumer document describes a paired run and owner acceptance with a
  disclosed interpreter-command deviation; the independent reviewer marked
  formal acceptance `INCOMPLETE`. It says the output report is not included.
  These qualifications must accompany any reuse of that evidence.
- [ucode #54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54) and
  [OpenWrt #64](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/64)
  track broader gated work.

## Evidence required

1. Inventory accessible actual run artifacts, exact pins, source, independent
   consumer oracle, diagnostics, commands and reviewer disposition. Distinguish
   documentary assertions from inspectable receipts; do not treat missing
   output as a pass or historical evidence as a current run.
2. If a fresh run is warranted, pin both revisions and compatible source and
   context. Establish exact full rows and multiplicity independently, including
   ordered field/slot associations, then verify extraction, routing and errors.
3. Run the producer and pass its actual decoded output and diagnostics to the
   real consumer with its own oracle in isolated checkouts. Verify the bounded
   annotation, linked identities and invalid or wrong-identity controls.
4. Record actual commands and results, deviations and any unavailable evidence.
   A successful fixture or offline consistency check alone is not a live run.

## Boundaries and run record

This is a source-shape and consumer interpretation claim, not a sanitizer,
no-path, authorization, runtime or broad taint claim. Reflective writes and
import side effects remain unresolved. See the investigation and fresh run below.

### Investigation and fresh paired observation: 2026-11-18 UTC

**Status: Demonstrated for the bounded source-construction and consumer run
below.** The historical consumer document describes its earlier paired run
and its owner-accepted deviation, while the independent reviewer marked formal
acceptance `INCOMPLETE`. The output report and underlying historical receipts
were not found in the inspected project snapshots or this workspace, so those
documentary assertions are not treated as independently inspected artifacts.

For this new run, producer `d3588ca6821fe983d240fcbb2e80692fabcc6aab` and
consumer `a8bdef3c22c8d5ba9999baa978052b59bd22907e` used the source and clean
single-file database from [claim 002](002-getblock-query.md). CodeQL 2.27.4
ran `ql/src/m4/SetLocaltimeConstructionTable.ql` against that database and
`codeql bqrs decode --format=csv` produced the actual
[table](../evidence/006/table.csv); both commands exited 0. The producer's
source-first oracle verifier also exited 0. There are six 41-column rows,
representing the one source construction with slots year, mon, mday, hour,
min and sec. The actual table SHA-256 is
`d11882e671c1842f5c9f30b711e677bfa01a05cbdae276aceb8792a883715523`.

From the isolated, clean consumer snapshot, invoked `python3 -B -m
policy.setlocaltime_construction --table <actual-table> --extracted
<claim-002-extracted.csv> --errors <claim-002-errors.csv> --source-root
<claim-002-source-root> --format json`. Exit 0; its consumer-owned oracle and
context accepted the inputs and the actual [annotation](../evidence/006/consumer.json)
retains the six slots, historical effect and taint identities, primary and root
grant references, and unauthenticated deny decision. It reports
`execution_verified: false`; it makes no new policy assessment. The annotation
SHA-256 is `1704aa46a9d60e9ee260f681d077ebaf40b6cfc0cfd24524bf43efeef0b656c6`.
A copy of the table with its first field name changed to `month` was passed to
the actual consumer: exit 1, empty stdout, and `source construction
identity/slot multiset mismatch`. An initial attempted control accidentally
used a nonexistent relative input path and was rejected for missing input;
the corrected wrong-field control is the result just described. Producer
query controls were not rerun here, so this result does not expand the source
shape beyond the pinned positive. Logs and raw BQRS remain local under ignored
`work/`; the checked-in table and annotation are exact output bytes.
