# Local aggregate probe for bounded corpus v0.4

Status: one completed fresh **macOS source-staged** 111-file run on
2026-11-24. The predeclared [source oracle](../../planning/mvp-bounded-corpus-v0.4.json)
has SHA-256
`1e25cf9c2adc40c854502fed8d1ccc0977a3c4825d6ee4a1c0a543ffe0a76699`.
The [normalized receipt](receipt.json) records source, producer, tool and
pack identities, phase exits/times, raw artifact hashes and limits. The
[exact identities](exact-identities.csv) contain all 111 source and relative
staged paths, route decisions and successful-file multiplicity. Absolute
local `work/` paths were normalized in that CSV; the receipt hashes the raw
routing, diagnostics and SARIF. The database, raw outputs and logs remain
only under ignored `work/mvp-corpus-v0.4-run-20261124-a`; the runner and
post-run verifier are under ignored `work/mvp-corpus-v0.4-prep`.

The run command was `python3 -B work/mvp-corpus-v0.4-prep/run.py` from the
ledger root. Preflight checked clean full producer/source SHAs, source and
stage hashes, locks, unchanged extractor/build contract since copied pack
provenance, CodeQL 2.27.4 and extractor digests, disk, CPU and available
memory. Database, cache, `HOME`, `TMPDIR` and outputs were owned by this
run. Post-run verification rechecked all source and Git blob hashes, staged
hashes, clean checkouts, exact route and successful-file multisets, nine
zero-exit commands, diagnostics and SARIF results.

The route receipt reports 76 plain and 35 markup-inconclusive paths, zero
excluded or duplicate inputs. All 111 were successfully extracted once and
extraction errors were empty. The resolved default suite contains the direct
RPC rule and two extraction diagnostics. SARIF has the direct-rule descriptor
and **zero results** for this selected current-source corpus. Successful
extraction of markup is not modeled markup support; zero alerts do not
establish security or rule precision.

The nine phase wall times sum to 24.641 seconds; init/index/finalize sum to
3.214 seconds and default-suite analysis took 17.846 seconds. These local
macOS measurements are not Linux or full OpenWrt estimates. Peak RSS is
unavailable because local `time -l` cannot read `kern.clockrate` in this
sandbox. The wifi-scripts configuration was assumed, not built, and no
package-installed bytes were compared.
