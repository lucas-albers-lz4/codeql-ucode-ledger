# Package 6 source-first oracle: sibling callable scopes

Prepared before any Package 6 CodeQL execution or result inspection. The two input sources are `siblings.ut` and `siblings-all-covered.ut`; all
expected identities below are derived from their literal bytes, the pinned
producer implementation and documented/tested AST contract. Both files end
exactly at their final semicolon, with no trailing LF.

## Pins and source

- Producer: `6010ff2c0f101f7629c6fe117a421f671c311a2b` (detached evidence
  source originally inspected from the clean checkout at this SHA).
- Fixture: `siblings.ut`, SHA-256
  `940472ed365ba3c40aed4b42427ca703c05ece028069e696eb98d850808d7d16`.
- Source bytes (one line; columns are one-based and inclusive):

```ucode
{% x.y = function() { let n = 1; }; x.y = function() { call(); };
```

This is a valid markup root in the established fixture form. Both assignment
statements use the same textual target `x.y`. The first callable body contains
one lexical declaration initialized by a number. The second contains an
ordinary call expression, which is valid syntax but outside the supported
callable-body subset.

## Expected source identities

All rows have file identity `siblings.ut` and line 1. AST identities use the
same format as `MarkupCreationTestUtils.identity`:
`kind:startLine:startColumn:endLine:endColumn:parentKind:parentIndex`.

Top-level nodes, in source order (each has scope `top`):

1. `object-identifier` — `Identifier:1:4:1:4:MemberExpression:0`
2. `member-reference` — `MemberExpression:1:4:1:6:AssignmentExpression:0`
3. `function-creation` — `FunctionExpression:1:10:1:34:AssignmentExpression:2`
4. `assignment-completion` — `AssignmentExpression:1:4:1:34:ExpressionStatement:0`
5. `statement-completion` — `ExpressionStatement:1:4:1:35:Markup:1`
6. `object-identifier` — `Identifier:1:37:1:37:MemberExpression:0`
7. `member-reference` — `MemberExpression:1:37:1:39:AssignmentExpression:0`
8. `function-creation` — `FunctionExpression:1:43:1:64:AssignmentExpression:2`
9. `assignment-completion` — `AssignmentExpression:1:37:1:64:ExpressionStatement:0`
10. `statement-completion` — `ExpressionStatement:1:37:1:65:Markup:2`

Root scope identity is the markup root at `Markup:1:1:1:65:<root>:-1`.
Callable scope identities are the exact FunctionExpression locations:

- `callable:1:10` (`FunctionExpression:1:10:1:34:AssignmentExpression:2`), covered. Its graph nodes in order are `entry`,
  `initializer` — `Number:1:31:1:31:VariableDeclarator:2`,
  `declaration-completion` —
  `LexicalDeclaration:1:23:1:32:StatementBlock:1`, and `exit`.
- `callable:1:43` (`FunctionExpression:1:43:1:64:AssignmentExpression:2`), unsupported. The scope identity remains present, but it has
  no callable graph nodes because `call()` is not an allowed body node.

## Expected edges and counts

The complete top-level edge set is the adjacent pairs in this explicitly
numbered node sequence: `1→2`, `2→3`, `3→4`, `4→5`, `5→6`, `6→7`,
`7→8`, `8→9`, `9→10` (the numbers refer to the top-level identities above).
The first callable edge set is `entry → Number:1:31:1:31:VariableDeclarator:2`,
`Number:1:31:1:31:VariableDeclarator:2 → LexicalDeclaration:1:23:1:32:StatementBlock:1`,
and `LexicalDeclaration:1:23:1:32:StatementBlock:1 → exit`. Total expected
graph: 14 nodes and 12 edges. There are no nodes for the
unsupported second callable and no cross-scope edges.

