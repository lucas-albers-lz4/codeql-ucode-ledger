# Decision for ucode #57 on trim-delimited expression tags

The user selected option 1 on 2026-11-23: the bounded markup ordering graph
should cover clean identifier tags with trim delimiters at either or both
ends, with the same ordering roles as the ordinary tag. This is a newly
selected policy, not evidence of prior documented upstream intent.
[Claim 034](../../claims/034-markup-trim-delimiters.md) records the tested
disposable implementation; the producer patch is not yet merged upstream.

## Current evidence

The remote producer main checked on 2026-11-22 was
`dc7310d0d2fb57047aa0c5653d9a32d6876c2d81`. The disposable producer snapshot
used for source inspection contains `1ccf5268e6915dc8d4cbb926b28be8ff79bcb0ed`.
The remote comparison between these revisions adds receiver observation
evidence and its attributes only. In turn, the change from claim 027's
`6010ff2c0f101f7629c6fe117a421f671c311a2b` through the roadmap revision
leaves the bounded markup CFG implementation and grammar pin unchanged.
[Latest delta](https://github.com/lucas-albers-lz4/codeql-ucode/compare/1ccf5268e6915dc8d4cbb926b28be8ff79bcb0ed...dc7310d0d2fb57047aa0c5653d9a32d6876c2d81)

- The generated grammar represents an ordinary or trim token at each delimiter
  field of the same `expression_tag`. The raw-text scanner marks the preceding
  token end at the tag boundary. These are syntax facts for the pinned grammar.
  [Grammar](https://github.com/m00qek/tree-sitter-ucode/blob/4a243af329fae2f4ff01e0fc80133cbab8314600/common/define-grammar.js#L184-L207)
  · [Scanner](https://github.com/m00qek/tree-sitter-ucode/blob/4a243af329fae2f4ff01e0fc80133cbab8314600/common/scanner.h#L83-L163)
- The current closed CFG subset has ordinary opener/closer requirements in two
  places. Its child allowlist accepts ordinary delimiter tokens and its
  per-tag coverage check independently requires the ordinary token classes.
  This implies rejection of trim-close and dual trim by source inspection.
  Claim 027 observed the normal and trim-open cases only. Its trim-open fixture
  extracted cleanly and yielded no nodes or edges.
  [CFG](https://github.com/lucas-albers-lz4/codeql-ucode/blob/dc7310d0d2fb57047aa0c5653d9a32d6876c2d81/ql/lib/codeql/ucode/MarkupCFG.qll#L29-L69)
  · [Claim 027](../../claims/027-markup-trim-open-cfg.md)
- Issue #57 remains open, unassigned and marked deferred. Its author
  `lucas-albers-lz4` also authored and merged the bounded implementation.
  The merged proposal and implementation describe simple identifier tags
  and a closed subset. The merged roadmap calls the two existing ordering
  slices separately approved and keeps broader work deferred. None states
  a decision about the trim-token variant. The merged LuCI measurement
  already uses an ordinary identifier/member expression control pair. Its
  negative is a member expression, and its coverage result does not determine
  trim policy.
  [Issue #57](https://github.com/lucas-albers-lz4/codeql-ucode/issues/57)
  · [Proposal PR #139](https://github.com/lucas-albers-lz4/codeql-ucode/pull/139)
  · [Implementation PR #142](https://github.com/lucas-albers-lz4/codeql-ucode/pull/142)
  · [Measurement PR #147](https://github.com/lucas-albers-lz4/codeql-ucode/pull/147)
  · [Roadmap PR #148](https://github.com/lucas-albers-lz4/codeql-ucode/pull/148)

## Options for the maintainer

1. **Admit all four delimiter combinations.** Keep the single direct
   `Identifier` child, exact child count, extraction-diagnostic veto and
   all existing unsupported forms. In the current implementation both
   delimiter checks must recognize their exact ordinary or trim token
   classes. Keep the token classes and AST locations intact. This is the
   recommended bounded ordering extension because the graph already uses
   the identifier and tag as executable-order identities and the delimiters
   supply syntax only.
2. **Keep ordinary-only coverage.** Document both trim token exclusions as
   part of the public contract. Add exact trim-open, trim-close and dual-trim
   clean-extraction negatives alongside the ordinary positive. Optionally
   revisit their status under #57 when there is a separate design decision.

## Proposed acceptance matrix

Use these five ASCII fixtures with no final newline and stage each as a
separate markup root. Before examining output, derive exact source hashes,
delimiter and child AST classes and one-based inclusive spans, parent/child
indexes, and graph tuples. This initial matrix is a proposal.

| Fixture bytes | Expression child | Opener and closer | Recommend |
| --- | --- | --- | --- |
| `A {{ x }} B` | Identifier | ordinary / ordinary | covered |
| `A {{- x }} B` | Identifier | trim / ordinary | covered |
| `A {{ x -}} B` | Identifier | ordinary / trim | covered |
| `A {{- x -}} B` | Identifier | trim / trim | covered |
| `A {{- x.y -}} B` | MemberExpression | trim / trim | unsupported |

For each covered case the exact ordering roles are entry, leading raw text,
identifier, expression-tag completion, trailing raw text, exit. Verify all
six nodes and five immediate normal edges with exact root scope and AST
identity. Delimiters remain separate AST tokens and add no graph nodes.
For the member near miss, verify that extraction reports the actual member
shape and the graph has zero nodes and edges. Under option 2, expect the
ordinary path only and zero graph rows for each trim fixture.

An accepted change should update the producer contract and targeted smoke
together under #57. Before running tests, pin current producer and grammar
revisions, verify the extractor and lock digests, use a disposable copy
and run-owned database and caches, and retain exact parsed route decisions,
selected identities, all diagnostics and graph/output multiplicity. Assert
the existing fixtures still meet the same contracts, including diagnostic
vetoes. The test concerns AST-derived ordering only. Whitespace rendering,
runtime evaluation or reachability, output escaping, data flow, security
and consumer routing remain outside this proposed decision.
