# Claim 078: experimental OpenVPN historical source distinction

**Status:** Demonstrated for the six pinned staged files, producer/query pin and run-f execution.

**Scope:** The explicit experimental query `OpenvpnRawMetadataCommand.ql` at producer `c4829ff1d30225ca758b0f7979f47c3265cf882d` emitted one row for the pinned historical OpenVPN parent source and no rows for the fixed source or four eligible near-miss controls. Each staged file extracted once with zero errors. The parent SARIF probe emitted one result at the source location.

**Out of scope:** Runtime exploitability, reachability, authorization, a general shell-injection verdict, complete project coverage, default-suite inclusion, release status, or a conclusion that the query recognizes the historical vulnerability or proves the fix safe.

## Revisions and context

- Producer commit: `c4829ff1d30225ca758b0f7979f47c3265cf882d`, branch `security/openvpn-metadata-shell`, based on `18afe771568d373088edee7a790825ee46dec9e0`.
- Historical source pair: LuCI parent `b45584b4e6068b9b096872dd02494a048d869c36`; fixed revision `e4ff45ecbc6ad212951815c8c99b2749fbd7de6b`. Their exact staged SHA256s are in the source-first evidence.
- Tool: CodeQL 2.27.4; extractor SHA256 `c7bde2d31303127f6bf8ebbbb364a5a47840867b67962a013032a3b6bbe7f8d2`; Cargo lock SHA256 `20678c3cbb29632a9369bdb3c735af9ee63c9443879db38847fbda9813aa0a77`; QL lock SHA256 `bce2891940f09fcac3337b250707047ba9fd06d307abdbc7cb42c2ed193751a3`.
- Experimental query SHA256: `559c5174ace56a3b5081906849e3584c4019de14292fbd5ebf34dd97fcb155d5`.

## Evidence required

1. The source-first oracle declares six input byte hashes and expected source/sink spans. Run-f staged bytes matched all six hashes. Each successful-file result named exactly its one staged file; each error result was empty.
2. The exact rule result multiset was one row for `parent` and zero for `fixed`, `constant_sink`, `req_reassigned`, `cmd_shadowed`, and `nested_assignment`. The independent witness query located the predeclared source/sink spans; its rows and multiplicities are retained in the receipt.
3. Controls exercise a constant sink, request reassignment to constants, a shadowed command local, and an assignment in an uncalled nested function. They all extracted without errors and returned zero rule rows.
4. A separate SARIF probe on the parent database emitted one result, rule ID `ucode/m4/openvpn-raw-metadata-command`, URI `usr/share/rpcd/ucode/luci.openvpn.uc`, region line 71, columns 115–132. It is a query-result serialization observation for that probe, not a release-consumer handoff.
5. All 54 recorded extraction, query, and decode commands in run-f exited 0. Per-command durations, peak RSS, normalized argv and raw hashes are in [the evidence receipt](../evidence/078-20261124-openvpn-final-rule/receipt.json) and [commands](../evidence/078-20261124-openvpn-final-rule/commands.json).

## Run record

- Date/environment: 2026-11-24, six separate run-owned databases, caches and output directories under ignored `work/openvpn-rule-shadow-final-20261124-f`.
- Exact commands and statuses: 54 run-f commands, all exit 0; plus the separate parent SARIF probe, exit 0. See the normalized command record.
- Results and identities: [source-first inputs](../evidence/078-20261124-openvpn-final-rule/source-first.json), [case results](../evidence/078-20261124-openvpn-final-rule/case-results.json), and [SARIF summary](../evidence/078-20261124-openvpn-final-rule/sarif-summary.json). Raw artifact SHA256s are recorded in `receipt.json`.
- Status and limits: demonstrates only the stated explicit-query distinction on these historical bytes and controls. The positive rule row is not an exploitability or security finding.
- Unknowns: the detector is experimental and not part of the default suite or release gate; no live consumer or runtime validation was performed.
