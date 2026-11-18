# Claim 010: bounded direct `ubus.call` inventory

**Status: Demonstrated for the named pinned fixture and syntax controls.**

## Claim and boundary

For the pinned LuCI plugin and the supplied control fixture, the real
`UbusCallInventory.ql` selects the named direct `ubus.call` syntax sites and
excludes the listed near misses. It does not resolve the `ubus` receiver's
binding, model computed or optional calls, prove invocation or success, or
assess arguments, reachability, taint or authorization.

## Run: 2026-11-18 UTC

Producer `d3588ca6821fe983d240fcbb2e80692fabcc6aab`, CodeQL 2.27.4.
Independently inspected the pinned plugin's source and
[query contract](https://github.com/lucas-albers-lz4/codeql-ucode/blob/d3588ca6821fe983d240fcbb2e80692fabcc6aab/docs/m4-ubus-call.md):
the direct `ubus.call` sites occur at lines 663 and 671, and the control's
direct positive occurs at line 2. The plugin SHA-256 is
`6f9d972958d9cfb8a7ba421f38f0a5b03718ffeb0e30d460b64c9faf725fc54e`;
`ubus_call_controls` SHA-256 is
`5cac0b1745ac48f81a079b13d493fe90f4f35121ea7eb2a3fa80997a5f0d95c4`.

In the disposable checkout ran `HOME=<isolated-home> bash
scripts/m4-ubus-call-smoke.sh`; exit 0. It created a fresh database, indexed
the plugin and the control bytes copied under the extractor's `ssa_pos`
fixture name, ran the actual query, and checked exactly three messages and no
errors. Then ran `SuccessfullyExtractedFiles.ql` against that same database
and decoded it and the query's entity locations as JSON; both commands exited
0. [Extracted identities](../evidence/010/extracted.json) contain exactly
the two intended files, and [errors](../evidence/010/errors.csv) has no rows.
[Actual entity results](../evidence/010/ubus.json) identify the positive at
`2:1–2:37` and the plugin sites at `663:17–663:53` and `671:15–671:59`.

The same successfully extracted control file contains direct positive and
bare-call, different receiver/method, computed, parenthesized, nested member,
and optional-call near misses. Only the direct positive appears. This tests
these exact forms together; it does not show that a local object named `ubus`
is a real ubus receiver. Reviewed JSON normalizes its temporary prefix; raw
outputs and logs remain under ignored `work/`. Existing broader concept work
belongs to [ucode #53](https://github.com/lucas-albers-lz4/codeql-ucode/issues/53).
