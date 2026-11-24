# v0.6 local aggregate grammar-prototype run

The source-first [manifest](../../planning/mvp-bounded-corpus-v0.6.json),
[oracle](../mvp-corpus-v0.6-source-first-oracle.json) and
[controls](../mvp-corpus-v0.6-controls.json) preceded the scan. The OpenWrt
source is the captured PR #26933 head
`bce40f6a15c273778061e8fceced7b9e0f58d99b`, alongside pinned LuCI
`b2e0be4b46ec0fd43394c081fa7c50657af14011` and packages
`07e0d16305d2b5903b37ad7913e33e18795f81a4`.

The command `python3 -B work/mvp-corpus-v0.6-prototype-prep/run.py --execute`
used a fresh run-owned source stage, producer checkout, modified grammar
pack, database, cache, `HOME` and `TMPDIR` under ignored
`work/mvp-corpus-v0.6-prototype-run-20261124-b`. The
[normalized receipt](receipt.json) records preflight identities, exact
commands, exits, times and raw hashes. The
[identity table](exact-identities.csv) gives all 128 source and staged paths,
source commits/blobs/hashes, expected and actual routes, and successful-file
multiplicity. Absolute run paths are normalized as `$RUN`; `$CODEQL` is the
recorded 2.27.4 executable. Raw logs, database and SARIF remain under `work/`.

All 128 exact routes matched the oracle: 93 plain and 35
markup-inconclusive. Each selected file had one successful extraction row;
there were zero extraction-error rows. The two files that failed under the
merged producer in [the first v0.6 run](../mvp-corpus-v0.6-local-run/README.md)
now succeeded once each. The suite resolved to `DirectRpcShellWord.ql` and
the two extraction diagnostics. Its SARIF had the direct-rule descriptor and
zero results on these current-source files. Nine CodeQL phases exited zero
and took 18.137 seconds total, including 11.041 seconds of suite analysis;
init/index/finalize took 3.494 seconds. Peak RSS was unavailable.

The first prototype attempt stopped at preflight on whitespace normalization,
and the second on a mistyped preflight constant; neither created a database.
The first database attempt under `work/mvp-corpus-v0.6-prototype-run-20261124-a`
indexed and finalized, then failed its diagnostic query because dependencies
were copied to the wrong CodeQL cache location. It was retained and not
reused. The completed run used a new database and corrected run-owned cache.

This is a local macOS **modified-grammar** source-staged run. The merged
producer still has the two parse failures. No installed package bytes, Linux
run, full OpenWrt corpus, live incoming PR event, rule precision or security
property was established. Zero alerts here do not imply security.
