# Source-derived oracle for bounded sibling call support

Prepared from literal fixture bytes, published producer source and upstream
fixture assertions before inspecting any CodeQL output for this refresh.
`expected.json` fixes the exact predicted root, scope, graph node and graph
edge tuples, plus selected AST witnesses. `expected.py` records their
source derivation. Expected projections have multiplicity one throughout.
Graph edges are ordered endpoint pairs. Endpoint entity counts establish
uniqueness of the selected projection. Every predicted edge stays within
one fixture and scope.

## Source and locks

- Producer `11a53fd8e911573860950ee8e549b337a8742438`, fetched as
  `origin/main` and checked out detached and clean. Claim 028's historical
  baseline was `6010ff2c0f101f7629c6fe117a421f671c311a2b`.
- [Producer #151](https://github.com/lucas-albers-lz4/codeql-ucode/pull/151)
  merged at the current pin. The bounded model source changes are
  `4f79502` and `2fe6745`. Broader markup CFG/dataflow remains open
  under [producer #57](https://github.com/lucas-albers-lz4/codeql-ucode/issues/57).
- Grammar source pin as declared by `scripts/clone-grammar.sh` is
  `4a243af329fae2f4ff01e0fc80133cbab8314600`. That script pins the grammar
  development dependency to tree-sitter 0.26.8 in the staged copy.
- SHA-256 for `Cargo.lock` is
  `20678c3cbb29632a9369bdb3c735af9ee63c9443879db38847fbda9813aa0a77`.
  SHA-256 is `bce2891940f09fcac3337b250707047ba9fd06d307abdbc7cb42c2ed193751a3`
  for both `ql/lib/codeql-pack.lock.yml` and `ql/src/codeql-pack.lock.yml`.
  Git reports no delta since claim 028 in either lock, `Cargo.lock`,
  `extractor/` or `scripts/clone-grammar.sh`. A run must establish actual
  extractor and dependency identities separately.
- Oracle JSON SHA-256
  `b3373b7c2b8511020fd255b0db5b4796f0cbc71defaa31de3393b95d07b133f3`.
  Generator SHA-256
  `d81f629b2fae41058c72a344b5be9d95aaf72e6142d75230f89185139413aee4`.

The three files in `fixtures/` end exactly at their final semicolon. The
first two preserve the historical fixture bytes. The table lists SHA-256
and the exact replacement body in the second callable.

| Fixture identity | Second body | SHA-256 |
|---|---|---|
| `siblings.ut` | `call();` | `940472ed365ba3c40aed4b42427ca703c05ece028069e696eb98d850808d7d16` |
| `siblings-all-covered.ut` | `let m = 2;` | `885ea36bf4edfa571a860c0226642a491b007f40d58ca8ed660a7bea2a46fb23` |
| `siblings-computed-callee.ut` | `obj[key]();` | `e4781ff609e500d449f48641a418a8ee1f211ef6d68fea080d71826d6b728885` |

The expected routing receipt for each exact fixture identity is one row
with parser `markup`, reason `ut_markup_extension`, status
`inconclusive` and inconclusive reason `markup_not_modeled`. The expected
successful extraction set contains these three identities, once each.
The expected diagnostic set is empty.

## Graph and AST contract

The current `MarkupCreationCFG.qll` keeps the same top-level observation
and source-order edge construction as the prior pin. Each root is expected
to be `top-observed` and uncovered by the foundation `MarkupCFG`.
All three retain a ten-node, nine-edge top-level path and the identical
four-node, three-edge first callable at `1:10–1:34`. Changing the second
body shifts only the source endpoints of its top-level creation,
assignment-completion and statement-completion nodes.

- `siblings.ut` is the direct-call positive. Current coverage permits an
  identifier callee and an empty argument list as a direct expression
  statement. The second scope `1:43–1:64` is covered. Its predicted path
  is entry → `Identifier:1:56:1:59:CallExpression:0` (identifier) →
  `CallExpression:1:56:1:61:ExpressionStatement:0` (call-completion) →
  `ExpressionStatement:1:56:1:62:StatementBlock:1` (statement-completion) →
  exit. Totals are 19 nodes and 16 edges. Under claim 028 this exact
  scope and body were present in the AST but emitted no callable graph.
- `siblings-all-covered.ut` preserves the numeric regression control.
  The second scope `1:43–1:67` remains covered, with entry →
  `Number:1:64:1:64:VariableDeclarator:2` (initializer) →
  `LexicalDeclaration:1:56:1:65:StatementBlock:1`
  (declaration-completion) → exit. Totals are 18 nodes and 15 edges.
- `siblings-computed-callee.ut` is the eligible near miss. It still has a
  direct no-argument call statement, with a subscript expression as its
  callee. The `simpleRef` check rejects a `SubscriptExpression`.
  The second scope `1:43–1:68` retains its identity and is expected
  unsupported with zero nodes and edges. Totals are 14 nodes and 12 edges.
  Require the AST to expose `SubscriptExpression:1:56:1:63:CallExpression:0`,
  `CallExpression:1:56:1:65:ExpressionStatement:0`, and
  `ExpressionStatement:1:56:1:66:StatementBlock:1`. Each expected
  node is singular and the other sibling retains its graph.

These predictions derive from `bodyAllowed`, `simpleRef`, `callChild`,
`isCallableCovered`, `callableAst`, `getRole`, and `beforeAst` in
`ql/lib/codeql/ucode/MarkupCreationCFG.qll`, the generated markup AST
class definitions, and the source/assertions in
`scripts/markup-creation-smoke.py` and
`scripts/markup-call-controls-smoke.py`. Upstream's `body-call.ut` asserts
the equivalent direct-call path at its own coordinates. Its separate
computed-argument control supplies an example of subscript syntax. The
ledger's near miss places that syntax specifically in the callee position.
This is an oracle for a bounded static source-order graph.
