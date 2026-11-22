# Wave 2 portable receipt

Preparation and evidence for the bounded `view.ut` markup AST inventory. The delegated preparation and run did not modify tracked ledger files; the claim and receipt were added afterward. No query or extraction command was retried.

## Contents

- `oracle/source-first-oracle.json`: source-first expectations as prepared before query execution.
- `inputs/runner-manifest.json` and `inputs/source/`: four staged bytes and predeclared route/hash/control expectations.
- `outputs/routing.json`, `extracted.json`, `errors.json`, and `all-diagnostics.json`: decoded producer receipts with exact source URIs normalized to `file:///__SOURCE_ROOT__/...`.
- `outputs/markup-view-inventory.json` and `markup-nearmiss-audit.json`: both actual decoded QL outputs, with entity URLs preserved under the same normalization.
- `outputs/wave2-query-comparison.json`: corrected interpretation plus all rows, including the nine rows outside the predeclared target subset. The as-produced comparison is also retained; its `exact_shared_parent_observed_for_view_text_nodes` field overstates evidence because the query selected parent descriptors, not parent entities.
- `outputs/commands-and-timings.json`: every extraction, diagnostic, query and decode command, status, wall time and peak RSS where recorded.
- `queries/`: exact local QL sources and reviewed runner used for the run.
- `outputs/provenance.json`: pins, pack/cache provenance, actual status, failures during preparation, and path normalization.
- `outputs/archive-check.json`: independent post-run comparison of the four archived source identities and hashes with the pre-query manifest; not execution attestation.
- `artifact-index.json`: portable file hashes and byte sizes.

The predeclared target identities appeared exactly once with expected spans, source text and parent kind/index. All four files routed and extracted once with zero diagnostics. The broad literal-lookalike audit returned no `ExpressionTag` or `CallExpression` entities. The mixed-template fixture was a clean extraction positive but was not a QL target in the prepared inventory query. Parent entity identity was not selected; matching parent kind/span/index are the observed evidence.

Large raw BQRS files, database, and unnormalized `/usr/bin/time -l` stderr remain under ignored `work/wave2-run/execution/`; this receipt contains normalized JSON and structured command timings instead.
