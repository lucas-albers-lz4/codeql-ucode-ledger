# Claim 082: local direct-RPC SARIF handoff

**Status:** Demonstrated for three pinned staged source inputs, the final local direct-RPC query, and the identified local consumer parser.

**Scope:** Fresh local macOS run-b produced default code-scanning-suite SARIF for separate parent, fixed, and swconfig databases; the actual SARIF bytes were passed to the local consumer at `a6f4956507e2cd2078ba7c3ac7270c2e0c343cd6`. Source files each extracted exactly once with zero errors. The parent SARIF result was accepted at the exact predeclared warning identity; fixed and swconfig had no results and were accepted as empty.

**Out of scope:** Linux or versioned-release readiness, installed package/rootfs bytes, runtime exploitability, reachability, authorization, or shell quote-state proof. This local acceptance does not authenticate arbitrary producer receipts.

## Revisions and context

- Producer: integrated commit `299731d8e22112cf88680b89ee08915ff531d273`, clean at run preflight.
- Consumer: checkout `a6f4956507e2cd2078ba7c3ac7270c2e0c343cd6`, clean at run preflight; validator SHA256 is recorded in the evidence.
- Source-first oracle: SHA256 `fcab0ad97ee83389e62ecaafb6491675f6605e4a7987c3d666f8ee8669e712ea`.
- Query: `DirectRpcShellWord.ql`, SHA256 `a071facd947a65d3eb48906070cf17ad53d2bd62b54116991437f77fef5e52d8`.
- CodeQL: 2.27.4. Extractor binary SHA256 `c7bde2d31303127f6bf8ebbbb364a5a47840867b67962a013032a3b6bbe7f8d2`; complete 14-file pack inventory and digest are in the evidence. Pack build revision: `8375887ed14825dd59addbfd0df43616d9e684fb`.
- Code-scanning suite SHA256: `6d343f93e37c309b8461da9fafcf67d089737980d7ac42a5409e75df3bd442e5`. The suite resolved the direct-RPC query and the successful-file and extraction-error diagnostics.

## Evidence required

1. Before indexing, each source was checked against the source-first oracle and copied to an installed-style stage path. Parent, fixed, and swconfig staged SHA256 values matched the oracle. Their manifests pin those source bytes and predeclare the expected SARIF multiset.
2. Each of the three fresh databases returned exactly its one expected successful-file identity and zero extraction-error rows. Separate databases, caches, outputs, and TMPDIRs were used per case.
3. The resolved suite queries had `@id` values `ucode/m4/direct-rpc-shell-word`, `ucode/diagnostics/extraction-errors`, and `ucode/diagnostics/successfully-extracted-files`. SARIF carried the direct-RPC descriptor. Parent emitted one warning for `req.args?.cl_meta` at `usr/share/rpcd/ucode/luci.openvpn.uc`, line 71 columns 115–132; fixed and swconfig emitted none. The local consumer accepted exactly that parent result and returned empty accepted-result lists for fixed and swconfig.
4. All 30 run-b commands exited 0. Their full argv, wall time, peak RSS, and stdout/stderr hashes are preserved in the normalized command record. The raw SARIF, pre-run manifests, producer receipts, diagnostics, and consumer outputs are preserved under the evidence `raw/` directory.
5. The extractor pack's fourteen files matched the earlier build provenance manifest. The producer identity field named `pack_sha256` is specifically the extractor executable digest; the evidence separately records the full pack directory digest. The build provenance records a dirty grammar `Cargo.toml` patch and its digest.
6. `run_b.py` orchestrated run-b. `run.py` is the superseded run-a prototype. The run-b workspace started from a prior `29d8a6e9b352e0904065ec5572db4d845ff15919` producer snapshot and overlaid both final query files from integrated producer `299731d`. The QL source diff between those commits is the direct query modification and Tailscale query addition; the executed query files, suite, diagnostics, and QL locks were byte-checked against the integrated checkout.
7. The consumer checks supplied source bytes, SARIF SHA256 against the receipt, producer identity equality, extraction inventory, zero errors, suite rule IDs, descriptor IDs, and the exact expected result multiset. Its own documentation states that it cannot authenticate an arbitrary receipt. The local orchestration records the actual producer outputs and consumer invocation; this is a local handoff observation, not a signed execution attestation.

## Run record

- Date/environment: 2026-11-24, fresh databases under ignored `work/direct-rpc-local-handoff/run-b/` on macOS.
- Commands and statuses: 30 producer, suite-resolution, and consumer commands, all exit 0. See [normalized commands](../evidence/082-20261124-local-direct-rpc-sarif-handoff/commands-normalized.json).
- Source, suite, SARIF and accepted identities: [handoff results](../evidence/082-20261124-local-direct-rpc-sarif-handoff/handoff-results.json); [raw artifact hashes](../evidence/082-20261124-local-direct-rpc-sarif-handoff/raw-hashes.json); exact raw manifests, receipts, SARIF, diagnostics and accepted outputs are in [raw evidence](../evidence/082-20261124-local-direct-rpc-sarif-handoff/raw/).
- Status and limits: demonstrated for this local draft producer, three staged files, and local parser checkout only. The evidence does not establish a Linux/release environment, deployed bytes, or semantic security.
- Outstanding unknowns: authenticate receipts at the CI boundary; verify the final integrated producer and pack through the Linux/versioned release pipeline; establish installed-byte correspondence; separately validate any runtime or quote-state security conclusion.
