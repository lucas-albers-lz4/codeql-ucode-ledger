# Claim 084: disjoint LuCI package Ucode source slice

**Status:** Demonstrated

**Scope:** One fresh, source-staged CodeQL 2.27.4 run over four pinned LuCI files under `applications/*/ucode/`, disjoint by exact source path from the prior 21-file and 17-file slices. The claim covers source/stage bytes, routing, successful extraction and error identities, and bounded observations of the resolved default suite and a separate testing query.

**Out of scope:** Built package or installed-image bytes, all LuCI Ucode, a security-negative conclusion, query precision, runtime behavior, or a producer-to-consumer handoff. This selection has no pre-established eligible security positive/near-miss pair; empty query output is only a recorded observation.

## Revisions and context

- LuCI: clean detached `b2e0be4b46ec0fd43394c081fa7c50657af14011`; consumer corpus lock SHA-256 `b4cbdabb76df90a807aba7d42ae675198c7b7b09c3b84db259a3a4c941b0ea9a` in clean consumer checkout `48c6a65b7578234644c6b06780fc82ccf6d61a8b`.
- Producer: clean disposable `mvp/direct-rpc-suite-draft` at `977331713b4b8b5574813bee0884245bf6db2752`; CodeQL CLI 2.27.4. The copied extractor pack and dependency cache identities are in the receipt; each run used its own writable copies, database and outputs.
- Frozen [source-first oracle](../evidence/084-20261124-luci-package-ucode-slice/source-first-oracle.json), SHA-256 `123cf5151e3ff1f717883d665b35c36b9a823f9a17893a16d4cb3e2d3b74b518`, records four Git blobs, source/staged SHA-256 digests, proposed installed paths and route decisions. The selected files are `luci-app-commands` `controller/commands.uc`, `luci-app-dockerman` `controller/docker.uc` and `docker_socket.uc`, and `luci-app-lxc` `controller/lxc.uc`.

## Evidence required and observed

1. The oracle was prepared before run-i. Each pinned source blob and source/stage hash matched; exact source-path comparison found no overlap with the prior first-21 or rpcd-17 manifests. The four staged files retained their `applications/<package>/ucode/...` layout, allowing the extractor to derive proposed `usr/share/ucode/luci/...` installed paths.
2. The route receipt contained exactly four `plain` / `ucode_extension` / `plain_route_selected` decisions with the expected source and proposed installed paths. The successful-file diagnostic returned each exact staged source identity once, with zero extraction-error tuples. Source-relative extracted identities and proposed installed paths are separate fields; no package build verified their byte equivalence.
3. The resolved default suite contained `DirectRpcShellWord.ql`, `ExtractionErrors.ql`, and `SuccessfullyExtractedFiles.ql`; SARIF emitted the direct rule descriptor and zero results. An explicit `ShellInjection.ql` testing query also returned zero rows. Source-first inspection found no valid positive/near-miss pair for these rule shapes in this slice, so neither empty output is a negative security proof.
4. The first four-file attempt, run-h, stopped before suite resolution because the validator opened the wrong CSV filenames. Its failure is retained in the run-i receipt. The corrected validator passed against run-h's decoded four identities and zero errors before fresh run-i; run-h is not counted as a successful analysis.

## Run record

- Date/environment: 2026-11-24 UTC, isolated macOS run `work/stage6-next-install-shaped/run-i/`, with run-owned stage, database, copied pack/dependency cache, compilation cache, temp and outputs. The selected LuCI, producer and consumer checkouts were clean at the recorded pins. The run inherited the process home directory; this is a provenance limit, while explicit writable CodeQL caches were run-owned.
- Commands/exits: 11 phase commands, all exit 0: database init/index/finalize, diagnostic queries and decodes, suite resolution/analyze, explicit testing query and decode. Index took 0.62 seconds/120,733,696 bytes peak RSS; finalize 1.14 seconds/267,042,816 bytes; suite analyze 3.52 seconds/472,596,480 bytes; testing query 2.37 seconds/681,443,328 bytes. These are four-file measurements, not corpus-scale estimates.
- Portable artifacts: [normalized run receipt](../evidence/084-20261124-luci-package-ucode-slice/run-receipt.json), SHA-256 `e202389aa0c4fbd6e5fdccf6041d4c33809cbb10a7709096e60179db676a518d`, the oracle, exact diagnostic/testing CSVs, resolved suite and [provenance notes](../evidence/084-20261124-luci-package-ucode-slice/README.md). The receipt retains raw output hashes and phase metrics with local path roots normalized. Raw database, SARIF and logs remain under ignored `work/`.
- Follow-up: establish installed-byte mapping and a broader representative source inventory, then choose a query family with a source-backed positive and discriminating near miss before making alert-quality or incoming-change claims.
