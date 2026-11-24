# Local plain and markup typed AST syntax smoke

The disposable producer's source-first fixture manifest fixes exact bytes
for `plain.uc` and `markup.ut`, expected routes and five typed AST rows.
The plain fixture contains static import, dynamic `import()`, a similarly
named `importer()` call, and both explicit-semicolon and semicolon-free
exported functions. The markup fixture contains dynamic import and an
explicitly terminated exported function in statement tags.

The actual `run_newer_grammar_syntax` release-gate function was exercised
locally against the refined producer pack with a macOS command wrapper.
It created a fresh database under ignored
`work/mvp-grammar-syntax-smoke-20261124-c`. The
[normalized receipt](receipt.json) records the source-first oracle hash,
exact commands/exits, routing and diagnostic hashes, and observed rows;
raw files remain under `work/`.

Both files extracted once with zero errors. The `.uc` file took the plain
extension route; the `.ut` file took the markup-inconclusive route. The QL
query returned exactly the declared five rows: plain dynamic import at
`2:15`, plain exports at `4:1` and `5:1`, markup dynamic import at `2:18`,
and markup export at `3:4`. The static import and `importer()` controls
produced no dynamic-import row. This checks projected typed AST locations;
it does not infer distinct entity counts from identical CSV tuples.

An earlier isolated database attempt stopped at query resolution because
the query was placed in the test pack without its dependency lock; the
query moved to the source pack and a new database was used. This is local
modified-producer evidence. Hosted Linux behavior and semantic import
resolution remain unverified.
