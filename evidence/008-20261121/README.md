# Typed handoff receipt

These small reviewed copies derive from the local run recorded in claim 008.
The `main-*` and `controls-*` CSV and routing files are decoded raw output with
only the absolute source-root prefix replaced by `<MAIN_SOURCE>` or
`<CONTROLS_SOURCE>`. The row tables and `typed.json` are otherwise byte-for-byte
copies. `expectations.json` was written from the source and query before either
database was created. `consumer-targets.json` selects the one target row from
each resulting effect artifact; it is not a complete copy of those artifacts.
`consumer-summary.json` records hashes of the four checked artifacts and the
asserted rejection outcomes. The error excerpts retain the final diagnostic,
not the full traceback. The numeric test log is the separate offline suite.

The command receipts are derived from raw runner logs: `<RUN_ROOT>` replaces
the local work directory and `<CODEQL>` the executable. Each entry preserves
arguments, working directory, actual exit status, Python-measured wall time and
`/usr/bin/time -l` real/user/system time and maximum RSS. The source root for
main indexing was also set as `CODEQL_UCODE_STAGED_ROOT`; controls were indexed
without it. Both runners set a run-local `HOME` and disable Python bytecode;
`/usr/bin/time -l` wraps each recorded command. Raw stdout/stderr, BQRS,
databases and disposable checkouts remain under ignored `work/`; these
reviewed copies do not authenticate the execution. For portability, the retained producer runner replaces the executed host-specific
CodeQL path with the `CODEQL` environment variable (or `codeql` on `PATH`);
the recorded commands show the normalized executable as `<CODEQL>`.

The initial isolated build attempt was interrupted (exit 130) while Cargo was
updating its git dependency. The successful retry used isolated copied Cargo
registry/git caches with `CARGO_NET_OFFLINE=true` and the project's own build
script. The grammar bootstrap intentionally modified its local grammar
`Cargo.toml` dev dependency, as documented by that script. No tracked producer
or consumer files were dirty at selection or after the run; the ignored grammar
clone was dirty for this declared modification.

Setup command record (all paths are relative to the ledger root unless stated;
`<HOME_ORIGINAL>` is the user's pre-run home and `<CODEQL_DIR>` is the supplied
CLI directory):

1. `git fetch origin` in each disposable triage clone, exit 0. Local no-hardlink
   clones and detached checkouts at the two full SHAs in claim 008 were run as
   one `/usr/bin/time -l sh -c` group, exit 0, 0.21 s real, 0.05 s user,
   0.13 s system, maximum RSS 26,099,712 bytes.
2. From `<RUN_ROOT>/producer`, an isolated cache copy used `cp -R
   <HOME_ORIGINAL>/.codeql/packages <RUN_ROOT>/producer/work/typed-20261121/home/.codeql/`
   and `cp -R <HOME_ORIGINAL>/.cargo/registry <HOME_ORIGINAL>/.cargo/git
   <RUN_ROOT>/producer/work/typed-20261121/cargo/`; the timed group exited 0,
   15.30 s real, 0.45 s user, 12.18 s system, maximum RSS 14,172,160 bytes.
   The copied directories were subsequently moved to `<RUN_ROOT>/home` and
   `<RUN_ROOT>/cargo` before the successful retry. No credentials were copied.
3. From the producer, `/usr/bin/time -l ./scripts/clone-grammar.sh` exited 0,
   1.22 s real, 0.10 s user, 0.07 s system, maximum RSS 12,140,544 bytes.
   The first build using an initially empty run-local Cargo home was
   interrupted with exit 130 during dependency fetching; no complete timing
   was retained for that attempt.
4. From the producer, `/usr/bin/time -l env PATH=<CODEQL_DIR>:$PATH
   HOME=<RUN_ROOT>/home CARGO_HOME=<RUN_ROOT>/cargo CARGO_NET_OFFLINE=true
   bash scripts/create-extractor-pack.sh` exited 0, 15.39 s real, 90.61 s user,
   9.29 s system, maximum RSS 387,006,464 bytes. Pack installation is recorded
   separately in `producer-commands.json`.
5. From the ledger root, `python3 -B evidence/008-20261121/run-producer.py
   <RUN_ROOT>/producer <RUN_ROOT>/consumer <RUN_ROOT>/run` and then
   `python3 -B evidence/008-20261121/run-consumer.py <RUN_ROOT>/consumer
   <RUN_ROOT>/run/typed.json <RUN_ROOT>/run/main/src
   <RUN_ROOT>/run/main/effects.csv <RUN_ROOT>/consumer-run` each exited 0.
6. From the consumer, `/usr/bin/time -l env HOME=<RUN_ROOT>/home
   TMPDIR=<RUN_ROOT>/tmp PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest -v
   policy.tests.test_interchange_numeric` exited 0; timings are in its log.

`/usr/bin/time -l` is the macOS system timing tool. Its maximum RSS is reported
for each measured process; it should not be interpreted as a combined peak
across every child in the run. Python monotonic elapsed values include wrapper
startup and can differ slightly from the tool's real time.
