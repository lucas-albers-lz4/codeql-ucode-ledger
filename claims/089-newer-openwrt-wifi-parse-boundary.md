# Claim 089: newer OpenWrt wifi sources fail exact extraction

**Status:** Demonstrated

**Scope:** The released-candidate producer at
`9166af76cf6944e1b3ea5856a9176366a1f7a6ee` routes all 128 selected
source-staged v0.6 inputs at captured OpenWrt PR #26933 head, but fails to
extract two changed wifi sources. This is an extraction observation at exact
pins, not an assertion about runtime Ucode validity.

**Out of scope:** Installed package bytes, Linux behavior, a default-suite
SARIF result, vulnerability or safety, complete OpenWrt coverage, and a
validated grammar fix.

## Revisions and context

- Producer: clean `9166af76cf6944e1b3ea5856a9176366a1f7a6ee`; reused
  extractor pack with provenance checked against unchanged extractor/build
  contract, binary SHA-256
  `c7bde2d31303127f6bf8ebbbb364a5a47840867b67962a013032a3b6bbe7f8d2`.
  Grammar pin: `4a243af329fae2f4ff01e0fc80133cbab8314600`.
- OpenWrt: captured head
  `bce40f6a15c273778061e8fceced7b9e0f58d99b`; prior v0.5 pin
  `4e9642517b48bae612ff10fb72fb9199e559500e`. LuCI and packages pins
  remain `b2e0be4b46ec0fd43394c081fa7c50657af14011` and
  `07e0d16305d2b5903b37ad7913e33e18795f81a4`.
- CodeQL 2.27.4 executable SHA-256
  `bb3a754e126ed061b5f3356531cd5501872ab3864bd665b2d1afdbf8a67a146d`.
  Source policy and controls: [v0.6 manifest](../planning/mvp-bounded-corpus-v0.6.md).

## Evidence required

1. The v0.6 [source-first oracle](../evidence/mvp-corpus-v0.6-source-first-oracle.json)
   was frozen before run output, with 128 selected and 13 excluded source
   identities. Independent pre-run review corrected stale control hashes,
   stage-path slashes and an excluded-source digest. The final manifest SHA-256
   was `9c004ed477665f6567a071eac45051445c61019af927bfa4e51bae4c50ebd490`;
   oracle SHA-256 was
   `c30bbd8108c44519b8f63f0861d14dbbb5ef8f533f09a20b79942181ec360c64`.
   All selected/excluded source bytes and Git blobs were rechecked at clean
   pinned revisions; staged destinations were unique and relative.
2. All 128 exact routes matched the oracle: 93 plain and 35
   markup-inconclusive. The [run receipt](../evidence/mvp-corpus-v0.6-local-run/receipt.json)
   and [identity table](../evidence/mvp-corpus-v0.6-local-run/identities.csv)
   show 126 successful-file identities once each and four parse diagnostic
   rows on two files. Neither failed file has a success row.
3. `lib/wifi/mac80211.uc` at the new pin has Git blob
   `da5d0975ceb3931bf4b8dd9906f03364add0e002` and source SHA-256
   `17143a060e91dd83476e864b484c402a8c88bf70b15b8af59a87d6d72a3d3bb8`.
   It routes by `ucode_shebang`; diagnostics point to line 17 columns 15–21
   and 33, where the source contains `import("provision")`.
   `usr/share/ucode/wifi/utils.uc` has Git blob
   `5158b84600f2692e0e918deeb04b38805e6558d6` and SHA-256
   `0cbbcda771ec40c8d9d394f2d3fa7cf5e36c039d08f26d8fd6aef71fba44380d`.
   It routes by `.uc` extension; diagnostics are at lines 72 and 76, after
   exported function declarations. The pinned grammar's compatibility table
   explicitly lists dynamic `import()` expressions and `export function`
   without a trailing semicolon as newer Ucode syntax it does not yet support.
   This explains the observed parse boundary; no parser patch was validated.
4. Eligible controls are `lib/netifd/wireless.uc`, whose bytes also changed
   across the source pins but which extracted once at both, and the new
   `lib/netifd/proto/wireguard.uc`, which routes by Ucode shebang and extracted
   once. The competing wifi shell path remained an explicit excluded near
   miss. At the older v0.5 pin the two now-failing paths each extracted once
   with zero errors; their Git blobs and source hashes changed at v0.6.

## Run record

- Date/environment: 2026-11-24, local macOS. Command:
  `python3 -B work/mvp-corpus-v0.6-prep/run.py`. It used a fresh run-owned
  database, stage, caches, `HOME`, `TMPDIR` and producer checkout under
  ignored `work/mvp-corpus-v0.6-run-20261124-b`.
- Seven completed CodeQL phases exited zero and took 6.910 seconds in total.
  Exact normalized argv, individual times, output hashes and diagnostic
  locations are in the [portable receipt](../evidence/mvp-corpus-v0.6-local-run/receipt.json).
  The runner itself exited 1 at the exact extraction check. Source and staged
  hashes and clean checkout pins were rechecked afterward. Peak RSS was
  unavailable.
- No suite resolution or SARIF analysis ran after this failure. The two
  parse gaps require producer grammar/extractor investigation before v0.6 can
  be used as a current-corpus pass. Earlier v0.5 success does not transfer
  across the OpenWrt source revision change.
