# Claim 077: current LuCI and OpenWrt staged extraction slice

**Status:** Demonstrated

**Scope:** In one run-owned staged source tree, CodeQL 2.27.4 successfully extracted all 21 selected source identities from the frozen LuCI luci-base and OpenWrt utils/cli slice, with zero extraction error rows; the routing probe selected plain extraction for 20 and classified one markup-sensitive input as inconclusive.

**Out of scope:** Installed package or rootfs byte equivalence; complete package/repository selection; semantic query behavior, SARIF production or consumption; vulnerability or reachability conclusions. `uhttpd.uc` is not a plain-extraction success for route coverage purposes.

## Revisions and context

- LuCI commit: `b2e0be4b46ec0fd43394c081fa7c50657af14011` (clean disposable checkout).
- OpenWrt commit: `4e9642517b48bae612ff10fb72fb9199e559500e` (clean disposable checkout).
- Packages feed commit: `07e0d16305d2b5903b37ad7913e33e18795f81a4` (clean disposable checkout).
- Consumer corpus lock: checkout `66a9c78cd605dbe63645235074b9747ab57b187e`, `corpus/lock.json` SHA256 `b4cbdabb76df90a807aba7d42ae675198c7b7b09c3b84db259a3a4c941b0ea9a`.
- Producer: `18afe771568d373088edee7a790825ee46dec9e0`, clean; CodeQL 2.27.4; extractor SHA256 `c7bde2d31303127f6bf8ebbbb364a5a47840867b67962a013032a3b6bbe7f8d2`.
- Source-first oracle SHA256 `3943f4cec7739867178ceb94f2ba1026d24f5379d4137bf90aff7215c51e92da`; staged receipt SHA256 `5e598e54c3c4ad37d729d5a936a9f432a1e2beefd37f6926b639cd75fac9e066`.
- Existing contracts: consumer corpus lock and route probe behavior in the pinned consumer; producer extraction diagnostics `SuccessfullyExtractedFiles` and `ExtractionErrors`.

## Evidence required

1. Exact intended extraction identities and diagnostics were checked against the independent source-first oracle. All 21 staged paths appeared once in successful-file tuples; zero extraction-error tuples were observed.
2. The receipt preserves source repo/path, package owner, Git blob, source SHA256, staged path/digest and routing expectation. The source and staged SHA256 values match for all selected files.
3. The selection includes three extensionless ucode roots: `usr/sbin/cli`, `usr/share/rpcd/ucode/luci`, and `www/cgi-bin/luci`. The routing probe recorded 20 plain decisions and one inconclusive markup decision (`usr/share/ucode/luci/uhttpd.uc`, reason `markup_tag_content`, status `inconclusive`, `markup_not_modeled`). Generated `version.uc` was excluded. This is a source selection/extraction check, not a semantic positive/negative query test.
4. Run-a completed database extraction commands but did not produce a verified successful-file result: its extraction diagnostic query exited 2 because `codeql/controlflow@1.0.12` was unavailable. A prior direct route-probe invocation printed a missing `CODEQL_EXTRACTOR_UCODE_DIAGNOSTIC_DIR` error despite exit 0; it is not treated as a pass. The fresh run-b route probe used its owned diagnostic directory and emitted 21 decisions.
5. Run-b used a fresh owned database, outputs, cache and TMPDIR. Its seven recorded commands all exited 0. Query stderr included the warning that stages were not cached because maximum heap size was 1256 MB. The run-owned QL pack copy replaced the workspace dependency with locked `0.1.0`; query/library bytes were unchanged.

## Run record

- Date and environment: 2026-11-24, disposable workspace under ignored `work/stage6-first-slice-prep-20261123-a/run-b`; detailed normalized commands, wall times and peak RSS are in [commands.json](../evidence/077-20261124-current-slice-extraction/commands.json).
- Exact commands and exit statuses: seven run-b commands (database init, index-files, finalize, successful-files query/decode, extraction-errors query/decode), each exit 0. Raw artifact hashes are recorded in [receipt.json](../evidence/077-20261124-current-slice-extraction/receipt.json).
- Actual outputs / artifact locations and relevant hashes: the portable [evidence README](../evidence/077-20261124-current-slice-extraction/README.md), [source identities](../evidence/077-20261124-current-slice-extraction/source-identities.json), [successful files](../evidence/077-20261124-current-slice-extraction/successful-files.json), [extraction errors](../evidence/077-20261124-current-slice-extraction/extraction-errors.json), and [routing decisions](../evidence/077-20261124-current-slice-extraction/routing.json). Frozen oracle SHA256: `3943f4cec7739867178ceb94f2ba1026d24f5379d4137bf90aff7215c51e92da`.
- Controls and results: independent exact source identity/multiset comparison passed; zero extraction errors. Markup-sensitive `uhttpd.uc` is explicitly inconclusive, not a negative or plain success.
- Status and its limits: demonstrated for this staged 21-file source slice and these extraction/routing observations only. It does not represent installed bytes or complete corpus coverage.
- Outstanding unknowns / follow-up: establish build/install transformations and installed bytes in a separately pinned package/rootfs; evaluate query and SARIF contracts in a distinct claim.
