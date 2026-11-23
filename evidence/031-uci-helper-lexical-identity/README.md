# Claim 031 evidence: UCI helper lexical identity

This record covers one pinned LuCI controller, a reassigned-formal positive, and a copied-alias near miss against the producer's unchanged test-only observer. The source-first oracle is in [ORACLE.md](ORACLE.md); selected normalized query outputs are in [outputs](outputs/); query sources and hashes are in [queries](queries/) and [provenance.json](provenance.json). Raw database, BQRS, command logs and timing files remain under ignored `work/uci-formal-reassignment-clean-run-retry-01/`; `outputs/normalization.json` maps normalized files to their raw SHA-256 digests and locations. The normalization replaces only the exact run-root string with `$RUN`; it preserves row count and multiplicity.

## Exact result

The actual extractor `routing.json`, captured before database finalization, records three inputs, all selected as plain with reason `ucode_extension`; markup, markup-inconclusive, uncertain, excluded and duplicate counts are zero. The selected identities are `controls-formal/alias-instead-of-formal.uc`, `controls-formal/reassigned-formals.uc`, and `usr/share/ucode/luci/controller/admin/uci.uc`.

`SuccessfullyExtractedFiles` returns exactly those three identities once each. `ExtractionErrors` returns zero rows. `AllDiagnostics.ql` returns zero **file-located `Diagnostic` entities**; it filters for diagnostics with a source file and does not enumerate global CLI diagnostics.

The unmodified upstream `UciHelperObservation.ql` returns exactly two projected rows: the reassigned-formal fixture (`caller 5:1–5:30`, helper `1:3`, forwarding call `3:10–3:40`) and pinned controller (`caller 79:9–79:81`, helper `25:28`, forwarding call `28:12–28:42`). The alias fixture has no observer row.

A separate eligibility diagnostic returns one alias candidate with direct call shape, its argument-1 identifier, and its local variable declaration. Additional aggregate queries count distinct matching AST entities per site: each observer-positive site has one forwarding-call entity and one associated helper entity; the alias near miss has one candidate call, one argument-1 identifier, and one variable target. These entity counts strengthen the projected-row check for the stated sites; they do not establish runtime value flow.

The source-only oracle predicted the alias identifier span as `3:28–3:43` using an end-exclusive byte position. Direct UTF-8 byte counting shows `forwardedMethod` occupies 15 bytes at columns 28–42 inclusive. The decoded CodeQL identifier entity is `3:28–3:42`; the initial end-column prediction was off by one and is retained in the oracle rather than rewritten. The full forwarding call span was correctly predicted as `3:10–3:49`.

## Pins and run

Producer checkout was detached at `1ccf5268e6915dc8d4cbb926b28be8ff79bcb0ed`, with tracked files clean and four auxiliary query files untracked. The relevant observer was introduced at `cc87f6d7a104bd54bcb8a1ec97e9eb23afc6ba63`; the current pin contains it unchanged. LuCI source is revision `b2e0be4b46ec0fd43394c081fa7c50657af14011`; staged bytes match blob `c38a42b10bfefbaa31741feae9395abd8a1f8e40` and SHA-256 `ac75cfef7d74f87ed7f957778004a7bf486c76df699398c215795b4947e0c93e`.

CodeQL CLI 2.27.4 and `/usr/bin/time -l` were used. The run used a fresh database and run-owned source root, `TMPDIR`, XDG directories, common cache, and compilation cache. `HOME` was inherited and not overridden. The existing extractor pack was copied from the build at producer `8375887ed14825dd59addbfd0df43616d9e684fb`; exact pack digests are in provenance. There are no extractor/grammar changes between that build pin and the selected producer revision. The query package lock SHA-256 is recorded in provenance. The eight exact lock versions were copied from a prior run's ready package cache into this run's private `common-caches/packages` and exposed via `--additional-packs`; manifest digests are included.

The initialized/extracted/finalized run phases exited 0 (0.49/0.65/1.17 sec; peak RSS 122,372,096/121,372,672/226,115,584 bytes). Final queries and decodes exited 0. Query wall time / peak RSS: successful files 1.76 sec / 330,661,888 bytes; extraction errors 1.72 sec / 291,241,984; file-located diagnostics 1.73 sec / 334,659,584; observer 3.78 sec / 533,282,816; alias eligibility 3.20 sec / 491,978,752; entity counts 2.80 and 2.78 sec / 435,355,648 and 428,933,120 bytes. These are focused run timings, not corpus estimates.

## Failures and ownership

[Failed attempts](failures/attempts.md) records all failed setup, query, decode, and count-query attempts, along with the raw work paths that preserve their complete logs. The final query pass used the same finalized database after the missing dependency was supplied; the earlier errors are not treated as passes.

Ucode issue [#53](https://github.com/lucas-albers-lz4/codeql-ucode/issues/53) owns this upstream UCI inventory/helper work. Its direct cursor-write gate remains unmet. This claim demonstrates the observer's lexical variable identity behavior for these exact inputs; it does not establish that the caller's `'commit'` value survives reassignment, that any call executes, or runtime ubus resolution, authorization, persistence, configuration effects, or security impact.
