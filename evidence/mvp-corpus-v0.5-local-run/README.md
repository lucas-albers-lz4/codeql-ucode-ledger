# Local aggregate probe for bounded corpus v0.5

Status: one failed route-oracle attempt followed by one completed fresh
**macOS source-staged** 123-file run on 2026-11-24. The first attempt stopped
before finalize when two `.uc` sources with Ucode shebangs routed by
`ucode_shebang`, rather than the predeclared `ucode_extension` reason. The
[failure receipt](first-attempt.json) preserves the original oracle hashes
and raw routing hash. Pinned source first lines were inspected, and the
[corrected oracle](../mvp-corpus-v0.5-source-first-oracle.json) was frozen
before the second run (SHA-256
`d19401a66c581fad5860306f76f4a1815f6b4c057c1f6afc3268a8e3a1972e0e`).

The retry command was `python3 -B work/mvp-corpus-v0.5-prep/run.py` from
the ledger root. The [normalized receipt](receipt.json) records exact source,
producer, CodeQL, locks and pack identities; normalized exact command argv,
phase exits/times; raw artifact hashes; and limits. `$RUN` denotes the
second run root and `$CODEQL` the recorded 2.27.4 executable. The
[exact identities](exact-identities.csv) list all 123
source and staged paths, source SHA-256 values, route decisions and
successful-file multiplicity. Absolute `work/` paths are normalized there.
The raw database, logs, and outputs remain under ignored
`work/mvp-corpus-v0.5-run-20261124-b`; the first failed run remains under
`work/mvp-corpus-v0.5-run-20261124-a`.

Preflight checked clean pinned source/producer revisions, source and stage
hashes, locks, pack provenance, CodeQL 2.27.4, and available resources.
Database, cache, `HOME`, `TMPDIR` and outputs were run-owned. Post-run checks
rehashed source and staged bytes, compared all 123 exact route and successful
identity tuples with the oracle, and checked diagnostics and SARIF. Three
bootstrap and nine CodeQL commands exited zero. The route report has 88
plain and 35 markup-inconclusive selections, no duplicates or exclusions.
All 123 files extracted exactly once, with zero extraction errors. The
default suite resolved to the direct RPC rule and two diagnostics; SARIF has
the direct-rule descriptor and zero results for these current-source files.

The nine CodeQL phase times sum to 46.868 seconds, including 39.423 seconds
for suite analysis; init/index/finalize sum to 3.574 seconds. Peak RSS was
unavailable in this sandbox. This is a bounded local macOS measurement, not
a Linux full-corpus estimate. The package/target conditions in the manifest
were not built into one image, and actual installed bytes were not compared.
Successful extraction of markup is not modeled markup support; zero alerts
do not establish security or rule precision. Gates 6 and 7 remain open.
