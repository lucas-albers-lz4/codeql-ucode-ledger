# Claim 012: LuCI backend declarations versus grant catalog

**Status: Demonstrated for this pinned comparison, with the oracle qualification below.**

## Claim and boundary

The actual `LuciBackendDeclarations.ql` output for the pinned LuCI source can
be compared by the actual OpenWrt consumer to its source and grant fixtures.
The output identifies 21 syntactic declaration rows, 18 represented methods
and three names with no current matching materialized grant row. A missing
row is not a denial, an ACL defect, a runtime registration, a reachability
claim or proof of a security gap. This claim does not establish a complete
inventory for arbitrary or unsupported ucode source.

## Run: 2026-11-18 UTC

Producer `d3588ca6821fe983d240fcbb2e80692fabcc6aab`; consumer
`a8bdef3c22c8d5ba9999baa978052b59bd22907e`; CodeQL 2.27.4 and Python 3.15.2.
The pinned source and exact clean extraction diagnostics are from the fresh
single-file database in [claim 002](002-getblock-query.md). Ran
`codeql query run ql/src/m4/LuciBackendDeclarations.ql` on that database with
`--threads=1 --ram=2048` and decoded its BQRS to CSV; both exited 0. Actual
[table](../evidence/012/table.csv) SHA-256:
`245ad2dc1aedc9d4e0d41d83fcb0246a0990bcd70b5d0a35e1cb65100bfa8996`.
Query SHA-256:
`58d11ee8bf4f27db2dec4e34292d5155874f035bac8b98121c9ee8d85225a298`.

From the isolated consumer snapshot, invoked `python3 -B -m
policy.backend_declarations --table <actual-table> --extracted
<actual-extracted> --errors <actual-errors> --source-root <actual-root>`;
exit 0. Its actual [report](../evidence/012/report.json) lists 21 declarations,
18 represented methods, 38 matching grant rows, and `getInitList`,
`getUSBDevices`, `setInitAction` as source-only. A duplicated table row was
passed to the actual comparator: exit 1, empty stdout and `source identity/span
multiset mismatch`. The consumer is non-writing. Its report's producer and
consumer revision fields are historical reference values, not the actual
revision pins or proof of execution; the actual pins are recorded above.

The consumer checks a separately stored source fixture and grant-identity
snapshot. A pin-specific indentation scan performed during this investigation
matched all 21 source fixture identities and spans to the actual source. This
is not a general parser and was not blinded: the author had access to the
fixture, query and prior reports. The grant fixture is a frozen catalog map,
not an independent oracle of ACL correctness. Do not treat this comparison as
proof of runtime semantics, independent policy correctness or general analysis
completeness. The [consumer contract](https://github.com/lucas-albers-lz4/codeql-openwrt/blob/a8bdef3c22c8d5ba9999baa978052b59bd22907e/docs/luci-backend-comparison.md)
and [producer contract](https://github.com/lucas-albers-lz4/codeql-ucode/blob/d3588ca6821fe983d240fcbb2e80692fabcc6aab/docs/m4-luci-backend-declarations.md)
record further limitations. Existing broad ownership remains with
[ucode #54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54) and
[OpenWrt #64](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/64).

### Fresh producer-to-consumer handoff: 2026-11-18 UTC

**Demonstrated for the pinned source and comparison contract.** This follow-up
used clean detached checkouts of producer `094a163db1138c83820197180501bd7c78bd9051`,
consumer `faf95a4934ce0ad73a9d361742ab57f9eb514ea8`, and LuCI
`b2e0be4b46ec0fd43394c081fa7c50657af14011`. The lock, profile, grants and
consumer source/grant-oracle hashes are in the
[portable receipt](../evidence/017-20261118/commands-and-timings.json). The
actual upstream `luci` source was reconstructed at
`usr/share/rpcd/ucode/luci` from the locked LuCI checkout; its SHA-256 is
`6f9d972958d9cfb8a7ba421f38f0a5b03718ffeb0e30d460b64c9faf725fc54e`.
This was not a package build. Before querying, the consumer oracle's 21 method
keys, `call: function` starts, and closing lines were checked against those
pinned bytes. The oracle is not blinded or independently re-reviewed here.

The current producer query hash remains
`58d11ee8bf4f27db2dec4e34292d5155874f035bac8b98121c9ee8d85225a298`.
A fresh database routed the exact one-file input as
`rpcd_raw_mode_full_path` / `plain_route_selected`; successful extraction had
one exact file and the error query had zero rows. The actual query and decode
exited 0 and produced 21 unique rows matching the source-first identity/span
multiset. Table SHA-256:
`245ad2dc1aedc9d4e0d41d83fcb0246a0990bcd70b5d0a35e1cb65100bfa8996`.
The [actual decoded table](../evidence/017-20261118/table.csv),
[normalized diagnostics](../evidence/017-20261118/extracted.csv),
[errors](../evidence/017-20261118/errors.csv),
[routing](../evidence/017-20261118/routing.json), and
[pre-query expectations](../evidence/017-20261118/prequery-expectations.json)
are retained. Temporary paths are normalized in the diagnostic/routing copies;
manifest hashes link those copies to raw run artifacts under ignored `work/`.

Passed the actual table, actual successful-file/error CSVs and matching source
root to `python3 -B -m policy.backend_declarations` in the current disposable
consumer checkout. Exit 0; the
[consumer report](../evidence/017-20261118/consumer-report.json) contains 21
declarations, 18 represented methods, 38 grant rows, three
source-only methods (`getInitList`, `getUSBDevices`, `setInitAction`) and no
grant-only methods. Its `getFeatures` declaration is associated with the
unauthenticated and root grant IDs in the current catalog. A
[duplicate-row control table](../evidence/017-20261118/table-duplicate-row.csv)
changed only table multiplicity; the actual comparator exited 1, emitted no
success stdout, and reported `source identity/span multiset mismatch`.
Consumer context files and worktree were unchanged. The report's
`producer_revision_reference` (`d54c17a…`) and `consumer_baseline_reference`
remain historical constants, not the actual run pins or execution evidence;
the local commands, outputs and statuses are recorded separately.

The producer extractor's `cargo test` passed 10 tests. On the current consumer,
16 backend-comparison tests and 33 handler-effect-join tests also passed. The
latter cover the consumer change since its previous batch pin, but they exercise
retained `join_policy_grants` rows, not this fresh declaration table. The
consumer delta since `c45d0c4…` changed only that test module; its comparator,
grants, lock, profile and two declaration oracles were unchanged. Current
[ucode #54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54),
[OpenWrt #64](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/64),
and [OpenWrt #113](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/113)
keep broader query-family promotion and retained grant-join work in their
existing owners. This run closes none of them.

Build, pack-install, extraction, query, consumer and focused-test timings, peak
RSS where measured, exact commands and the setup-only failed legacy patch
attempt are documented in the receipt. CodeQL was 2.27.4; Rust/Cargo 1.100.0;
Python 3.15.2. The run used a copied Cargo cache but run-owned databases,
CodeQL package cache and output paths. The consumer comparison is non-writing;
this is evidence of a local fresh handoff, not cryptographic attestation,
policy correctness, runtime registration, reachability or authorization.
