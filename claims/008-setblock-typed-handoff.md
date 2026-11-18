# Claim 008: setBlockDetect typed producer–consumer handoff

**Status: Demonstrated for the pinned pair and current consumer state.**

## Claim and scope

The actual query table and extraction diagnostics for the pinned source can
be passed to the real producer's opt-in typed exporter, and its actual neutral
record can be passed to the real consumer's typed adapter. The consumer
revalidates its policy context and updates the expected retained effects while
preserving unrelated records. Invalid observation and policy-bearing typed
input are rejected. This is a bounded source observation, not runtime,
interprocedural flow or authorization evidence.

## Run: 2026-11-18 UTC

Producer `d3588ca6821fe983d240fcbb2e80692fabcc6aab`; consumer
`a8bdef3c22c8d5ba9999baa978052b59bd22907e`; CodeQL 2.27.4 and Python 3.15.2.
The fresh table from [claim 007](007-setblock-csv-handoff.md), with the exact
source, routing and diagnostics from [claim 002](002-getblock-query.md), was
passed to `python3 -B tools/export_setblock_detect.py --csv <actual-table>
--extracted <actual-extracted> --errors <actual-errors> --source-root
<actual-source-root> --lock <consumer-corpus-lock>`. Exit 0. The supplied raw
lock SHA-256 was
`b4cbdabb76df90a807aba7d42ae675198c7b7b09c3b84db259a3a4c941b0ea9a`.
The actual [typed JSON](../evidence/008/typed.json) has exactly one unassessed
record, expected source location and unknowns, and matches the producer's
versioned complete expected fixture byte-for-byte; SHA-256
`5c619d5aa3566c5296080b0a9be7072b38d6eb7a98eae647d68c5dcf09b2b59b`.
The fixture match is a contract comparison; the actual exporter invocation and
fresh query provide this run's provenance. Feeding the exporter a table with
its start line changed from 532 to 533 exited 1 and produced no JSON.

The [consumer runner](../evidence/008/run-typed-consumer.py) made isolated
no-hardlink copies and passed that actual JSON to `python3 -B -m
policy.setblock_table --typed-json <actual-typed-json> --source-root
<actual-source-root>`. Exit 0. Both target records were updated to
`step3:setblock-typed-import-v1` with the expected source span, independently
assessed mounts expectation and primary/supplementary grant references;
unrelated rows, grants and policy decisions were preserved. A second typed
import was byte-idempotent. A fresh copy rejected a modified producer record
claiming `intended_access` and left effect and policy artifacts unchanged. On
the typed-imported copy an actual attempt to import the CSV exited 1 with
`typed-to-CSV downgrade is not supported`, leaving those artifacts unchanged.
The [summary](../evidence/008/summary.json) gives artifact hashes and errors;
raw local logs and clones are ignored under `work/`.

The [producer](https://github.com/lucas-albers-lz4/codeql-ucode/blob/d3588ca6821fe983d240fcbb2e80692fabcc6aab/docs/interchange.md)
and [consumer](https://github.com/lucas-albers-lz4/codeql-openwrt/blob/a8bdef3c22c8d5ba9999baa978052b59bd22907e/docs/setblock-typed-import.md)
contracts say supplied hashes and records do not authenticate CodeQL
execution. This ledger preserves the observed local chain, not cryptographic
attestation. The consumer policy assessment comes from independent policy
context; it is not contained in the producer's unassessed observation.
Broader interchange work remains owned by
[ucode #55](https://github.com/lucas-albers-lz4/codeql-ucode/issues/55) and
[OpenWrt #65](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/65).
