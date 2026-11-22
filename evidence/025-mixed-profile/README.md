# Mixed LuCI profile extraction receipt

The [source-first oracle](source-first-oracle.json) records 21 pinned files,
three controls, exclusions, source hashes, and per-file routing and root
expectations. The [prequery source map](prequery-source-map.json) records the
stage identities. The stage preserves upstream LuCI bytes. The database
[source archive check](archive-check.json) verified the same 24 member paths
and hashes.

The [command receipt](commands.json) contains commands, exit statuses, elapsed
time and peak resident memory from `/usr/bin/time -l`. It records the initial
root-query [import failure](logs/mixed-profile-root-counts-query.stderr-time.txt)
and the [successful retry](logs/mixed-profile-root-counts-retry-query.stderr-time.txt)
using the same query bytes inside the disposable producer query pack. Run
scripts set temporary and extractor/cache directories inside the workspace
and explicitly supplied the run-local package search paths. They inherited
`HOME`, and the execution record does not establish a run-owned override.
The [pack provenance](provenance.json) compares the actual pack bytes with
the matching [earlier build receipt](../021-template-extraction/pack-and-lock-provenance.json).

The [decoded outputs](outputs/) retain exact routing, successful-file
identities, diagnostic rows, and mode-specific AST root counts. Entity counts
were calculated inside CodeQL before projection. The diagnostic gate and
canonical routing identify the staged files separately. The
[artifact index](artifact-index.json) records raw and retained hashes.
`<RUN>`, `<CODEQL>`, `<LEDGER>`, and `<HOST_HOME>` replace host paths.
The command receipt adds timing context to the raw command rows. The ZIP
archive, BQRS files, and CodeQL database remain local and outside Git.

The two templates and the plain tag-like string control establish the
expected root kind for their files. The query does not evaluate their
interior AST, template rendering, or control and data flow.
