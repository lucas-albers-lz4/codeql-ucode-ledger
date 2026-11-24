# Claim 040 evidence

Run-i is the fresh final-commit result: 24 source-first inputs (parent, fixed, swconfig, and 21 controls) each extracted once with zero extraction errors; the explicit direct-RPC rule emitted 1/0/0/5 rows, corroborated by SARIF result counts and exact regions. Source identities, AST witness tuples, rule rows, SARIF locations and all command timings/peak RSS are normalized in the receipts.

Probe-c is separate: it copied the Stage-6 21-file database, did not extract source again, and produced zero CSV/SARIF rows with the same final query hash. `nonpasses.json` records run-h's two control parse errors and current-slice-a's interrupted query (exit 130 at 183.36 seconds); neither contributes a positive or negative rule result. Raw paths normalize to `$RUN`, `$PRODUCER`, `$ORACLE`, and `$CODEQL`; unmodified raw artifact SHA256 values are in `raw-hashes.json`.
