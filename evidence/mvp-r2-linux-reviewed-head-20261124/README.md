# R2 Linux gate on reviewed PR head, 2026-11-24

[CodeQL ucode Actions run 45438052249](https://github.com/lucas-albers-lz4/codeql-ucode/actions/runs/45438052249)
(attempt 1) passed on PR #157 head `7c62553b7a81b236b75d1b1fa0d50c612a020cc`.
The runner checked out GitHub's synthetic merge commit
`99b536b4108c0203909ebb4da2dad3db95c8f796`, clean before its build.
The raw artifact is retained locally at ignored
`work/r2-ci-run-45438052249/`; this local path is not portable. The linked
Actions run and these hashes identify the raw bytes.

| Raw artifact member | SHA-256 |
| --- | --- |
| `receipt.json` | `c16a1bd6920a1d3115fb762cd3910de7af84e2b0fc31f46bcbfaac46133c85bf` |
| `preflight.json` | `2c1847241efe4582193b088b01029e73547263608fd4ba4eb7a750f832b2ff9a` |
| `commands.json` | `e3f4c69b6305447b4e7754fb4e543f0527b136194b23d6434825cbd5cc74628f` |
| `source-oracle.json` | `e45264baa0988085ed5761fbb23f0e0107fe045e230cb884a9689c58697b584c` |
| `out/openvpn-parent/default-suite.sarif` | `0546193f1886e881fadf02fa2f6eb7cb004294fd6671886d830535ebc5c93074` |
| `out/openvpn-fixed/default-suite.sarif` | `7c5366043e225e6bff1ea0d2a490382b64f79457037c5bccc0dbb54e3a327273` |
| `out/direct-controls/default-suite.sarif` | `4489fa76200d1f3505885ee54bd8cfdb6a72f7acba2d1ff337f6de808a64fd6d` |
| `out/tailscale-parent/candidate.sarif` | `f0f72ee4fc2de2671caf6efe3c55ca41e151b857fa79276a44681f8e6027577d` |
| `out/tailscale-fixed/candidate.sarif` | `6a299c5eeeeabdc8285c7e37ff2d78633d573dd4cffa6c34b06bdcbd3984c0fc` |
| `artifact/codeql-ucode-linux.tar.gz` | `2669ae66d14e0a522ac1387bd8fdaed2e467896f267b2342a95b83b0e70bf11d` |

The downloaded receipt has 104 recorded commands, all exit 0, with wall time
and peak RSS. CodeQL reports version 2.27.4. The resolved default suite has
`DirectRpcShellWord.ql` and the two extraction diagnostics. The OpenVPN
parent, fixed and LuCI swconfig cases each extracted their selected file
exactly once with zero errors. Parent SARIF has one
`ucode/m4/direct-rpc-shell-word` result at
`usr/share/rpcd/ucode/luci.openvpn.uc:71:115-132` (UTF-16, exclusive end);
fixed and swconfig have zero. The 21-file direct control matrix has five
results at its exact expected locations. The separate Tailscale testing
query has one parent result and zero fixed results, with its rule ID,
location multiplicity and full single-line region checked. The downloaded
archive hash matches the receipt; the producer verifier accepted its 290
manifested files.

These are source-staged observations, not package-installed-byte or runtime
proof. The bundle is marked `artifact_kind: ci-candidate`. An immutable
versioned release and fresh consumer run are still required for R2/R3.
