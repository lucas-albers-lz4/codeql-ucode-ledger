# Claim 011: same-file argument-to-parameter experimental flow

**Status: Demonstrated for the named smoke fixture.**

## Claim and boundary

In the pinned `ssa_pos` fixture, the experimental `JumpLocal.ql` smoke reports
the second argument reaching the used `b` formal's SSA read for the two
same-file identifier and member-property declaration shapes named below; it
does not report a corresponding jump-local row for unused formal `a`. This is
an experimental query over the represented nodes, not production taint,
`path_found`, a general call graph or evidence that a member call dispatches
at runtime. Imported `luci.sys` call resolution remains outside this claim.

## Run: 2026-11-18 UTC

Producer `d3588ca6821fe983d240fcbb2e80692fabcc6aab`, CodeQL 2.27.4. The
fixture source shows `formal_order(a,b)` and `member_order(a,b)` return `b`,
with both called using two positional arguments. The separately documented
[contract](https://github.com/lucas-albers-lz4/codeql-ucode/blob/d3588ca6821fe983d240fcbb2e80692fabcc6aab/docs/m4-jump-local.md)
expects `1:b` for both and no `a` SSA read. Fixture `ssa_pos` SHA-256
`9c37c2621a10c76afe4ae211a38bbd8cb96b0e8fada60b37b4a8c00a993f37bb`;
LuCI fixture SHA-256
`6f9d972958d9cfb8a7ba421f38f0a5b03718ffeb0e30d460b64c9faf725fc54e`.

In the isolated producer clone, ran `HOME=<isolated-home> bash
scripts/m4-jump-local-smoke.sh`; exit 0. It compiled the experimental and
production queries, checked that production still imports Models and that
`jumpStep` is not wired into `localFlowStepImpl`, built a fresh database, and
verified [exact extracted identities](../evidence/011/extracted.json) and
[zero errors](../evidence/011/errors.json). The actual
[results](../evidence/011/results.csv) include exactly two `jump-local` rows
for `ssa_pos`: `1:b from formal_order` and `1:b from member_order`. The
successfully extracted fixture itself supplies both used `b` positives and
unused `a` near misses. The smoke also observed its named LuCI and parameter
controls. It does not prove all absent flows or runtime callees. Reviewed
extraction output normalizes the local checkout prefix; raw log and database
remain local under ignored `work/`.

Broader DataFlow and imported-callee limitations are tracked by
[ucode #50](https://github.com/lucas-albers-lz4/codeql-ucode/issues/50) and
[#49](https://github.com/lucas-albers-lz4/codeql-ucode/issues/49); compare
[claim 005](005-imported-callee-boundary.md).
