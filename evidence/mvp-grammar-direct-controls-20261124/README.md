# Local grammar-prototype direct-RPC control matrix

The source-first fixture manifest in producer
`ql/test/direct-rpc-shell-word/expected.json` has SHA-256
`5ec2d74cb21732189a41558ec59671126310679c6725f802614ac3fa9c19caf0`.
It fixed the 21 selected file hashes and five exact expected alert locations
before this run. The producer source checkout was at
`9166af76cf6944e1b3ea5856a9176366a1f7a6ee`; the extractor pack was
the same locally modified grammar prototype used by the
[128-file v0.6 probe](../mvp-corpus-v0.6-prototype-local-run/README.md).

The command `python3 -B work/mvp-grammar-historical-regression-prep/direct_controls.py`
created a fresh database, stage, cache, `HOME` and `TMPDIR` under ignored
`work/mvp-grammar-direct-controls-20261124-a`. The
[normalized receipt](receipt.json) records preflight hashes, exact commands,
exits, phase times, routing hash, diagnostic CSV hashes and SARIF hash;
`$RUN` and `$CODEQL` replace the absolute run and executable paths. Raw
outputs and database remain under `work/`.

All 21 selected files routed as plain RPCD sources and extracted exactly
once; there were zero extraction errors. The default-suite SARIF had exactly
five direct-RPC results at the five predeclared file/line/column spans, with
no extra results. Nine CodeQL phases exited zero and took 9.698 seconds in
total. Peak RSS was unavailable in this local macOS environment.

This is the fixture control matrix, not the historical OpenVPN parent/fix or
Tailscale parent/fix real-source matrices. It does not establish Linux release
regressions, installed package bytes or current OpenWrt alert performance.
