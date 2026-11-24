# Claim 086: disjoint LuCI markup and shebang route slice

**Status:** Demonstrated

**Scope:** A source-first, fresh CodeQL 2.27.4 routing and extraction check of 24 pinned LuCI files disjoint from the selected paths in claims 021, 077, 081 and 084: 22 `.ut` templates and two Ucode-shebang scripts. It records exact source/stage identities, route decisions, successful-file and error tuples, and the draft default-suite output.

**Out of scope:** Modeled markup semantics, installed package bytes, a security-negative result, representative corpus coverage, or a consumer handoff. The 22 template routes are explicitly `markup_not_modeled` and inconclusive even though their files appear in the successful-extraction diagnostic.

## Revisions and context

- LuCI: clean `b2e0be4b46ec0fd43394c081fa7c50657af14011`; producer: clean `977331713b4b8b5574813bee0884245bf6db2752`; consumer lock checkout: clean `48c6a65b7578234644c6b06780fc82ccf6d61a8b`, lock SHA-256 `b4cbdabb76df90a807aba7d42ae675198c7b7b09c3b84db259a3a4c941b0ea9a`.
- Source-first [oracle](../evidence/086-20261124-luci-markup-shebang-slice/source-first-oracle.json), SHA-256 `9560c11c00a094b86a8f12591c067f346cb1a4159f759430f875b726261630bd`, frozen before extraction. It records all 24 Git blobs, source/stage hashes, expected source and proposed installed identities, exact route categories and zero overlap with earlier selected paths. The 24-file selection follows the pinned [LuCI source census](085-pinned-luci-ucode-source-census.md), not a generated package listing.
- Tool: CodeQL CLI 2.27.4, with copied extractor pack and locked dependency cache into run-owned paths. The normalized receipt records the executable/pack digests, build provenance and dependency-readiness result; no pack was rebuilt for this run.

## Evidence required and observed

1. All 24 staged hashes matched the independently pinned source blobs and bytes. The extractor route receipt matched the oracle exactly: 24 inputs, two `plain` / `ucode_shebang` routes, 22 `markup` / `ut_markup_extension` routes with `status=inconclusive` and `inconclusive_reason=markup_not_modeled`, zero uncertain/excluded/duplicate decisions.
2. `SuccessfullyExtractedFiles` returned every expected staged source identity once; `ExtractionErrors` returned zero tuples. This is exact extraction accounting, not a statement that the templates' embedded Ucode behavior is modeled.
3. The resolved default suite contained `DirectRpcShellWord.ql` and the two extraction diagnostics. SARIF emitted the direct rule descriptor and zero results. No eligible positive/near-miss security pair was established in this route slice; the empty result is an observation only.
4. The initial local validation harness exited 1 because it opened `extracted.csv`/`errors.csv` while the decoders wrote `extracted-decode.csv`/`errors-decode.csv`. The already produced raw diagnostic tuples were retained. A corrected offline comparison on those same outputs exited 0 before suite analysis; extraction was not rerun. The failed validation remains visible in the command receipt and is not counted as a pass.

## Run record

- Date/environment: 2026-11-24 UTC, isolated macOS `work/luci-24-route-extraction-20261124/run-a/` with run-owned stage, database, pack/dependency-cache copies, temp, compilation cache and outputs. The inherited home directory is a provenance limit; explicit writable CodeQL caches were owned by the run.
- Commands/exits: 13 recorded phases; 12 exited 0 and the original filename-bug validation exited 1. The corrected validation exited 0. Index took 0.78 seconds/121,421,824 bytes peak RSS; finalize 1.21 seconds/277,037,056 bytes; successful-file and error queries 1.40 and 1.38 seconds; default-suite SARIF analyze 3.50 seconds/480,821,248 bytes. These are 24-file measurements, not full-corpus estimates.
- Portable artifacts: [normalized receipt](../evidence/086-20261124-luci-markup-shebang-slice/run-receipt.json), SHA-256 `95ee4717247ca0d4e9f91ab143c5616998bdd4bce4fb3c69e5357c5c83096ebf`, oracle, diagnostic CSVs, route comparison, resolved suite and [provenance notes](../evidence/086-20261124-luci-markup-shebang-slice/README.md). Local roots were normalized; raw outputs and their hashes are retained under ignored `work/`.
- Follow-up: use the exact 22-template inconclusive list for OpenWrt #68 markup reconciliation, and verify package-installed bytes before calling this an installed corpus scan. Security checks need separately supported markup models and discriminating controls.
