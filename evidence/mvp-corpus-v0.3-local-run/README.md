# Local aggregate probe for bounded corpus v0.3

Status: one completed fresh **macOS source-staged** 99-file run on
2026-11-24. The predeclared [source oracle](../../planning/mvp-bounded-corpus-v0.3.json)
has SHA-256
`22c0a0434b583913715cdbbd1fbfe0930bb876252fd2823c41cd38bf3a1c870b`.
The [normalized receipt](receipt.json) records source, producer, tool and
pack identities, phase exits/times, raw artifact hashes and limits. The
[exact identities](exact-identities.csv) contain all 99 source and relative
staged paths with route and successful-file multiplicity. Raw absolute
`work/` paths were normalized to relative staged paths in this CSV; the
receipt hashes the raw outputs. The raw database, SARIF and logs remain
only under ignored `work/mvp-corpus-v0.3-run-20261124-a`, with the runner
and post-run verifier under ignored `work/mvp-corpus-v0.3-prep`.

The run command was `python3 -B work/mvp-corpus-v0.3-prep/run.py` from the
ledger root. Preflight checked clean full producer/source SHAs, source and
stage hashes, locks, unchanged extractor/build contract since the copied
pack's provenance, CodeQL 2.27.4 and extractor digests, disk, CPU and
available memory. Database, cache, `HOME`, `TMPDIR` and outputs were owned by
this run. Post-run source and Git blob hashes, clean checkouts, every route
tuple and successful identity with multiplicity, nine zero-exit commands,
zero diagnostics and SARIF result array were rechecked by
`python3 -B work/mvp-corpus-v0.3-prep/post.py`.

The route receipt reports 65 plain and 34 markup-inconclusive paths, with
zero excluded or duplicate inputs. All 99 extracted once and extraction
errors were empty. The resolved default suite contains the direct RPC rule
and two extraction diagnostics. SARIF has the direct-rule descriptor and
**zero results** on this selected current-source corpus. The 34 markup
routes are not evidence of modeled markup support. Zero alerts do not
establish security or rule precision.

The nine phase wall times sum to 24.637 seconds; init/index/finalize sum to
3.058 seconds and default-suite analysis took 17.997 seconds. These are
local macOS measurements for 99 staged source files, not Linux or full
OpenWrt estimates. Peak RSS was unavailable because local `time -l` cannot
read `kern.clockrate` in this sandbox. The wifi-scripts configuration was
assumed, not built; no package-installed bytes were checked.
