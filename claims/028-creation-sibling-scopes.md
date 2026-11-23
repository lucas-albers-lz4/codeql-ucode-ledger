# Claim 028: sibling callable creation scopes

**Status:** Demonstrated for the two synthetic markup inputs and pinned producer below.

**Scope:** A supported callable and an unsupported call-bearing callable are siblings in one markup root. The creation graph preserves the root's top-level observation and the supported sibling's callable graph; the unsupported callable retains a scope identity without callable graph nodes. A second fixture changes that body to a supported numeric declaration and exercises both callable graphs.

**Out of scope:** Runtime calls, control-flow completeness, rendered behavior, security or general support for arbitrary callable bodies.

## Source and decision

The producer was [codeql-ucode `6010ff2c0f101f7629c6fe117a421f671c311a2b`](https://github.com/lucas-albers-lz4/codeql-ucode/tree/6010ff2c0f101f7629c6fe117a421f671c311a2b), with CodeQL 2.27.4. The source-derived [oracle](../evidence/028-creation-sibling-scope/ORACLE.md) precedes query results and specifies the exact fixture bytes, source identities and graph expectations. The module's [creation graph](https://github.com/lucas-albers-lz4/codeql-ucode/blob/6010ff2c0f101f7629c6fe117a421f671c311a2b/ql/lib/codeql/ucode/MarkupCreationCFG.qll) distinguishes top-level observation from callable-body eligibility. Broader markup control flow remains owned by [ucode #57](https://github.com/lucas-albers-lz4/codeql-ucode/issues/57).

## Observation and controls

Both `.ut` inputs routed exactly once as markup, with `inconclusive` / `markup_not_modeled`, and were successfully extracted with no diagnostics. Both roots were top-observed and not foundation-covered. The mixed file's first callable was covered and its call-bearing sibling unsupported; the AST confirmed the call expression and selected declarations. The all-covered fixture reported both callable scopes covered.

The mixed fixture yielded the expected 10 top-level nodes and four first-callable nodes, with nine top-level and three first-callable edges. The all-covered fixture yielded the same top-level structure plus both four-node, three-edge callable graphs: 18 nodes and 15 edges. Expected tuples and entity counts are in the [run evidence](../evidence/028-creation-sibling-scope/README.md). Each projected node identity had one entity. The edge query selects ordered endpoint identities and a literal count of one; since each endpoint projection was independently unique and `edge` is a relation, the exact observed edge tuples establish these bounded edges without asserting a directly measured edge-pair count. No cross-file or cross-scope edge tuple was observed.

## Run limits

Run D used an isolated database, output and configured cache copies; `HOME` was inherited and not run-owned. The [receipts](../evidence/028-creation-sibling-scope/README.md) retain the pack provenance, timing, failed setup and query attempts, and continuation against the same finalized database. Inputs were rehashed after the run. A successful command and matching rows do not authenticate execution, prove runtime behavior, or resolve general graph completeness. The results are limited to these two source shapes and this revision.
