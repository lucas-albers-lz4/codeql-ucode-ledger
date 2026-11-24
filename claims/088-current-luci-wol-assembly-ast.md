# Claim 088: current LuCI WOL assembly AST identities

**Status:** Demonstrated

**Scope:** One fresh source-staged macOS CodeQL 2.27.4 database over the pinned
LuCI WOL rpcd file and one synthetic control file. The testing query observes
distinct AST entities for `request.args.args`, `shellquote` declaration and
callback argument, `map`/`parts`, `join`, concatenation and imported `popen`.

**Out of scope:** A flow or sanitizer model; an alert, runtime reachability,
authorization, safety or vulnerability conclusion; installed package bytes;
other assembly forms and full-corpus coverage.

## Revisions and context

- LuCI: clean `b2e0be4b46ec0fd43394c081fa7c50657af14011`; source
  `applications/luci-app-wol/root/usr/share/rpcd/ucode/luci.wol`, Git blob
  `fd9e9f0485ab6baec96ae089caf1089a6d471c99`, SHA-256
  `51214ec57bcbd8d50e65016efda2a05e8eb7822dc7e510d014965834c61ef92b`.
- Producer: clean `977331713b4b8b5574813bee0884245bf6db2752`.
  The isolated run copied its QL source and locks. The reused macOS extractor
  pack binary SHA-256 was `c7bde2d31303127f6bf8ebbbb364a5a47840867b67962a013032a3b6bbe7f8d2`;
  its build revision was `8375887ed14825dd59addbfd0df43616d9e684fb`.
  The extractor/schema paths had no diff to the selected producer, and the
  locks matched. Pinned grammar revision:
  `4a243af329fae2f4ff01e0fc80133cbab8314600`.
- CodeQL: `2.27.4`, executable SHA-256
  `bb3a754e126ed061b5f3356531cd5501872ab3864bd665b2d1afdbf8a67a146d`.
  Context: [WOL candidate](../planning/mvp-next-wol-assembly-check-20261124.md),
  [ucode #54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54)
  and [#50](https://github.com/lucas-albers-lz4/codeql-ucode/issues/50).

## Evidence required

1. The [source-first oracle](../evidence/088-20261124-wol-assembly-ast/source-first-oracle.json)
   was written before compilation/extraction. It pins source and fixture
   hashes, stage identities, two expected witness line pairs, successful-file
   multiplicities and eligible near misses. The oracle SHA-256 was
   `92d86039566cf085e424f763d0bceb8427d4ce313ed43a6a3fdfcfeb08116e5a`.
2. Both files routed once as plain `rpcd_raw_mode_full_path`. The successful
   extraction multiset was exactly `usr/share/rpcd/ucode/luci.wol: 1` and
   `usr/share/rpcd/ucode/controls.uc: 1`, with zero extraction-error tuples.
3. The [testing query](../evidence/088-20261124-wol-assembly-ast/WolAssemblyAst.ql)
   returned exactly two rows. The real WOL source witness has source line 41
   and sink line 42; the [synthetic unquoted sibling](../evidence/088-20261124-wol-assembly-ast/controls.uc)
   has lines 11–12. Each row contains nine distinct AST source ranges, and
   every entity category differs across the two files. The
   [normalized receipt](../evidence/088-20261124-wol-assembly-ast/run-receipt.json)
   lists all ranges. Source snippets at those ranges were checked against
   the retained staged bytes.
4. The synthetic `fixed_args`, `other_callback` and `no_join` methods extracted
   in the same file and yielded no witness row. They respectively replace
   the request-derived array, the callback identifier and the join operation.
   The positive uses an identity callback; the real WOL source uses the
   single-quoting helper and a fixed-executable comparison at line 40. These
   source differences do not establish runtime safety.

## Run record

- Date and environment: 2026-11-24, macOS. Canonical run under ignored
  `work/wol-assembly-ast-20261124-a`, with run-owned stage, database, outputs,
  `HOME`, `TMPDIR` and caches. The [preflight](../evidence/088-20261124-wol-assembly-ast/preflight.json)
  records clean pins, hashes, about 122 GiB free disk and 65% free memory.
- An initial compile exited 2 because locked dependencies had been copied to
  the query cache rather than run-owned `HOME/.codeql/packages`; it was not
  treated as a pass. After copying the same locked dependencies into that
  `HOME`, compilation, database init/index/finalize, the successful-file and
  error queries/decodes, and the AST query/decode all exited 0. The ten
  canonical commands took 10.060 seconds in total. Individual exact commands,
  exits, wall times, stdout/stderr hashes and raw artifact hashes are in the
  [receipt](../evidence/088-20261124-wol-assembly-ast/run-receipt.json),
  SHA-256 `a7f7ebea89882b2d47419e334cedd4b785d03386aaa9e6b2abb1ed704f87e599`.
  Peak RSS was unavailable because macOS `/usr/bin/time -l` was denied by the
  sandbox.
- The raw database and outputs remain under ignored `work/` on this machine.
  The receipt normalizes the run root and CodeQL executable in command text;
  it is portable review evidence, not execution authentication.
- **Limit:** The query matches the `shellquote` declaration in the same file
  and the `parts` use by local name. It does not resolve either binding or
  prove `map`/`join` data flow. The selected `popen` is recognized by the
  producer's same-file named-import model. A reviewed flow and quote model,
  more controls and fresh SARIF are prerequisites for an alert claim.
