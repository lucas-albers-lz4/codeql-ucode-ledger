# Claim 009: LuCI status wrapper and helper inventory

**Status: Demonstrated for the named pinned source shapes and controls.**

## Claim and boundaries

For the two pinned LuCI sources, `LuciSysStatusExec.ql` identifies the
`getProcessList` / `process_list` and `getConntrackList` / `conntrack_list`
source shapes with their respective fixed `popen` calls. This query matches
syntactic wrappers and helper shapes; it does not establish interprocedural
call resolution, runtime execution, taint, or policy authorization. Its
conntrack control covers the modeled fallback idiom, not all possible forms.

## Run: 2026-11-18 UTC

Producer `d3588ca6821fe983d240fcbb2e80692fabcc6aab`, CodeQL 2.27.4. In its
disposable clone, ran `HOME=<isolated-home> bash
scripts/m4-luci-sys-status-exec-smoke.sh`; exit 0. The smoke created fresh
separate databases for positive and two mutated inputs, verified exact
successfully extracted file multisets and zero extraction errors for each,
then ran the actual query. The pinned LuCI source SHA-256 is
`6f9d972958d9cfb8a7ba421f38f0a5b03718ffeb0e30d460b64c9faf725fc54e`; pinned
`sys.uc` SHA-256 is
`0380fba5d843a8950bab0ef70982cb40ab8f475e8d267c873e4199a736b55656`.

Independently inspecting the two sources and
[query contract](https://github.com/lucas-albers-lz4/codeql-ucode/blob/d3588ca6821fe983d240fcbb2e80692fabcc6aab/docs/m4-luci-sys-status-exec.md)
establishes expected `process_list` fixed `/bin/busybox top -bn1` at line 7,
and `conntrack_list` fallback `/usr/sbin/conntrack -L -o extended` at line
49, paired with their named wrappers. The actual [results](../evidence/009/status.csv)
contain exactly those two messages; [successful-file identities](../evidence/009/extracted.json)
and [errors](../evidence/009/errors.json) cover both positive inputs. The
reviewed extracted JSON replaces only the local checkout prefix.

In one valid extracted control both wrapper dispatches were swapped; in another
both the top command and conntrack fallback guard were changed. Each fresh
control database had both expected files extracted with zero errors, and each
query produced zero rows. These are combined mutations: they demonstrate the
aggregate response to each pair of changes, not independent coverage of every
guard. The smoke's temporary control files and databases were deleted on exit;
the local log remains under ignored `work/`. Existing modeling and deferred
query work remain owned by [ucode #50](https://github.com/lucas-albers-lz4/codeql-ucode/issues/50)
and [#54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54).
