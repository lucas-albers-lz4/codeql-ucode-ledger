# R2 Linux candidate gate, 2026-11-24

This is a compact index to the raw artifact from [codeql-ucode Actions run
45435176723](https://github.com/lucas-albers-lz4/codeql-ucode/actions/runs/45435176723)
(attempt 1). The run passed on PR #157 head
`c79a37a08e05567249b3a928b14527133ddbfd4e`; Actions checked out the
synthetic merge commit `f5afea857b1a469ac94c0fa58d446e2320dbab54`.
The downloaded raw artifact is retained locally under ignored
`work/r2-ci-run-45435176723/`; that path is not portable. Use the linked
Actions artifact and the hashes below to obtain and identify the raw bytes.

| Raw member | SHA-256 |
| --- | --- |
| `receipt.json` | `c9dc6a2a22d4a8173fb41bc75d3c4620d574e5040fe0f7874eb6e3ecc341341c` |
| `preflight.json` | `2b29a6e77599f8a43cdfff78475c945010026d9414e9fdae671935e79eac6b16` |
| `commands.json` | `3dc891f1de23b5f7a8fa210b04001fa3e8cb7fb5f07dbe9bd7d16a3f8218a16a` |
| `source-oracle.json` | `e45264baa0988085ed5761fbb23f0e0107fe045e230cb884a9689c58697b584c` |
| `out/openvpn-parent/default-suite.sarif` | `7dcc42f19d8413205d67e70cbf18945fa5b6b1a5a289f0fe5d3c9a3482e98cbb` |
| `out/openvpn-fixed/default-suite.sarif` | `80457c1bae834ffbda580dc6b543528f276fdb0116a27f69c4cb8593e46481e8` |
| `artifact/codeql-ucode-linux.tar.gz` | `65c0367440daff9ba965af7cbf9b0643afd0cf7908fd81fe47b1f6c5b46b3691` |

The receipt records CodeQL 2.27.4 and 104 commands, all exit 0 with wall
time and peak RSS. The default suite resolved to `DirectRpcShellWord.ql` and
the two extraction diagnostics. Each of the OpenVPN parent, fixed, and LuCI
swconfig stages selected and extracted its one expected file exactly once,
with zero extraction errors. The parent SARIF has one
`ucode/m4/direct-rpc-shell-word` result at
`usr/share/rpcd/ucode/luci.openvpn.uc:71:115-132` (UTF-16, exclusive end);
the fixed and swconfig SARIF have zero results. The 21-file direct control
matrix has five exact results. A separate, explicit Tailscale query found
one parent candidate and zero fixed candidates. The downloaded bundle's
outer SHA matched the receipt, and the producer verifier accepted its 290
manifested files.

These observations concern source bytes copied to proposed installed paths;
they do not establish actual package-installed bytes, runtime exploitability,
or a fresh downstream handoff. The archive manifest says
`artifact_kind: ci-candidate`, so it is not the immutable R2 release. A later
review tightened the Tailscale SARIF identity check; this run predates that
change and must not be used as a pass for a newer PR head.
