# Failed attempts retained

These failures are not passes and did not replace the final outputs.

1. Exploratory run under `work/uci-formal-reassignment-run/` used producer checkout HEAD `8375887ed14825dd59addbfd0df43616d9e684fb` with the observer copied from a later producer commit. Init/index/finalize succeeded. A diagnostic query copied outside its QL pack failed compilation because `codeql.files.FileSystem` and `codeql.ucode.Diagnostics` were unresolved; the first decoder wrapper also requested nonexistent `query-*.bqrs` paths after overwriting its loop variable. Final successful query/decode logs in that directory were exploratory only, not exact current-checkout evidence.

2. `work/uci-formal-reassignment-clean-run/` preserved a failed attempt where `--common-caches` was placed before the CodeQL subcommand. CodeQL returned usage errors before database initialization. Its shell wrapper also failed to stop after command errors; none of those statuses are evidence of extraction or query results.

3. On the clean detached `1ccf5268e6915dc8d4cbb926b28be8ff79bcb0ed` retry, init/index/finalize succeeded and the pre-finalize routing receipt was retained. The first diagnostics query failed because locked `codeql/controlflow@1.0.12` was absent from that run's empty pack cache. The exact locked dependency packages were copied into the run-owned cache and passed through `--additional-packs`; all five diagnostics/observer queries and decodes then exited 0.

4. The first entity-count helper query had an incompatible AST-node type and exited 2. After correction, it exited 0 and yielded the count below. Its failure remains at the raw work log path listed in `README.md`.
