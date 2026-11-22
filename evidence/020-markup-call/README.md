# Markup call inventory receipt

`expectations.json` was written from the pinned source, installed-path
inventory, and query contract before the first database query. It records all
three selected paths, hashes, expected classifications and five expected
rows. It is a local contemporaneous record, not a cryptographic timestamp.
`MarkupCalls.ql` is the ledger-authored query copied into the disposable
producer's query pack; it is not an upstream committed query. `calls.csv` and
`errors.csv` are unmodified decoded output. `extracted.csv` and `routing.json`
replace only the absolute staged source prefix with `<SOURCE_ROOT>`.

`commands.json` preserves commands, exit statuses, Python monotonic wall time,
and real/user/system times and maximum RSS reported by macOS `/usr/bin/time
-l`. `<RUN_ROOT>` and `<CODEQL>` replace the actual absolute paths. The index
command additionally set `CODEQL_UCODE_STAGED_ROOT=<RUN_ROOT>/src`. All
commands ran with a run-local `HOME` and `TMPDIR` and Python bytecode disabled.
For portability, the retained [runner](run.py) replaces the executed host-specific
CodeQL path with the `CODEQL` environment variable (or `codeql` on `PATH`). The raw database, logs, BQRS and checkouts are
under ignored `work/`, not portable evidence or execution attestation.

The pinned producer and consumer were cloned no-hardlinks from freshly fetched
disposable snapshots; LuCI was fetched directly at the pinned SHA using `git
init`, `git remote add`, `git fetch --depth=1 origin <SHA>`, then detached
checkout. That timed setup group exited 0 in 10.86 s real, 0.89 s user, 0.78 s
system, maximum RSS 63,111,168 bytes. Both project trees and the LuCI tree
were clean at selection. The copied extractor pack was built from the same
producer revision in [the preceding typed run](../008-20261121/README.md); its
binary SHA-256 is `c7bde2d31303127f6bf8ebbbb364a5a47840867b67962a013032a3b6bbe7f8d2`.
The pack and run-local CodeQL package cache were copied to new run-owned paths
in 0.04 s real, 0.00 s user, 0.03 s system, maximum RSS 2,588,672 bytes. The
producer clone gained only the locally authored `ql/src/MarkupCalls.ql` query
as an untracked file. No new producer build was performed for this run.

An initial `codeql pack install` in the new workspace was interrupted with
exit 130 after it stalled; no result is claimed from that attempt. A fresh
database run using the previously installed, copied package cache completed and
matched the oracle; it used the CLI's default temporary directory. The retained
final run repeated the database in a new path with `TMPDIR` under the run root.
The local cached dependencies and committed pack locks were used; no install
success is claimed. Both completed runs had the same five rows. The successful
final runner command was `python3 -B evidence/020-markup-call/run.py
work/claim020/producer work/claim020` (exit 0). Each child command and timing
is retained in `commands.json`. No consumer adapter or runtime service was run.
