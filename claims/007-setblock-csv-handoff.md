# Claim 007: setBlockDetect CSV handoff

**Status: Demonstrated for the pinned pair and current retained state.**

## Claim and boundary

The pinned producer's actual `setBlockDetect` source table is accepted by the
pinned OpenWrt CSV adapter with matching source and policy prerequisites; the
expected retained record and unrelated rows survive, and invalid table or
source inputs are rejected without writing effect or policy artifacts. This
is a source-body observation, not execution, taint, or authorization proof.

## Run: 2026-11-18 UTC

Producer `d3588ca6821fe983d240fcbb2e80692fabcc6aab`, consumer
`a8bdef3c22c8d5ba9999baa978052b59bd22907e`, CodeQL 2.27.4, Python 3.15.2.
Used the fresh single-source database and diagnostics from
[claim 002](002-getblock-query.md), with fixture SHA-256
`6f9d972958d9cfb8a7ba421f38f0a5b03718ffeb0e30d460b64c9faf725fc54e`.
The source and [producer contract](https://github.com/lucas-albers-lz4/codeql-ucode/blob/d3588ca6821fe983d240fcbb2e80692fabcc6aab/docs/m4-setblockdetect-effect-table.md)
establish the expected direct literal call at `532:21–532:68`. Ran actual
`codeql query run ql/src/m4/SetBlockDetectEffectTable.ql` against that database
with `--threads=1 --ram=2048`, then decoded to CSV; both exited 0. The
[table](../evidence/007/table.csv) has exactly the independently expected
header and row, SHA-256
`9d9a1a7178e7f5fbd3cb772122fe172354004fac09ce00e91647d6b35ba9d0a0`.
[Claim 004](004-system-shadowing.md) independently exercised positive and
shadowed-source controls for this query family.

The [consumer runner](../evidence/007/run-consumer.py) created independent
no-hardlink checkouts and invoked the real `policy.setblock_table` adapter on
the actual table and matching source root. The positive invocation exited 0;
in both effect artifacts there was exactly one expected record with the
correct location, mounts assessment and mounts/root grant references. Other
rows remained ordered and unchanged; grants and decisions were unchanged.
Both artifacts were already byte-identical to the resulting current state;
the actual second import was byte-identical as well. This is a current-state
reimport, not evidence of a legacy migration or a changed initial record.

In separate clones, an altered source byte and an altered row location each
caused an actual adapter invocation to exit 1. Both effect artifacts, grants,
and decisions remained byte-identical to their initial state. The
[summary](../evidence/007/summary.json) records digests and rejection reasons.
Local raw commands, outputs and clones remain under ignored `work/`. The
[consumer contract](https://github.com/lucas-albers-lz4/codeql-openwrt/blob/a8bdef3c22c8d5ba9999baa978052b59bd22907e/docs/pack-contract.md)
assigns the intended-access assessment to separate policy expectations. The
CSV and adapter do not authenticate execution; this ledger binds the observed
local run, not cryptographic attestation. Existing broader work remains owned
by [ucode #54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54),
[ucode #55](https://github.com/lucas-albers-lz4/codeql-ucode/issues/55) and
[OpenWrt #65](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/65).
