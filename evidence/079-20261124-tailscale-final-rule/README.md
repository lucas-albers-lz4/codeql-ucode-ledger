# Claim 039 evidence

Run-d explicit-query receipt. `source-first.json` is the prior independently prepared parent/fix oracle; its parent/fix SHA256 identities were rechecked against the staged run bytes. The run preflight pins the producer, query and source manifest. Exact extracted paths, error/candidate/field tuple multiplicities and SARIF rule/result regions are normalized in `results.json` and `sarif-summary.json`. Command paths normalize to `$RUN`, `$PRODUCER`, and `$CODEQL`; raw hashes are in `receipt.json`.

The copied-database query in run-b is a separate timing observation: copied 42,527,916-byte database, same query hash, exit 0, 3.196 seconds query / 450,052,096-byte peak RSS, 0.230 seconds decode, zero rows. It is not a clean extraction rerun or performance estimate beyond this single bounded command.

The source manifest records its fixture preparation producer pin (`18afe...`); run-d separately pins the analyzed query producer (`2dde...`). These are distinct provenance facts.