The top-level count follows the module's `topAst` node classes and
`beforeAst`/`before` ordering; the graph has no top-level synthetic entry or
exit. The callable count follows `callableAst` plus `TEntry`/`TExit`. For any
edge, `before` first requires equal top scope or equal callable scope. Thus an
edge cannot join the top-level graph to either callable, or the two callable
scopes to one another. This is an implementation contract check, not an
observed query result.

## Eligibility and discriminating controls

- Positive: the first sibling has one direct lexical declaration with exactly
  one binding and a numeric initializer, meeting `isCallableCovered`.
- Eligible negative: the second sibling is a valid function body containing a
  call; `hasTopLevelObservation` deliberately excludes body syntax from its
  top-level subset, while `isCallableCovered` rejects the call for this
  callable only. Therefore it should not suppress the first sibling's callable
  graph or the root's top-level observation.
- Existing pinned source controls to retain alongside this case: `supported.ut`
  gives a supported callable; `body-call.ut` gives a valid call-bearing
  unsupported callable; `two-callables.ut` gives two callable sibling scopes.
  These are source-level eligibility controls only; no outputs were read for
  this oracle.

## Source and implementation basis

Reviewed only source and contract material at the stated producer pin:

- `docs/markup-cfg-creation.md`: defines top-level creation ordering, separate
  callable scopes, supported number-initialized declaration bodies, and no
  cross-scope edge.
- `ql/lib/codeql/ucode/MarkupCreationCFG.qll`: `hasTopLevelObservation`,
  `CallableScope`, `bodyAllowed`, `isCallableCovered`, `topAst`, `callableAst`,
  `Node`, `beforeAst`, and the equal-scope condition in `before`/`edge`.
- `ql/src/MarkupCreationTestUtils.qll`: exact scope/file/AST identity formats.
- `tests/data/markup-creation/{supported.ut,body-call.ut,two-callables.ut}` and
  `scripts/markup-creation-smoke.py`: establish valid fixture syntax and the
  declared positive/unsupported/sibling control shapes. Existing result tables
  and generated artifacts were not read.

No CodeQL command was run, no database or query output was inspected, and no
tracked project file was modified.

## Parallel all-covered sibling comparison

The paired comparison fixture is `siblings-all-covered.ut`, SHA-256
`885ea36bf4edfa571a860c0226642a491b007f40d58ca8ed660a7bea2a46fb23`:

```ucode
{% x.y = function() { let n = 1; }; x.y = function() { let m = 2; };
```

It preserves the two `x.y` assignments and first supported callable exactly;
only the second callable body changes from `call();` to a number-initialized
single-binding lexical declaration. This is the matching supported control
for the mixed fixture's eligible unsupported second body.

The expected root is `Markup:1:1:1:68:<root>:-1`. The two callable scope
identities are `callable:1:10`
(`FunctionExpression:1:10:1:34:AssignmentExpression:2`) and `callable:1:43`
(`FunctionExpression:1:43:1:67:AssignmentExpression:2`); both are covered.

Complete expected node set (all line 1; file `siblings-all-covered.ut`):

| Scope | Role | AST identity |
|---|---|---|
| top | object-identifier | `Identifier:1:4:1:4:MemberExpression:0` |
| top | member-reference | `MemberExpression:1:4:1:6:AssignmentExpression:0` |
| top | function-creation | `FunctionExpression:1:10:1:34:AssignmentExpression:2` |
| top | assignment-completion | `AssignmentExpression:1:4:1:34:ExpressionStatement:0` |
| top | statement-completion | `ExpressionStatement:1:4:1:35:Markup:1` |
| top | object-identifier | `Identifier:1:37:1:37:MemberExpression:0` |
| top | member-reference | `MemberExpression:1:37:1:39:AssignmentExpression:0` |
| top | function-creation | `FunctionExpression:1:43:1:67:AssignmentExpression:2` |
| top | assignment-completion | `AssignmentExpression:1:37:1:67:ExpressionStatement:0` |
| top | statement-completion | `ExpressionStatement:1:37:1:68:Markup:2` |
| callable:1:10 | entry | `entry` |
| callable:1:10 | initializer | `Number:1:31:1:31:VariableDeclarator:2` |
| callable:1:10 | declaration-completion | `LexicalDeclaration:1:23:1:32:StatementBlock:1` |
| callable:1:10 | exit | `exit` |
| callable:1:43 | entry | `entry` |
| callable:1:43 | initializer | `Number:1:64:1:64:VariableDeclarator:2` |
| callable:1:43 | declaration-completion | `LexicalDeclaration:1:56:1:65:StatementBlock:1` |
| callable:1:43 | exit | `exit` |

