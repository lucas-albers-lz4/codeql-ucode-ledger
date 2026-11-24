# Claim 079: experimental Tailscale nested-shell historical source distinction

**Status:** Demonstrated for the two pinned historical files, thirteen staged files, producer/query pin and run-d execution.

**Scope:** The explicit experimental query `TailscaleNestedShell.ql` at producer `2dde7010e9bcf7cb445743fc48221bbfadfcaa34` returned one candidate for the pinned Tailscale parent and zero for the fixed source. Its eleven-file control stage produced one candidate on the predeclared nested positive and zero on the other ten files. The parent, fixed and controls SARIF runs had result counts 1, 0 and 1 respectively.

**Out of scope:** Runtime exploitability, reachability, authorization, general shell-injection detection, default-suite inclusion, release status or a complete repository scan. A syntactic query distinction does not establish a vulnerability or validate remediation safety.

## Revisions and context

- Producer commit: `2dde7010e9bcf7cb445743fc48221bbfadfcaa34`, clean; CodeQL 2.27.4.
- Historical source pair: parent `46cd82328dfb7fbb15961c63f9e674a41cef2500`; fix `507ab5e45c304543d4111af9a331db0f03be6bcb`.
- Source-first staged manifest SHA256: `b1a538d03d60e356ae94cf374a2bfdc9338d81068b9e0a7233ac3bcbf89ac114`; all thirteen staged file hashes matched its file entries.
- Query SHA256: `136ec48e2f38c0da03d3dd975fcccae348997dbb6e6ec4a014444c42b6e09bfc`; extractor SHA256 `c7bde2d31303127f6bf8ebbbb364a5a47840867b67962a013032a3b6bbe7f8d2`; lib/src lock SHA256 `bce2891940f09fcac3337b250707047ba9fd06d307abdbc7cb42c2ed193751a3`.
- The run-owned copied pack changed only the `ql/src/qlpack.yml` workspace dependency to explicit locked version `0.1.0`; query/library bytes were unchanged.

## Evidence required

1. The source-first manifest predeclared exact hashes and expected candidate sites for both historical files and all eleven controls. Run-d staged hashes matched all thirteen entries. Parent, fixed and controls successful-file multisets contained one, one and eleven identities; all three error multisets were empty.
2. The exact candidate result multiset had one parent row at the bounded nested-shell sink, zero fixed rows, and one controls row at `nested_pos.uc` (line 18, columns 5–50); other control candidates were absent. The supplementary field query reported two parent source fields (`loginserver`, `loginserver_authkey`) at the same sink, zero fixed fields and one `nested_pos.uc` control field.
3. The source-first controls include an unrelated direct-model positive, a nested positive, nested fixed and near-miss cases, plus constant fallback, reassignment, shadowing and nested-function exclusions. They discriminate this narrow query behavior; they do not prove all nested shell flows are modeled.
4. SARIF rule ID was `ucode/m4/tailscale-nested-shell-candidate` in each run: parent result location `usr/share/rpcd/ucode/tailscale.uc` line 164 columns 3–49; fixed zero results; controls one result at `usr/share/rpcd/ucode/nested_pos.uc` line 18 columns 5–51. These are three explicit analyze outputs, not a consumer handoff.
5. All 36 recorded run-d commands exited 0. The separate copied-database run-b query used the same query hash on a 42,527,916-byte copied database, exited 0, took 3.196 seconds with peak RSS 450,052,096 bytes, and decoded zero rows in 0.230 seconds. It is a bounded side observation, not a clean extraction rerun or broad performance estimate.

## Run record

- Date/environment: 2026-11-24, separate parent/fixed/controls databases and three copied SARIF databases under ignored `work/tailscale-rule-final-20261124-d`.
- Exact commands and exits: 36 commands, all exit 0; command argv, wall time and peak RSS are in [commands.json](../evidence/079-20261124-tailscale-final-rule/commands.json).
- Results: [source-first manifest](../evidence/079-20261124-tailscale-final-rule/source-first.json), [normalized result tuples and file identities](../evidence/079-20261124-tailscale-final-rule/results.json), [SARIF summaries](../evidence/079-20261124-tailscale-final-rule/sarif-summary.json), and [copied-database timing](../evidence/079-20261124-tailscale-final-rule/copied-db-performance.json). Raw artifact hashes are in `receipt.json`.
- Status and limits: demonstrates only the bounded explicit-query historical distinction and control behavior. Neither the query nor output was tested as a default-suite or release contract.
- Unknowns: no runtime validation, installed-image mapping, full-corpus query or live external consumer handoff was performed.
