# Claim 087: current LuCI quoted switch AST identities

**Status:** Demonstrated

**Scope:** One fresh, isolated local CodeQL 2.27.4 database over the pinned
current LuCI `luci` rpcd source and one synthetic control file. It checks the
distinct AST identities of two quoted `swconfig` template substitutions at
source lines 343 and 400, exact extraction and routing, and the promoted
direct RPC rule's result on a structurally eligible raw sibling positive.

**Out of scope:** Installed package bytes; shellquote correctness, runtime
reachability or exploitability; other helper/assembled shell forms; any
full-corpus or incoming-change scan; producer release or consumer handoff.

## Revisions and context

- LuCI source: clean `b2e0be4b46ec0fd43394c081fa7c50657af14011`, file
  `modules/luci-base/root/usr/share/rpcd/ucode/luci`, Git blob and SHA-256 in
  the [source-first oracle](../evidence/087-20261124-direct-rpc-current-ast/source-first-oracle.json).
- Producer: clean `7c62553b7a81b236b75d1b1fa0d50c612a020cc5`.
  The reused macOS extractor pack was built from
  `8375887ed14825dd59addbfd0df43616d9e684fb`; the extractor tree,
  pack-building scripts, grammar clone script, extractor descriptor and
  Cargo lock had no diff to the selected producer. Its pinned grammar was
  `4a243af329fae2f4ff01e0fc80133cbab8314600`; the binary SHA-256 was
  `c7bde2d31303127f6bf8ebbbb364a5a47840867b67962a013032a3b6bbe7f8d2`.
  Copied pack and locked dependency files were hash-checked before use.
- CodeQL executable: `CodeQL command-line toolchain release 2.27.4.`, SHA-256
  `bb3a754e126ed061b5f3356531cd5501872ab3864bd665b2d1afdbf8a67a146d`.
- Context: [current site census](../planning/mvp-direct-rpc-current-eligibility.md),
  [claim 081](081-current-luci-rpcd-direct-shell-slice.md), and the query/model
  scope issues [ucode #54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54)
  and [#50](https://github.com/lucas-albers-lz4/codeql-ucode/issues/50).

## Evidence required

1. The source-first oracle SHA-256
   `6350940a793c7f2ed1f45fc9ca4aeebfec58a67e257c36f0953627dd61b94604`
   was retained before extraction. It pins the LuCI source and synthetic
   fixture bytes, stage paths, two quoted AST spans, one raw control span,
   one different-field near miss, route/extraction identities and expected
   SARIF multiplicity. The [fixture](../evidence/087-20261124-direct-rpc-current-ast/controls.uc)
   and [testing query](../evidence/087-20261124-direct-rpc-current-ast/QuotedSwitchAst.ql)
   are portable.
2. Both staged files matched their pinned bytes. The route receipt selected
   each once as plain `rpcd_raw_mode_full_path`, with no excluded, uncertain,
   markup or duplicate inputs. The successful-file query returned exactly
   `usr/share/rpcd/ucode/luci` and `usr/share/rpcd/ucode/controls.uc` once
   each; the extraction-error query returned zero tuples.
3. The testing query selected exactly two rows. Each row carries five AST
   entities: `request.args.switch`, its `shellquote` call, the substitution,
   the template and the imported `popen` call. Their source URLs and exact
   ranges differ by line 343 versus 400; every entity category had two
   distinct source locations. No target-field quoted witness came from the
   synthetic different-field control.
4. The direct rule emitted exactly one SARIF result for the synthetic raw
   sibling at `controls.uc:11:37-56` (UTF-16, exclusive end), and no result
   for the two quoted current-source sites or the synthetic quoted `other`
   field. This exercises the rule's raw-substitution/quote distinction. The
   testing AST query filters specifically for `switch`, so its absence on
   `other` is by construction; the direct rule accepts any handler field and
   this fixture is not a field-specific negative control. These observations
   do not establish security or general precision.

## Run record

- Date and environment: 2026-11-24, macOS; canonical fresh run under ignored
  `work/direct-rpc-nearmiss-ast-20261124-c`, with unique stage, database,
  `HOME`, `TMPDIR`, output and writable cache paths. Preflight recorded
  about 122 GiB free disk and 65% system-wide free memory. The source and producer
  checkouts were clean at their full SHAs.
- Exact commands and exits: compile testing query, database init/index/finalize,
  successful-file query/decode, extraction-error query/decode, AST witness
  query/decode and direct-rule SARIF analysis: 11 commands, all exit 0.
  Their normalized exact arguments, stdout/stderr hashes and individual wall
  times are in the [run receipt](../evidence/087-20261124-direct-rpc-current-ast/run-receipt.json),
  SHA-256 `de40c4e05027a4f2f98b3bc23683068f070980d677e682b789bf324d0ccf95a0`.
  The summed command wall time was 12.724 seconds. Peak RSS is unavailable:
  macOS `/usr/bin/time -l` exited 1 under this sandbox because
  `sysctl kern.clockrate` was denied.
- Raw artifacts: the receipt commits to the raw preflight, command log,
  routing receipt, decoded diagnostic and AST rows, and SARIF hashes. Raw
  files and database remain under ignored `work/`; another machine must use
  the portable oracle, fixture/query and normalized receipt or perform a
  fresh run. The independent post-run comparison matched source blob/hash,
  stage hashes, extraction multiset, AST entity ranges, SARIF tuple and all
  11 command exits.
- Preparation history: an initial query compile outside a QL pack failed;
  a second compile lacked dependencies in run-owned `HOME`. A fresh
  preparation corrected both. Its first synthetic fixture returned the
  methods object directly and produced zero rule alerts, so it was rejected
  as an ineligible positive control. The canonical run used a top-level
  methods table returned through an exported pair, as the rule requires.
  Neither failed attempt is treated as a pass.
- Status and limits: Demonstrated only for the pinned source-staged AST and
  direct-rule behavior above. No package install, Linux release, or consumer
  step occurred.
- Follow-up: test helper caller-to-formal flow separately and retain the
  WOL and nested-shell sites as unsupported unknowns. Do not infer a safe
  current LuCI corpus from this bounded zero-result near miss.
