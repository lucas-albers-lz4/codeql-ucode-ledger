# Claim 034: Trim delimiters in the bounded markup CFG

**Status:** Demonstrated for the local patch and the six pinned fixtures.

**Scope:** With the user-selected option A, a diagnostic-free bounded markup root can use ordinary or trim tokens independently at the opener and closer of an identifier expression tag. Its markup CFG has the same immediate ordering shape for all four delimiter combinations.

**Out of scope:** Upstream merge or policy disposition, runtime rendering and whitespace behavior, evaluation, reachability, flow, consumer handoff and general markup CFG coverage.

## Revisions and context

- Producer `codeql-ucode` at clean detached `11a53fd8e911573860950ee8e549b337a8742438`, with the recorded local patch applied in a disposable checkout. [Exact producer patch](../evidence/034-markup-trim-delimiters/producer.patch)
- Grammar `tree-sitter-ucode` at `4a243af329fae2f4ff01e0fc80133cbab8314600`, from a clean checkout. Six ledger fixture bodies and SHA-256 values are recorded in the [source-first oracle](../evidence/034-markup-trim-delimiters/source-first-oracle.json).
- CodeQL 2.27.4. The isolated pack copies trace to the pack built at `8375887ed14825dd59addbfd0df43616d9e684fb`. The scoped extractor, pack and lock inputs match. [Environment and digests](../evidence/034-markup-trim-delimiters/outputs/smoke/preflight.json)
- The user's choice implements option A locally for the boundary discussed in ucode issue #57. Claim 032 records the earlier ordinary-only baseline. [Tracking issue](https://github.com/lucas-albers-lz4/codeql-ucode/issues/57) · [Prior baseline](032-markup-trim-matrix-implementation.md)

## Evidence

1. All six exact fixture paths routed once as `markup` / `ut_markup_extension` / `inconclusive` / `markup_not_modeled`. All six extracted successfully and matched the archived source-byte digests. The standalone fixture database had zero file-located extraction errors and diagnostics. [Routing and extraction evidence](../evidence/034-markup-trim-delimiters/run-record.md)
2. The four identifier fixtures match the independent AST and field oracle. Their exact graph path runs from entry through leading raw text, identifier, tag completion and trailing raw text to exit. Each fixture contributes six nodes and five immediate edges with count one per projected tuple. The actual matrix had 48 AST and field rows across both positive and near-miss cases, with count one per identity. [Oracle comparison](../evidence/034-markup-trim-delimiters/outputs/matrix/oracle-comparison.json)
3. Both valid member-expression controls satisfy the delimiter guards. Their named expression field holds a member expression with the expected object and property. Both roots are unsupported and emit no nodes or edges. In the smoke's diagnostic-veto database, one injected warning on each of the otherwise supported ordinary and dual-trim fixtures suppressed their graphs while preserving successful extraction and their checked AST identities. [Decoded smoke outputs](../evidence/034-markup-trim-delimiters/outputs/smoke/decoded)

## Run record

On 2026-11-23, the patched producer smoke passed in 56.59 s. An unrelated CodeQL query was observed live during the smoke. The recorded process checks cover the later standalone run. The standalone matrix waited for a quiet process gate before creating a fresh database with separate caches. Its first query hit a missing workspace manifest. After copying the exact pinned manifest, the standalone query phase passed against that same newly finalized database. Both runs inherited `HOME`. The portable record includes exact commands, exit statuses, per-phase timings, raw-to-portable hashes and the decoded outputs. [Run record](../evidence/034-markup-trim-delimiters/run-record.md)
