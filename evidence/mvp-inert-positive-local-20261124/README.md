# Inert selected-path positive feasibility probe

On 2026-11-24 an isolated local CodeQL 2.27.4 run tested whether the default
suite's direct-RPC shell-word rule could alert on a change to the currently
selected LuCI path
`applications/luci-app-example/root/usr/share/rpcd/ucode/example.uc`.
The clean LuCI source was pinned at
`b2e0be4b46ec0fd43394c081fa7c50657af14011`, Git blob
`d6e21fcfeb8ff49d0387a605313b2b6f11fed56f`. The test appended an
unreachable handler after an unconditional top-level return, within
`if (false)`. Its command expression interpolated a request argument; the
otherwise matching control applied `shellquote` to that argument. Neither
fixture was executed or deployed. Source bytes and expected source span were
recorded before the final run.

The producer was a **dirty experimental copy** based on
`9166af76cf6944e1b3ea5856a9176366a1f7a6ee`, with prior built-pack
provenance retained in ignored
`work/inert-positive-local-policy-20261124/`. It was not a versioned release.
The run used CodeQL 2.27.4 executable SHA-256
`bb3a754e126ed061b5f3356531cd5501872ab3864bd665b2d1afdbf8a67a146d`.
Each fixture had its own database, stage and output. The raw source-first
oracle, 18 command records, exact routing JSON, diagnostics and SARIF remain
under that ignored run root. [summary.json](summary.json) is a small path
normalized projection of those raw observations, not a replacement for the
raw files on this machine.

Both files routed as plain ucode by `rpcd_raw_mode_full_path`, extracted
exactly once and had zero extraction errors. The positive yielded one
`ucode/m4/direct-rpc-shell-word` SARIF tuple at
`usr/share/rpcd/ucode/example.uc` line 53, columns 26–44 (SARIF end
exclusive). The quoted control yielded zero. All 18 commands exited 0.
Summed command phases were 9.457 s and 9.044 s respectively; peak RSS was
unavailable. These are single-file smoke timings, not full-corpus estimates.

An earlier handwritten route expectation incorrectly said `ucode_shebang`.
The mismatch is retained in
`work/inert-positive-local-routed-20261124/summary.json`. The final run used
the pre-existing v0.6 source policy's `rpcd_raw_mode_full_path` expectation,
but that correction also followed observed output. Treat this as a feasibility
probe, not an independent held-out oracle. There is no upstream PR, incoming
event resolver, released Linux scan, actual consumer handoff or installed-byte
claim. A future Gate 8 drill must predeclare its exact event/control source,
rule, location and multiplicity, then run both through the released hosted
workflow.
