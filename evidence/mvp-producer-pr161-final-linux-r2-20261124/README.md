# Producer PR #161 final-head Linux R2 candidate

The [hosted Linux R2 run](https://github.com/lucas-albers-lz4/codeql-ucode/actions/runs/45498511187)
passed at producer PR head `b25bdd34f2dfb701f52f996702fd1a8830be048d`.
Its Ubuntu runner used GitHub's clean synthetic merge checkout
`7aba3e7481d5419167c534b54663a050136bdb83`, as recorded in the raw
preflight and receipt. This is a distinct run from the earlier PR head
`d39b1e1` receipt; the earlier evidence must not be attributed to this head.

I downloaded artifact `direct-rpc-r2-45498511187-1` to new ignored
`work/producer-pr161-final-r2-20261124/`, inspected `preflight.json` and
`receipt.json`, and independently hashed the candidate archive. The
[portable summary](summary.json) records the raw receipt and preflight
digests, exact extraction multiplicity, SARIF rule/location tuples, 116
zero-exit commands, phase time sum and highest per-command peak RSS. The
default suite found one OpenVPN-parent alert and zero fixed and swconfig
near-miss results. The separately named Tailscale query found one parent
candidate and zero fixed candidates; its controls yielded one declared
positive. The syntax fixture extracted one plain and one markup file with
zero errors. The Linux bundle verified as `ci-candidate`, not a versioned
immutable release. The runner's source staging is not an installed-byte
observation or downstream consumer handoff.

The complete raw artifact is run-scoped and not committed. These small
summary claims depend on the linked hosted run and downloaded receipt;
another machine cannot read this ledger's ignored `work/` directory.
