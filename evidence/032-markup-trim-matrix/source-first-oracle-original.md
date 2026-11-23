# Conditional test oracle for trim-delimited markup ordering

This source-only oracle accompanies the [policy disposition](trim-policy-disposition.md) for [ucode #57](https://github.com/lucas-albers-lz4/codeql-ucode/issues/57). It supplies expected observations for either maintainer decision. Neither option is recorded as approved here. No extraction or query ran for this matrix. [Claim 027](../../claims/027-markup-trim-open-cfg.md) is prior evidence for different, tag-only fixtures.

## Exact inputs and extraction expectations

Stage the following five files under `usr/share/ucode/controls/`. Each body is exactly the ASCII between the inline code delimiters, with a single space where shown, no BOM and no terminal newline.

| File | Body | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `plain.ut` | `A {{ x }} B` | 11 | `557c70f3707a0f1f22bd06e189c8d303ee99542d2767eb59226ac8010c8220da` |
| `trim-open.ut` | `A {{- x }} B` | 12 | `fbeecce989e50bb9bd205afd29f8e717469dc977e57131f4ffa24378a5833e49` |
| `trim-close.ut` | `A {{ x -}} B` | 12 | `afde724719c5f9bf3204a47b13d9028a3a0bb0ac60008827bf72602551da519a` |
| `trim-both.ut` | `A {{- x -}} B` | 13 | `d897ab97d9025f6eacaa460015d71757746888efacef854955b31e3ac283f03f` |
| `trim-member.ut` | `A {{- x.y -}} B` | 15 | `2b1650e98fcd52c9e18a10cfe5ad5016031ea4aae0ce412a309f4ef02858005d` |

For either option, expect five input, markup and markup-inconclusive entries, with all other routing counts zero. For each staged path, expect classification `markup`, reason `ut_markup_extension`, status `inconclusive`, and inconclusive reason `markup_not_modeled`. Expect each exact successful-file identity once and zero extraction errors or file-located ucode diagnostics. The proposed CFG choice leaves selection and extraction criteria as described. [Routing implementation](https://github.com/lucas-albers-lz4/codeql-ucode/blob/dc7310d0d2fb57047aa0c5653d9a32d6876c2d81/extractor/src/extractor.rs#L128-L154)

## AST identities

Every span below is on line 1 with one-based inclusive columns. Each table cell is one distinct AST identity in its file. Check these seven exact root, root-child and tag-child tuples per file, including their fields, parents and indexes. For every row, the root is parentless, the leading `RawText`, `ExpressionTag` and trailing `RawText` are its children at indexes 0, 1 and 2, and the opener, expression and closer are children of the tag at indexes 0, 1 and 2. The leading raw source slice is `A ` and the trailing slice is ` B`.

| File | `Markup` | Leading `RawText` | `ExpressionTag` | Opener class and span | Expression class and span | Closer class and span | Trailing `RawText` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `plain.ut` | 1–11 | 1–2 | 3–9 | `ExpressionTagOpen` 3–4 | `Identifier` 6–6 | `ExpressionTagClose` 8–9 | 10–11 |
| `trim-open.ut` | 1–12 | 1–2 | 3–10 | `ExpressionTagTrimOpen` 3–5 | `Identifier` 7–7 | `ExpressionTagClose` 9–10 | 11–12 |
| `trim-close.ut` | 1–12 | 1–2 | 3–10 | `ExpressionTagOpen` 3–4 | `Identifier` 6–6 | `ExpressionTagTrimClose` 8–10 | 11–12 |
| `trim-both.ut` | 1–13 | 1–2 | 3–11 | `ExpressionTagTrimOpen` 3–5 | `Identifier` 7–7 | `ExpressionTagTrimClose` 9–11 | 12–13 |
| `trim-member.ut` | 1–15 | 1–2 | 3–13 | `ExpressionTagTrimOpen` 3–5 | `MemberExpression` 7–9 | `ExpressionTagTrimClose` 11–13 | 14–15 |

In the last file, also check that the member itself owns the `object` field `Identifier` `x` at 7–7 and the `property` field `PropertyIdentifier` `y` at 9–9 and has no optional chain. This is a field-level check. It does not inventory the member's punctuation descendants. The other four tag expression children are the single identifier `x`.

The producer pins grammar `4a243af329fae2f4ff01e0fc80133cbab8314600`. Its markup start rule takes the leading text sequence; that sequence admits raw text and expression tags. The expression-tag rule fixes the opener/expression/closer order and allows the ordinary or trim token at each delimiter field. The scanner marks the raw-text end at the next tag boundary, consumes the full opener or closer including its optional dash, and starts the trailing raw token after the closing delimiter. The member rule exposes its object and property through the named fields. These source rules and the existing generated AST field definitions were reviewed separately from the span calculation. [Grammar pin](https://github.com/lucas-albers-lz4/codeql-ucode/blob/dc7310d0d2fb57047aa0c5653d9a32d6876c2d81/scripts/clone-grammar.sh#L5-L9) · [Markup grammar](https://github.com/m00qek/tree-sitter-ucode/blob/4a243af329fae2f4ff01e0fc80133cbab8314600/common/define-grammar.js#L149-L207) · [Scanner](https://github.com/m00qek/tree-sitter-ucode/blob/4a243af329fae2f4ff01e0fc80133cbab8314600/common/scanner.h#L83-L163) · [Member rule](https://github.com/m00qek/tree-sitter-ucode/blob/4a243af329fae2f4ff01e0fc80133cbab8314600/common/define-grammar.js#L628-L632)

## Conditional graph tuples

For every **covered** row below, let `R` be the exact `Markup` identity for that file. The complete node multiset has these six tuples `(scope, role, AST identity)`, each once.

| Key | Scope | Role | AST identity |
| --- | --- | --- | --- |
| `E` | `R` | `entry` | absent |
| `L` | `R` | `raw-text` | leading `RawText` from the table |
| `I` | `R` | `identifier` | tag child `Identifier` from the table |
| `T` | `R` | `tag-completion` | `ExpressionTag` from the table |
| `B` | `R` | `raw-text` | trailing `RawText` from the table |
| `X` | `R` | `exit` | absent |

The complete immediate normal edge multiset is `(E,L), (L,I), (I,T), (T,B), (B,X)`, each once in scope `R`. For every **unsupported** row, expect `isCovered(R)` false and an empty node and edge multiset. The current graph identifies nodes from their scope and role or exact AST entity and orders nested nodes before their enclosing tag and siblings by parent index. It gives delimiters no graph node. [Node and edge definitions](https://github.com/lucas-albers-lz4/codeql-ucode/blob/dc7310d0d2fb57047aa0c5653d9a32d6876c2d81/ql/lib/codeql/ucode/MarkupCFG.qll#L80-L141)

| File | Option A, admit all identifier delimiters | Option B, ordinary-only |
| --- | --- | --- |
| `plain.ut` | covered, 6 nodes and 5 edges | covered, 6 nodes and 5 edges |
| `trim-open.ut` | covered, 6 nodes and 5 edges | unsupported, 0 nodes and 0 edges |
| `trim-close.ut` | covered, 6 nodes and 5 edges | unsupported, 0 nodes and 0 edges |
| `trim-both.ut` | covered, 6 nodes and 5 edges | unsupported, 0 nodes and 0 edges |
| `trim-member.ut` | unsupported, 0 nodes and 0 edges | unsupported, 0 nodes and 0 edges |

The member fixture is a discriminating expression-shape near miss under option A because both delimiters would qualify. Under option B its delimiters already exclude it, so that row alone cannot distinguish the member check. Retain the producer's existing ordinary member-expression control for that purpose under either option. [Existing ordinary near miss](https://github.com/lucas-albers-lz4/codeql-ucode/blob/dc7310d0d2fb57047aa0c5653d9a32d6876c2d81/docs/evidence/markup-cfg-real/controls/ordinary-negative.ut)

If testing is authorized, compare entity counts within the projected identities and edge endpoint pairs as well as the projected rows, and preserve any mismatch. This matrix concerns extracted AST and immediate ordering. It supplies no expectation about rendering, runtime whitespace, expression evaluation, reachability, binding or data flow.
