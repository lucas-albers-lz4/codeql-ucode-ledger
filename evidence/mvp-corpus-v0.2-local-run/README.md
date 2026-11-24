# Local aggregate probe for bounded corpus v0.2

Status: one completed fresh **macOS source-staged** 93-file run on
2026-11-24, not a Linux Gate 6/7 pass, installed-package scan or
security-negative result. The predeclared
[source oracle](../../planning/mvp-bounded-corpus-v0.2.json) has SHA-256
`7c3e055ece88c13684efb100c2c248b35a448027d836697063c5d79a32a200fe`.
The [normalized receipt](receipt.json) records the producer, tool and source
pins, preflight, phase exits/times, raw artifact digests and boundaries. The
[exact identities](exact-identities.csv) list all 93 relative staged paths,
route reasons/statuses and one successful-file identity each. Absolute local
`work/` paths were normalized to relative staged paths in the CSV; the receipt
hashes the raw routing and diagnostic outputs. The raw database, SARIF, logs
and runner remain under ignored `work/mvp-corpus-v0.2-run-20261124-a` and
`work/mvp-corpus-v0.2-prep`; those paths are not portable links.

The run command was `python3 -B work/mvp-corpus-v0.2-prep/run.py` from the
ledger root. Preflight checked clean full producer/source SHAs, source and
staged hashes, locks, unchanged extractor/build contract since the copied
pack's provenance, CodeQL 2.27.4 executable and extractor digests, disk,
CPU and available memory. The copied pack and dependencies had owned run
paths; database, cache, `HOME`, `TMPDIR` and outputs were unique to this run.
The post-run review rechecked all source Git blobs/hashes and staged hashes,
clean source checkouts, every route tuple and successful identity with
multiplicity, nine zero-exit commands, zero diagnostics and the SARIF result
array.

The route receipt reports 59 plain and 34 markup-inconclusive files, with
zero excluded or duplicate inputs. All 93 were extracted once; extraction
errors were empty. The resolved default suite contains the direct RPC rule
and two extraction diagnostics. SARIF has the direct-rule descriptor and
**zero results** for this selected current-source corpus. The 17 wifi-scripts
paths assume `CONFIG_WIFI_SCRIPTS_UCODE=y`, but no package was built. The
34 markup routes are not evidence of modeled markup support, and zero alerts
do not establish security or rule precision.

The nine phase wall times sum to 23.106 seconds; init/index/finalize sum to
3.091 seconds and default-suite analysis took 16.483 seconds. These are
local macOS measurements for 93 staged source files, not Linux or full
OpenWrt estimates. Peak RSS is unavailable because the local `time -l`
wrapper cannot read `kern.clockrate` in this sandbox.
