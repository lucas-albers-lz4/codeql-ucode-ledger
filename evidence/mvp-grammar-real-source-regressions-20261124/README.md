# Local grammar-prototype historical source regressions

The source-first oracle pinned four LuCI revisions before CodeQL ran:
OpenVPN parent `b45584b4e6068b9b096872dd02494a048d869c36`, fix
`e4ff45ecbc6ad212951815c8c99b2749fbd7de6b`, Tailscale parent
`46cd82328dfb7fbb15961c63f9e674a41cef2500`, and fix
`507ab5e45c304543d4111af9a331db0f03be6bcb`. Each was fetched to an
isolated Git worktree, checked at its full SHA and clean state, then hashed
and staged at its proposed installed path. The Tailscale controls came from
the producer's pinned `ql/test/tailscale-nested-shell/expected.json` manifest.

`python3 -B work/mvp-grammar-historical-regression-prep/real_pairs.py` used
the same locally modified grammar prototype extractor pack as the
[128-file corpus run](../mvp-corpus-v0.6-prototype-local-run/README.md).
The [normalized receipt](receipt.json) contains each source Git blob and
SHA-256, oracle/preflight hashes, exact command arguments, exits and times,
route/diagnostic hashes and observed SARIF locations. `$RUN` and `$CODEQL`
replace absolute paths; raw logs, database and SARIF remain under ignored
`work/mvp-grammar-real-source-regressions-20261124-a`.

All 15 selected files routed as plain RPCD sources and extracted exactly
once with zero errors. The default suite found the expected direct-RPC alert
at `luci.openvpn.uc:71:115–132` in the historical parent, and zero in the
fix. The separately named Tailscale query found the expected candidate at
`tailscale.uc:164:3–49` in the parent and zero in the fix. Its 11 controls
produced exactly the predeclared single positive at
`nested_pos.uc:18:5–51`; eligible near misses had no result. The receipt
checks URI, line and column multiplicity rather than counts alone. All 40
CodeQL phases exited zero, taking 38.740 seconds in total. Peak RSS was
unavailable on this local macOS run. The CLI reported only its query-stage
caching warning at the configured memory cap.

The first fetch command failed before analysis because the Tailscale fix SHA
was mistyped; the corrected full SHA fetched successfully. No failed source
revision was used. This is a local modified-grammar regression, not the
merged producer, Linux release gate, actual installed bytes, or a security
claim beyond the stated candidate results.
