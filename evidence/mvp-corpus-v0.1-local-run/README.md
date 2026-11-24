# Local aggregate probe for bounded corpus v0.1

Status: one completed fresh **macOS source-staged** 76-file run on 2026-11-24,
not a Linux Gate 6/7 pass, installed-package scan or security-negative result.
The independently prepared
[source oracle](../../planning/mvp-bounded-corpus-v0.1.json) has SHA-256
`7c71634e7a02c5aa5776820f6b141b086935b8cff117d5bbfdd5cced668db601`.
The [normalized receipt](receipt.json) records the tool, producer/source pins,
preflight, phase exits/times, raw artifact digests and limitations. The
[exact identities](exact-identities.csv) list all 76 projected installed
paths, route reason/status, one successful-file identity each and zero
extraction errors. The CSV contains relative paths normalized from the raw
absolute `work/` stage paths; the receipt links it to the raw outputs by
SHA-256. The raw database, SARIF and command logs remain in ignored
`work/mvp-corpus-v0.1-run-20261124-c` and are not portable by link.

The run command was `python3 work/mvp-corpus-v0.1-prep/run.py` from the ledger
root, using the local CodeQL 2.27.4 executable and a copied, previously built
extractor pack. The preflight checked clean full source/producer SHAs, locks,
source and staged hashes, unchanged extractor/build contracts, tool and pack
digests, disk, CPU and available-memory percentage. All nine CodeQL phases
exited zero. The route receipt reports 42 plain and 34 markup-inconclusive
files; successful-file diagnostics report all 76 exactly once and extraction
errors are empty. The resolved default suite contains the direct RPC rule and
two extraction diagnostics. SARIF has the direct-rule descriptor and **zero
results** on this selected current-source corpus. This says nothing about
security of the selected files or precision outside the rule's eligible shape.

The nine phase wall times total 14.209 seconds; database init/index/finalize
total 2.880 seconds and default-suite analysis took 7.756 seconds. These are
local macOS measurements for these 76 source-staged files, not Linux or
full-OpenWrt estimates. Peak RSS is unavailable: the first attempt's macOS
`time -l` wrapper failed with a `kern.clockrate` permission error after CodeQL
created a skeleton database. That run was stopped and excluded. A second run
completed, but it lacked the required pre-run available-memory check, so the
fresh third run is the canonical observation. All attempts used different
database, cache and output paths under ignored `work/`.
