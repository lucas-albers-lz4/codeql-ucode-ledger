# Claim 090: local grammar override restores four-file extraction

**Status:** Demonstrated

**Scope:** A disposable producer built with a modified pinned Tree-sitter
grammar extracts two exact newer OpenWrt wifi sources that fail under merged
producer bytes, plus two eligible controls, each once with zero extraction
errors. A focused AST query sees the newly modeled dynamic-import syntax and
the semicolon-free exported function declaration.

**Out of scope:** A merged or released producer, installed package bytes,
Linux performance, runtime syntax validation, dataflow, security findings
and broad parser compatibility. The separate full v0.6 local prototype
run has its own bounded evidence and does not change this four-file claim.

## Revisions and context

- Producer checkout initially clean at
  `9166af76cf6944e1b3ea5856a9176366a1f7a6ee`. Local generated dbscheme,
  TreeSitter QL bindings and focused queries are recorded in the
  [producer receipt](../evidence/mvp-wifi-producer-prototype-20261124/receipt.json).
- Grammar base `4a243af329fae2f4ff01e0fc80133cbab8314600`, plus the
  [local source patch](../evidence/mvp-wifi-producer-prototype-20261124/grammar-source.patch).
  The override's diff SHA-256 is
  `008069fd058911c67429e89c29da153c6b007084a4f326f90d76ee2442176bd9`;
  it is not the unmodified locked grammar. The generated extractor SHA-256 is
  `169b55b06aff74907411cf9614ffbbe45dfb522c30a5455c03271a7e8c40fa69`.
- OpenWrt source checkout clean at captured head
  `bce40f6a15c273778061e8fceced7b9e0f58d99b`; CodeQL 2.27.4
  executable SHA-256
  `bb3a754e126ed061b5f3356531cd5501872ab3864bd665b2d1afdbf8a67a146d`.

## Evidence required

1. The [source-first oracle](../evidence/mvp-wifi-producer-prototype-20261124/source-first-oracle.json)
   preceded indexing and pinned four source paths, Git blobs, content hashes,
   staged paths, route expectations and one expected success each. Its raw
   SHA-256 was
   `51b88ef557d4ec8b7228598f9a6ab724efcc87f182673642fa36b153c7182341`.
   The source and staged bytes were rechecked after the run.
2. The [exact identity table](../evidence/mvp-wifi-producer-prototype-20261124/exact-identities.csv)
   records one successful-file identity for each of `lib/wifi/mac80211.uc`,
   `usr/share/ucode/wifi/utils.uc`, `lib/netifd/wireless.uc` and
   `lib/netifd/proto/wireguard.uc`. The CodeQL extraction-error query returned
   zero rows. The first two are the exact sources that failed in
   [claim 089](089-newer-openwrt-wifi-parse-boundary.md); the latter two are
   eligible changed/new source controls. A separate direct routing receipt
   showed the expected two shebang and two extension routes on the same
   staged bytes.
3. Focused query output showed one `DynamicImportExpression` with a `String`
   source child at `mac80211.uc:17:15–17:33`. Three distinct
   `ExportStatement` → `FunctionDeclaration` entities were observed in
   `utils.uc`; `board_wlan` spans lines 74–76 without a trailing semicolon.
   Entity IDs and exact ranges are retained in the receipt. This proves AST
   presence in this database, not module resolution, call semantics or flow.
4. The modified grammar's full local corpus tests passed: 244/244 plain
   Ucode, 89/89 markup and 151/151 documentation cases, plus query/highlight
   checks. The grammar parser also accepted the four exact source bytes.

## Run record

- Date/environment: 2026-11-24, macOS. Disposable producer, grammar, pack,
  database, stage, `HOME`, `TMPDIR` and caches were under ignored `work/`.
  The [receipt](../evidence/mvp-wifi-producer-prototype-20261124/README.md)
  records exact normalized commands, phase exits/times, output hashes and
  setup attempts. Cargo build exited zero in 16.860 seconds; generator,
  database init/index/finalize, diagnostic queries and focused AST queries
  exited zero. The outer macOS timing wrapper could not report peak RSS.
- Initial setup failures from missing pack index scripts, misplaced CodeQL
  dependencies and wrong custom-query placement were corrected inside the
  isolated run. The direct extractor routing-only call warned about its
  missing CodeQL diagnostic environment; the CodeQL database run and queries
  are the extraction evidence.
- The local grammar override adds a new AST node and schema relation. A full
  [v0.6 local prototype corpus run](../evidence/mvp-corpus-v0.6-prototype-local-run/README.md)
  now extracts all 128 selected sources exactly once and emits zero default
  suite SARIF results. At the original merged producer pin
  `9166af76cf6944e1b3ea5856a9176366a1f7a6ee`, claim 089's two parse
  failures remained. Producer PR #161 later merged grammar support as
  `104a398468f214961168d2edc9a10be45b80062f` and passed a Linux R2
  syntax fixture, but no released full 128-path Linux corpus run has yet
  transferred this local observation.