Complete expected edge set is the nine adjacent pairs in this explicitly
numbered top node sequence: `1→2`, `2→3`, `3→4`, `4→5`, `5→6`, `6→7`,
`7→8`, `8→9`, `9→10` (numbers refer to the top-level identities in the
table), plus these callable edges:

- `callable:1:10`: `entry → Number:1:31:1:31:VariableDeclarator:2`;
  `Number:1:31:1:31:VariableDeclarator:2 → LexicalDeclaration:1:23:1:32:StatementBlock:1`;
  `LexicalDeclaration:1:23:1:32:StatementBlock:1 → exit`.
- `callable:1:43`: `entry → Number:1:64:1:64:VariableDeclarator:2`;
  `Number:1:64:1:64:VariableDeclarator:2 → LexicalDeclaration:1:56:1:65:StatementBlock:1`;
  `LexicalDeclaration:1:56:1:65:StatementBlock:1 → exit`.

This file therefore has exactly 18 expected nodes and 15 expected edges. The
mixed fixture above has the same top-level paths and first callable graph, plus
the second callable scope identity but no second callable graph: 14 nodes and
12 edges. In both cases the callables are independent siblings; no edge may
cross from the top-level scope or between callable scopes. These are predeclared
sets from source/contract reasoning, not database or query observations.

## Predeclared extraction, AST and eligibility checks

The upcoming run, if executed, must first establish each fixture file's exact
successful extraction identity, exactly once, and zero diagnostics for both.
Both parser routes are expected to be `markup`; the route status and reason
are expected to be `inconclusive` / `markup_not_modeled`. This routing status is
not an extraction failure. For each root, the expected creation root status is `top-observed`.
Neither root is expected to be foundation-covered by `MarkupCFG::isCovered`.
These routing, extraction and root/scope assertions are predeclared checks,
not observations.

Additional source-derived AST assertions, each with multiplicity one per file:

| File | AST identity | Expected significance |
|---|---|---|
| `siblings.ut` | `VariableDeclarator:1:27:1:31:LexicalDeclaration:1` | Supported binding/value declarator in callable `1:10` |
| `siblings.ut` | `CallExpression:1:56:1:61:ExpressionStatement:0` | Valid unsupported call expression in callable `1:43` |
| `siblings.ut` | `ExpressionStatement:1:56:1:62:StatementBlock:1` | Enclosing call statement in callable `1:43` |
| `siblings-all-covered.ut` | `VariableDeclarator:1:27:1:31:LexicalDeclaration:1` | First supported binding/value declarator |
| `siblings-all-covered.ut` | `VariableDeclarator:1:60:1:64:LexicalDeclaration:1` | Second supported binding/value declarator |

The existing expected number identities at columns 31 and 64 each have parent
`VariableDeclarator` index 2. The lexical declarations have parent
`StatementBlock` index 1. The mixed file must expose exactly two callable
scopes, covered at `1:10–1:34` and unsupported at `1:43–1:64`; the all-covered
file must expose exactly two covered scopes at `1:10–1:34` and `1:43–1:67`.
The unsupported call's AST presence is expected independently of the fact that
its callable graph has no nodes. No query results have been inspected to
establish any of these expectations.
