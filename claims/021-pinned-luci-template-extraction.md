# Claim 021: extraction of selected pinned LuCI templates

**Status:** Demonstrated for the explicitly enumerated staged source and controls.

**Decision and scope:** At the recorded revisions, can the current ucode
extractor select and successfully extract the 11 `.ut` source blobs named by
the pinned `luci-ssl-25.12` inventory, when their upstream bytes are staged at
expected installed paths? This is an extraction and diagnostics observation;
it does not establish semantic or runtime coverage.

## Revisions and source selection

The clean disposable producer was
`0a6612fe0e66351a0ccda43ad5b51f5ef5a2724e`; the clean consumer inventory was
`d37adeadaf836ba97049f75087a348165027f7f9`. The LuCI source was a separate
clean checkout at lock pin `b2e0be4b46ec0fd43394c081fa7c50657af14011`. The
consumer lock SHA-256 was
`b4cbdabb76df90a807aba7d42ae675198c7b7b09c3b84db259a3a4c941b0ea9a`.
The [source-first inventory](../evidence/021-template-extraction/source-first-manifest.json)
compares the 11 consumer-transcribed entries with a separate Git-tree scan of
the profile package closure, recording blob IDs, modes, paths and hashes.
Their expected installed paths were derived from the pinned `luci.mk`; no
collisions were found. Seven are from `luci-base`, one from `luci-mod-status`
and three from the bootstrap theme. The inventory also records two extensionless
bootstrap symlinks, which were excluded, and the already-investigated
`uhttpd.uc`, which is outside this `.ut` selection.

These are **upstream source bytes staged at expected paths**. `luci.mk` runs
`SubstituteVersion` during installation; two headers contain matching tokens
and the profile seed does not supply a resolved package version. No configured
install was performed, so installed-byte equivalence is not asserted. The
producer's known valid `mixed.ut` fixture, a plain `.uc` fixture, and the
pinned shebang CGI source were separate controls, not counted among the 11.

## Run and results

The [pre-query manifest](../evidence/021-template-extraction/prequery-manifest.json)
fixes 14 unique paths, hashes and route expectations before output inspection;
real-template parse outcomes were not assumed. A fresh database was built with
CodeQL 2.27.4 and Python 3.15.2, using a copied extractor pack built at
`8375887ed14825dd59addbfd0df43616d9e684fb`. The extractor, library, pack and
lock inputs did not differ at the selected producer revision; the binary digest
and previous build provenance are in the [receipt](../evidence/021-template-extraction/README.md).
It used run-owned source, database, `HOME`, temporary directory and caches.

The [routing receipt](../evidence/021-template-extraction/routing.json)
contains exactly 14 input decisions: 12 markup and two plain, with zero
excluded, uncertain or duplicate inputs. All 12 markup routes retain the
**inconclusive** `markup_not_modeled` status. Each path and route matched the
pre-query oracle. The producer's
[successful-file diagnostics](../evidence/021-template-extraction/extracted.json)
identify all 14 files exactly once. That upstream diagnostic selects file
identities with a relative path and no `parse_error`; it is not a separate
per-file execution attestation. Its
[extraction-error output](../evidence/021-template-extraction/errors.json) has
zero rows. A separate labeled ledger query for all `Diagnostic` tags returned
[zero rows](../evidence/021-template-extraction/all-diagnostics.json). Both
plain controls and the valid markup control extracted cleanly. The
[source-archive check](../evidence/021-template-extraction/archive-check.json)
independently compared the 14 archived paths and byte hashes with the pre-query
manifest; it is not execution attestation.

All recorded database and query commands exited 0. Indexing took 0.66 seconds
wall and 120,930,304 bytes maximum RSS; finalization took 1.22 seconds; the
three diagnostic queries took 1.74, 2.07 and 2.28 seconds, respectively.
[Command receipts](../evidence/021-template-extraction/commands.json) and
[timings](../evidence/021-template-extraction/timings.json) preserve individual
timing and per-process memory. Setup and an interrupted full LuCI
clone are documented in the receipt; total setup/cache-copy wall time was not
fully measured. No full-corpus runtime may be inferred.

These results are limited to the selected source bytes, parser, routing and
reported diagnostics. They do not establish correct AST identities for every
construct, runtime rendering, CFG, flow, security, completeness or consumer
integration; the consumer's inconclusive status is unchanged. OpenWrt
[#68](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/68) owns
integration and ucode [#57](https://github.com/lucas-albers-lz4/codeql-ucode/issues/57)
continues to own deferred markup CFG/dataflow. No consumer was invoked.
