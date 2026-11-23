# Claim 027 evidence bundle

This bundle contains the independent source-first fixture oracle, the exact two small inputs, ledger-authored queries, decoded result rows, and a normalized run receipt. `portable-receipt.json` maps normalized rows to the raw result paths and hashes retained under ignored `work/cfg-trim-oracle/run-20261122-a/`. That host-local directory contains the database, BQRS files, command logs, and timing output; it is not committed and will not be present in another clone.

The normal and trim-open fixtures are both expected to route as markup with `inconclusive` / `markup_not_modeled`. The trim-open no-graph result describes the pinned implementation only. It does not assert an intended policy exclusion.
