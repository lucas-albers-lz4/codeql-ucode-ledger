# v0.6 local aggregate run: extraction failure

The source-first [v0.6 manifest](../../planning/mvp-bounded-corpus-v0.6.json)
selected 128 files at captured OpenWrt PR #26933 head
`bce40f6a15c273778061e8fceced7b9e0f58d99b`, with pinned LuCI and
packages sources unchanged. The [oracle](../mvp-corpus-v0.6-source-first-oracle.json)
and [controls](../mvp-corpus-v0.6-controls.json) were corrected, verified and
hashed before the first analyzer output. The initial drafts and corrections
are described in the [manifest note](../../planning/mvp-bounded-corpus-v0.6.md).

The command `python3 -B work/mvp-corpus-v0.6-prep/run.py` used a fresh
run-owned producer checkout, pack copy, cache, staging tree and database under
ignored `work/mvp-corpus-v0.6-run-20261124-b`. The
[normalized receipt](receipt.json) records source/tool/pack identities,
exact command argv with `$RUN` and `$CODEQL` substitutions, exits, times, raw
artifact hashes and extractor diagnostic locations. The
[128-row identity table](identities.csv) preserves source and staged paths,
source hashes, expected routes and actual success/error multiplicity. All 128
route tuples matched the oracle: 93 plain and 35 markup-inconclusive. Database
init, index, finalize and both diagnostic query/decode pairs exited zero.

The run **failed** its exact extraction check: 126 selected files had one
successful-file row each; `lib/wifi/mac80211.uc` and
`usr/share/ucode/wifi/utils.uc` had no success row and two parse diagnostics
each. The first file's diagnostics are at line 17, columns 15–21 and 33;
the second's are at lines 72 and 76. The seven completed CodeQL phases took
6.910 seconds in total, without a peak RSS measurement. Source and staged
hashes and clean checkout pins were rechecked after failure. The runner
stopped before suite resolution or SARIF; there is no v0.6 alert result.

The first diagnostic aligns with `import("provision")` in the captured source;
the second follows an exported function declaration. The pinned grammar
contains static import declarations and documents a required semicolon after
exported functions. These are source/grammar observations, not a demonstrated
runtime validity judgment or a validated parser patch. This local macOS
source-staged run does not verify installed bytes or Linux cost.
