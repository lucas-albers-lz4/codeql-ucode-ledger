# Claim 008: setBlockDetect typed producer–consumer handoff

**Status: Demonstrated for the two pinned runs below, not for arbitrary revisions.**

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


## Refresh: 2026-11-21

The selected decision was whether the actual typed handoff still works after
producer extraction changes. The fresh disposable producer was
`8375887ed14825dd59addbfd0df43616d9e684fb` and consumer was
`33ff29f9f311fec078be8e2df04261529cba0e65`; both were clean at selection. The
latter advanced from the preceding triage pin by a roadmap-only commit. Since
the earlier claim run the producer's extraction pipeline and schema changed;
the specific table, model, exporter and selected fixture did not. The consumer's
strict setBlock adapter and corpus lock were unchanged, while the separate
generic interchange validator changed its numeric parsing. Ucode
[#55](https://github.com/lucas-albers-lz4/codeql-ucode/issues/55) and OpenWrt
[#65](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/65) remained
open for paired contract maintenance; their shipped integration is not
reopened by this run.

The producer's checked-in fixture is a declared byte copy of LuCI
`b2e0be4b46ec0fd43394c081fa7c50657af14011`, not a newly acquired upstream
checkout. Its SHA-256 was
`6f9d972958d9cfb8a7ba421f38f0a5b03718ffeb0e30d460b64c9faf725fc54e`.
The consumer lock SHA-256 was
`b4cbdabb76df90a807aba7d42ae675198c7b7b09c3b84db259a3a4c941b0ea9a`.
The run used CodeQL 2.27.4, Python 3.15.2, Cargo 1.100.0, and the producer's
grammar pin `4a243af329fae2f4ff01e0fc80133cbab8314600` (the bootstrap modifies
its local dev dependency). There were 136 GiB available, 16 GiB memory and 10
CPUs at setup. It used fresh databases and run-local caches serially.

Before inspecting output, the pinned source and query established one expected
row for `usr/share/rpcd/ucode/luci` at `532:21–532:68`. The
[selection/routing](../evidence/008-20261121/main-routing.json),
[extracted identities](../evidence/008-20261121/main-extracted.csv), and
[errors](../evidence/008-20261121/main-errors.csv) show exactly that one
selected and successfully extracted file and zero errors. There were no
excluded or unknown identities among this explicitly staged one-file input;
no broader corpus selection is claimed. The real query produced the
[one expected row](../evidence/008-20261121/main-effects.csv).

A separate fresh database extracted exactly the sibling-shadow and
formal-parameter controls, with [no errors](../evidence/008-20261121/controls-errors.csv).
The [routing](../evidence/008-20261121/controls-routing.json) and
[identities](../evidence/008-20261121/controls-extracted.csv) show both inputs.
The [query output](../evidence/008-20261121/controls-effects.csv) contains
exactly the two independently expected unshadowed sibling calls at
`8:7–8:54` and `14:5–14:52`; the same-method, same-literal shadowed calls at
lines 5 and 12 and the formal-parameter call at line 4 produced no rows. The
[pre-run expectations](../evidence/008-20261121/expectations.json) include
fixture hashes and multiplicity. These valid extracted near misses exercise
only the named syntactic binding controls.

The real exporter consumed the actual table, extraction diagnostics, staged
source and current lock and exited 0. Its [actual typed JSON](../evidence/008-20261121/typed.json)
contains exactly one unassessed record, SHA-256
`5c619d5aa3566c5296080b0a9be7072b38d6eb7a98eae647d68c5dcf09b2b59b`.
The identical historical fixture hash is a comparison, not proof of freshness.
Changing the table's start line to 533 caused the actual exporter to exit 1
with no JSON output.

The actual JSON was passed to the real typed adapter in a no-hardlink consumer
copy; exit 0. Both [target rows](../evidence/008-20261121/consumer-targets.json)
were updated to the expected source location and mounts assessment and grant
references. The runner verified unrelated rows in the two effect artifacts
and the bytes of `policy/grants.json` and `policy/policy_decisions.json` were
preserved. A second import was byte-identical across these four artifacts.
The CSV downgrade, a record claiming `intended_access`, and an otherwise
identical typed input with numeric token `532.0` each exited 1 and left these
four artifacts unchanged. See the [consumer summary](../evidence/008-20261121/consumer-summary.json)
and [error excerpts](../evidence/008-20261121/README.md). These assertions do
not cover every file in the consumer checkout.

Separately, the consumer's [offline numeric tests](../evidence/008-20261121/numeric-tests.log)
passed all five tests (exit 0), including generic schema acceptance of
integral decimal/exponent forms and rejection of precise fractional forms.
That generic validator is distinct from the strict typed importer and the
suite is not a fresh producer handoff.

The [runners](../evidence/008-20261121/README.md) and normalized
[producer](../evidence/008-20261121/producer-commands.json) and
[consumer](../evidence/008-20261121/consumer-commands.json) receipts give
exact commands, statuses and per-step timings and maximum RSS. The successful
build took 15.39 seconds wall and 387,006,464 bytes maximum RSS; the main
index took 0.63 seconds, the effects query 2.66 seconds, the exporter 0.02
seconds, and the first consumer import 0.06 seconds. These are measured
process wall times, not full-corpus estimates; the receipts separately report
CPU and per-process peak memory. The initial network build was interrupted and
retried offline, as documented in the receipt. This observed local chain does not
cryptographically authenticate execution, establish runtime binding or
reachability, or prove authorization or policy correctness. Claim 005 remains
partial.
