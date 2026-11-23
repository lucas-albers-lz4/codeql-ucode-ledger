# Claim 032 evidence bundle

This bundle preserves the original five-fixture planning oracle, a separately reviewed six-fixture source-first supplement, all exact input bytes, the query sources, decoded CodeQL outputs, and a comparison report. The original oracle is unchanged; the supplement adds an ordinary-delimiter member-expression control so expression-shape exclusion is independently observed.

All 11 assertions in `outputs/oracle-comparison.json` pass. The current implementation prediction has a graph only for `plain.ut`: six nodes and five edges. The other five fixtures have no graph rows. The ordinary member control is a valid eligible near miss for the identifier-child guard. No trim policy conclusion is made.

`outputs/AllDiagnostics.csv` and `outputs/ExtractionErrors.csv` are scoped to the six fixture files and contain only headers. The database also recorded three unlocated CLI telemetry events in `outputs/cli-diagnostics.jsonl`; they are not file-located diagnostics. `outputs/SuccessfulFiles.csv` is the scoped basename-filtered query, not a producer-wide file inventory.

The AST output contains 48 rows. All 46 predeclared root, text, tag, delimiter, expression, and member-field identities match once. Two additional `ReservedWord` dot entities belong to member-expression punctuation, which the oracle explicitly leaves unenumerated.

`outputs/portable-receipt.json` records revisions, tool and pack provenance, isolation, routing, outputs, timings, peak RSS and known capture gaps. Setup-failure and retry summaries and selected logs are retained under `outputs/timing-status/`; other raw stderr logs remain under `work/`. It records inherited `HOME` (not set or changed) and distinguishes empty file-located diagnostic queries from the three CLI telemetry events. Some manual retries lack structured argv capture, and the final member-field BQRS decode was not timed; the evidence does not claim complete command/timing coverage.

Decoded CSVs are the portable query rows. Raw BQRS binaries and the database remain under ignored `work/trim-matrix-run-20261122-a/`; sizes and SHA-256 values for the nine final BQRS files are in `outputs/artifact-manifest.json`. No database or BQRS binary is included here. Paths in portable command logs use `<RUN>` and `<CODEQL>` placeholders; raw local logs remain under `work/`.
