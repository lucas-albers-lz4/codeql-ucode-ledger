# Package 20 launch preparation

This source-first plan is for a v1 strict-consumer regression after the `validate_typed` refactor; it is not a v2 or real-policy handoff. [ORACLE.md](ORACLE.md) specifies the input hashes, expected exact paths and rows, and controls. Its earlier statement that the runner still needs routing assertions and calls `pack install` is superseded by the implementation described here.

`prepare.py` checks source pins/clean state, no visible CodeQL processes, unchanged extractor/generator/lock/build inputs from the retained build revision, grammar pin and bootstrap modification, completed offline build receipt, exact installed pack manifest and dependency files, tool executable digest and lock hashes. It creates no-hardlink producer and consumer checkouts in a new run and copies the installed extractor pack and dependencies. It records commands, results, hashes, free disk, Python/tool identity, and inherited HOME. Build-time rustc invocation is not independently logged; retained target metadata mentions rustc 1.100.0. The source and dependency checks are consistency checks, not authenticated provenance. Verify current ownership and fresh issue state and review resource sufficiency before launch; process polling is point-in-time only.

`run-producer.py` no longer installs packs. It uses the disposable checkout's QL workspace and extractor pack, plus explicit run-owned CodeQL common and compilation caches and `--no-default-compilation-cache`. It asserts complete routing decisions and counts before finalization, extracted source identities and errors, fixture/source and lock hashes, exact expected tables, full typed exporter SHA-256, and invalid span rejection. `run-consumer.py` uses no-hardlink copies, compares target rows and preserved artifacts, tests idempotence, and rejects downgrade, policy-bearing and 532.0 controls. Each command records exit, wall time, stdout and stderr plus `/usr/bin/time -l` peak RSS. Preparation and outer phase receipts preserve exit and elapsed time; consumer assertions cover only the four named effect/policy files.

When explicitly instructed and after verifying no heavy run is active, launch once from the ledger root with a new path:

```
python3 -B work/pkg20-typed-prep/launch.py work/pkg20-typed-run-<unique>
```

The launcher records each phase and stops on failure; inspect and poll live processes before any retry. Every retry needs a new run path. This prep does not set HOME: the inherited HOME is not run-owned, and setting TMPDIR, XDG cache, extractor cache and CodeQL's explicit caches does not prove all potential writes are confined. This is a documented isolation limitation. Paths are not credentials and logs may contain host paths; normalize reviewed copies before publishing. No CodeQL, producer, exporter, adapter or test was run in preparing this revision. These scripts have only been syntax-checked, not end-to-end validated; execution may reveal tool or route differences.
