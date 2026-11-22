# Claim 024 evidence: declaration and initializer AST observations

This receipt preserves the source-first oracle, four staged inputs, ledger-authored queries, normalized decoded results, command history, setup failures and provenance for the bounded AST prequery. It is a ledger observation only.

## Contents

- `inputs/prequery-manifest.json` fixes all four input digests, route expectations, controls and malformed-input diagnostics before output inspection. `inputs/source/` carries those exact source bytes.
- `oracle/source-first-oracle.json` contains expected entity kinds, spans and parent kind/index descriptors.
- `queries/` contains the exact ledger-authored queries and SHA-256 values are listed in `outputs/run-receipt.json`.
- `outputs/` retains normalized decoded extraction, error, all-diagnostics, AST inventory, positive value-relation and negative no-value-relation outputs. `source://` URIs are relative to the staged `source` root.
- `outputs/*commands.json` preserves exact command arguments, statuses, wall times, reported peak memory, and hashes of the timing/stderr files for all three attempts, including failures and interruption.
- `outputs/run-receipt.json` records source/tool/pack/cache provenance, outcome comparisons, and the attempt history.

## Evidence boundary

The five returned entity-bearing AST rows have distinct source spans and match the independent oracle. Internal entity IDs were not decoded. The parent kind/index descriptors are query-observed values, not evidence of a parent entity identity beyond the returned relation. The initialized declarator has one returned `d.getValue() = n` row with `n` typed as `Number`; the no-initializer control has one row for `not exists(d.getValue())`. These observations are limited to the four staged source files. The `.ut` route remains `markup_not_modeled` / inconclusive. This does not establish general markup support, CFG construction, rendering, reachability, flow, or security.

The unsuccessful workspace-resolution and locked-pack-import attempts and the interrupted third attempt are retained in the command receipts and `run-receipt.json`; the final queries were run against the already finalized retry-01 database from inside its disposable producer query pack. No database or large generated artifact is included here. Host paths in command strings are represented by portable placeholders.
