# Selected LuCI template extraction receipt

The [source-first inventory](source-first-manifest.json) records the pinned
source and inventory identities. The [pre-query manifest](prequery-manifest.json)
and translated [runner manifest](runner-manifest.json) were prepared before
querying; the 11 real-template diagnostic outcomes were deliberately left
unknown. [Source collection](source-collection.md) records clone commands,
source-tree checks and the interrupted full clone. The source blobs, staged
paths and install-transform boundaries are separate from a live installation.

`routing.json`, `extracted.json`, `errors.json`, `all-diagnostics.json` and
`verification.json` are reviewed copies of the actual run outputs with local
absolute paths replaced by consistent `@...@` placeholders; their row and
identity multiplicities are preserved. The first three JSON outputs were
produced by the extractor or upstream diagnostics; `all-diagnostics.json` is
from the explicitly [ledger-authored query](Wave1AllDiagnostics.ql).
`archive-check.json` was generated independently after the run by comparing
`src.zip` path identities and SHA-256 values with the pre-query runner
manifest. These copies and hashes do not authenticate execution. Raw BQRS,
source archive, logs, databases and disposable checkouts remain under ignored
`work/`, not as portable artifacts.

The [commands](commands.json) are copied from the runner's recorded argv,
working directory, exit statuses and monotonic wall timings with local paths
normalized. Each command ran under macOS `/usr/bin/time -l`; the separately
parsed [timings](timings.json) report real/user/system seconds and per-process
maximum RSS. The runner was executed by Luna on the exact configured route;
the parent independently compared the source hashes, routes, success
identities, empty diagnostic outputs and archive hashes. Its main command was:

```sh
python3 -B evidence/021-template-extraction/run.py <PRODUCER> <NEW_RUN_UNDER_WORK> <RUNNER_MANIFEST> <CODEQL_EXECUTABLE> --cache-source <PACKAGES_DIR>
```

The actual run used a run-owned `HOME`, `TMPDIR`, cache and database, with
`CODEQL_UCODE_STAGED_ROOT` set only during indexing. The runner copies the
manifest-listed staged bytes into its fresh source root and puts a labeled
local diagnostic query in the disposable producer. Its retained copy is the
executed script with no host-specific path substitutions in its body. Do not
run the adapter on an active checkout. The script's own `all_checks_match`
summary is useful but does not replace inspecting the underlying outputs.

The extractor pack was copied from the same-revision-input build recorded in
[claim 008](../../claims/008-setblock-typed-handoff.md#refresh-2026-11-21).
[Pack provenance](pack-and-lock-provenance.json) compares source and
run-owned pack file digests; the executable SHA-256 is
`c7bde2d31303127f6bf8ebbbb364a5a47840867b67962a013032a3b6bbe7f8d2`.
The selected revision differs from the build revision, but a tracked Git diff
of relevant extractor/library, lock, generator and pack inputs was empty.
Pack copying was measured at 0.01 s real, 0.00 s user, 0.00 s system, maximum
RSS 2,621,440 bytes. Total setup and package-cache-copy elapsed time was not
captured; the source-collection receipt separately records known setup times.
No producer or consumer implementation was changed.
