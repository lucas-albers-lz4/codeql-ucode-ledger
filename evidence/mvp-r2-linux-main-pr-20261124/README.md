# R2 Linux candidate on replacement publication PR #159

Status: [hosted run `45453107382`](https://github.com/lucas-albers-lz4/codeql-ucode/actions/runs/45453107382)
passed on 2026-11-24 for PR head
`91e22839092c697843f40dd37ca795a036e49ebf`. The checked-out
synthetic merge commit inside CI was
`6560ba57116ba74af2d63206c0f220503b8b319b`. The downloaded artifact
was reviewed separately under ignored `work/r2-ci-run-45453107382`.
The [portable receipt](receipt.json) has SHA-256
`e6bc0a64e12d76d056b1db1232bc9409222156577a15a93973b052dcfa376a97`
and hashes 13 raw inputs/outputs. Those raw `work/` paths are local only.

All 104 recorded commands exited zero. The source oracle digest matched,
the bundle's outer SHA-256 was
`3e33fc59276c71f4c7c01023b3dfc1cfd8d008b3ca5b189468708a7597019b6e`,
and the producer verifier checked all 290 manifested payload files. The
manifest identifies a `ci-candidate` bound to the synthetic merge commit.
The resolved default suite contains `DirectRpcShellWord.ql` and the two
extraction diagnostics. OpenVPN parent produced one exact
`ucode/m4/direct-rpc-shell-word` result at
`usr/share/rpcd/ucode/luci.openvpn.uc` line 71, columns 115–132; fixed and
LuCI swconfig cases produced zero. The direct control matrix produced five
expected results. The separate Tailscale regression produced one parent,
zero fixed and one control candidate.

This is a passing Linux PR candidate after rebasing publication work onto
merged main. It is not an immutable versioned release or a current OpenWrt
corpus/installed-byte result. The PR's M3/M4 smoke remains a separate gate.
