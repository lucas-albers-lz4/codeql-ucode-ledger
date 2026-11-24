# Claim 080: final experimental direct-RPC source distinction

**Status:** Demonstrated for the source-first bounded inputs, final producer/query pin and run-i execution.

**Scope:** The explicit `DirectRpcShellWord.ql` at clean producer `29d8a6e9b352e0904065ec5572db4d845ff15919` extracted the source-first parent, fixed revision, swconfig file and 21-control slice once each with zero errors. It emitted one parent row, no fixed or swconfig rows, and five eligible control rows. Four independent SARIF outputs had result counts 1, 0, 0 and 5 at the corresponding exact source regions.

**Out of scope:** Default-suite readiness, release status, security exploitability, runtime reachability, authorization, shell quote-state proof, installed bytes or consumer handoff. A reported direct interpolation site is a bounded source observation.

## Revisions and context

- Producer: `29d8a6e9b352e0904065ec5572db4d845ff15919`, clean; base `18afe771568d373088edee7a790825ee46dec9e0`.
- Source-first oracle SHA256: `fcab0ad97ee83389e62ecaafb6491675f6605e4a7987c3d666f8ee8669e712ea`.
- Query: `DirectRpcShellWord.ql`, SHA256 `046c57aa2003c5b0a5c1a8eec9afc7ca00fdb727928839bff51a4236f5e93f48`; witness query SHA256 `9400b7e68f1ba229dfb662418476640451f5fb14ab52c60348afe0982a577460`.
- CodeQL 2.27.4; extractor SHA256 `c7bde2d31303127f6bf8ebbbb364a5a47840867b67962a013032a3b6bbe7f8d2`; extractor pack build revision `8375887ed14825dd59addbfd0df43616d9e684fb`.
- Upstream pins: OpenVPN parent `b45584b4e6068b9b096872dd02494a048d869c36`, OpenVPN fix `e4ff45ecbc6ad212951815c8c99b2749fbd7de6b`, swconfig LuCI `b2e0be4b46ec0fd43394c081fa7c50657af14011`.

## Evidence required

1. The source-first manifest defines 24 exact input hashes: parent, fixed, swconfig and 21 controls. Run-i staged bytes matched every hash; successful-file identities matched all 24 expected staged paths exactly, once each, with zero extraction errors.
2. Independent AST witness rows are preserved with multiplicity: two each for parent, fixed and swconfig, and 23 across controls. The rule emitted exactly one parent row, zero fixed rows, zero swconfig rows, and five control rows.
3. Control results were `different_field_pos.uc`, `direct_pos.uc`, `initialized_local_pos.uc`, `multi_substitution_quote_context.uc`, and `quoted_first_raw_second.uc`. The remaining 16 controls emitted no rule row. Each was successfully extracted.
4. SARIF used rule ID `ucode/m4/direct-rpc-shell-word`. It emitted parent `luci.openvpn.uc` line 71 columns 115–132; no fixed or swconfig result; and five control results at their corresponding source operands. Exact URIs and regions are in the case results.
5. Run-i's 44 extraction/query/decode commands and four SARIF analyze commands all exited 0. The normalized receipt includes argv, phase wall times and peak RSS parsed from retained time output.
6. Probe-c separately copied the existing Stage-6 21-file database and ran the same final query. Its successful-file diagnostic returned 21 paths, errors were empty, and CSV and SARIF had zero results. This probe did not freshly extract those files.

## Run record

- Date/environment: 2026-11-24, fresh run-i databases and owned caches under ignored `work/direct-rpc-shell-run-20261124-i`; probe-c uses its separately copied database under ignored `work/direct-rpc-shell-current-slice-20261124-c`.
- Exact commands/statuses: 48 run-i commands and seven probe-c commands, all exit 0. See [normalized commands](../evidence/080-20261124-direct-rpc-generalized-rule/commands.json).
- Outputs: [source identities](../evidence/080-20261124-direct-rpc-generalized-rule/source-identities.json), [case results](../evidence/080-20261124-direct-rpc-generalized-rule/case-results.json), and [probe-c receipt](../evidence/080-20261124-direct-rpc-generalized-rule/probe-c.json). Raw artifact hashes are in [raw-hashes.json](../evidence/080-20261124-direct-rpc-generalized-rule/raw-hashes.json).
- Non-passes: earlier run-h used an invalid-catch source-first variant and produced two control parse errors (`catch_formal_shadow.uc`, `catch_local_shadow.uc`); its outputs are excluded. Current-slice-a's rule query was interrupted at 183.36 seconds with exit 130 and is not a result. See [nonpasses.json](../evidence/080-20261124-direct-rpc-generalized-rule/nonpasses.json).
- Status and limits: demonstrated only for this explicit query and these staged source/control inputs. Probe-c is a copied-database query observation, not a fresh source extraction.
- Outstanding unknowns: default-suite and release integration, true shell quote interpretation, installed-image correspondence, external consumer behavior and runtime semantics remain untested.
