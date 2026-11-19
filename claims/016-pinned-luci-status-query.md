# Claim 016: pinned upstream LuCI status source-shape query

**Status: Demonstrated for the named pinned slice and dispatch control.**

## Claim and boundaries

On the fresh installed-source slice in [claim 015](015-pinned-luci-source-extraction.md),
`LuciSysStatusExec.ql` observes the two documented `getProcessList` /
`process_list` and `getConntrackList` / `conntrack_list` source-shape pairs.
A valid plugin with the two wrapper helper calls swapped is a near miss. This
is syntactic correlation, not actual cross-file call resolution, registration,
runtime execution, taint, authorization or a `path_found` claim.

## Run: 2026-11-18 UTC

Producer `094a163db1138c83820197180501bd7c78bd9051`; selected upstream LuCI
and environment are documented in claim 015. Before running, the pinned
source and query identified the expected `process_list` popen at line 7 and
`conntrack_list` fallback popen at line 49. Query SHA-256
`416fc47ea41f60d2852a9250aba1e03a02df4c676d67d582fcd717752201c22b`.

The same [runner](../evidence/015-016/run.py) ran and decoded the actual query
against the fresh three-file positive database. Exit 0; the
[output](../evidence/015-016/positive-status.json) has exactly two rows, with
`sys.uc` call spans `7:14–7:43` and `49:10–49:57`. The runner then created a
separate database from the same three inputs except for a synthetic plugin
that swaps the two named wrapper calls; modified plugin SHA-256
`49102c5c7e7a6cf375f3efec2dd1bb8f61cda42bb6f4938086f09aba9c04f062`.
All three exact [control inputs extracted](../evidence/015-016/dispatch-swapped-extracted.json)
with [zero errors](../evidence/015-016/dispatch-swapped-errors.json); its actual
[query output](../evidence/015-016/dispatch-swapped-status.json) was empty.
The positive and control each retain their own
[routing](../evidence/015-016/dispatch-swapped-routing.json) and diagnostics.
This control swaps both calls, so it tests that combined change, not each
wrapper independently. Query wall time was 4.23 s positive and 1.87 s control
as reported by GNU time; full stage measurements and actual commands are in
the [timing record](../evidence/015-016/commands-and-timings.json). Prefixes in
reviewed receipts are normalized; raw outputs remain local under `work/`.
See [ucode #50](https://github.com/lucas-albers-lz4/codeql-ucode/issues/50)
and [#54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54) for
broader modeled-flow and query work.
