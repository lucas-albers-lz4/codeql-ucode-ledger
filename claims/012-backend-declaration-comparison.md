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
