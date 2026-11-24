# PR #161 hosted Linux R2 candidate receipt

The [source-pinned Linux R2 job](https://github.com/lucas-albers-lz4/codeql-ucode/actions/runs/45488088083)
for draft [producer PR #161](https://github.com/lucas-albers-lz4/codeql-ucode/pull/161)
completed successfully on GitHub Actions Ubuntu 24.04. PR head was
`d39b1e19eb3c9cb63b493f44f2be2e95d89c17f4` against base
`9166af76cf6944e1b3ea5856a9176366a1f7a6ee`. The job ran GitHub's
synthetic merge checkout `996a270beea379dbb6409e99d03336642dbcc043`;
the receipt attributes results to that exact CI checkout, not to the PR
head alone.

The [portable summary](summary.json) preserves the source-first oracle,
tool/grammar identities, exact file and SARIF result identities, per-case
multiplicity, command exits/timing, candidate-bundle verification and
SHA-256 hashes of the downloaded raw artifact. The raw database is not in
the artifact. The run-scoped artifact was downloaded under ignored
`work/producer-grammar-pr161-r2-20261124`; its original run link is above.

All 116 recorded commands exited zero. The default suite resolved to the
direct-RPC check and two extraction diagnostics. It extracted the OpenVPN
parent once and found the exact alert at `luci.openvpn.uc:71:115–132`,
extracted the fixed version once with zero results, and extracted the
current swconfig near miss once with zero results. The 21 direct-RPC fixture
controls yielded exactly five predeclared locations. The separately named
Tailscale query extracted the parent and fix once each, finding its exact
candidate at `tailscale.uc:164:3–49` in the parent and zero in the fix;
11 controls yielded only the declared `nested_pos.uc:18:5–51` candidate.
All cases reported zero extraction errors.

The new plain/markup syntax fixture extracted both files once with zero
errors and returned all five predeclared projected typed AST locations.
The candidate Linux bundle verified successfully with base grammar SHA,
patch SHA-256, generated-files fingerprint and built-extractor SHA-256 in
its manifest. Its archive is a CI candidate, not a versioned immutable
release. The 116 phase wall times sum to 282.882 seconds; the maximum
reported per-command peak RSS was 587,087,872 bytes. This is not a
full-OpenWrt corpus performance estimate. Installed package bytes,
downstream handoff and maintainer-ready coverage remain open.
