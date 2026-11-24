# Claim 044: shellquote placement in application command templates

- Status: Blocked
- Program: [Security-40](../planning/security-40-20261124.md), category B
- Producer: `lucas-albers-lz4/codeql-ucode` — routing probe P2 at HEAD below; application backends not routed
- Producer commit: `734555a9f56893e89e678cdee63028fc17ea5bc8` (clean; probe-ucode/producer); luci slice pin `b2e0be4b46ec0fd43394c081fa7c50657af14011`
- Consumer: none (no consumer join reached)
- Consumer commit: none
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-pm9w-522m-8rrh (openvpn generateKey cl_meta command injection)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned application command templates reaching system/popen, where does `shellquote` appear — complete-argument position, executable position, or absent — under the M4 barrier definition?

## Method

Inventory shellquote call sites feeding command strings in the manifested application set; classify placement per the documented M4 barrier context; do not extend the barrier model.

## Required evidence

- Placement multiset with source lines
- M4 barrier definition cited by pack digest

## Controls

- Positive: absent-quote advisory shape
- Near miss: complete-argument quote (barrier context)
- Negative: quoted executable selection (still injection candidate per M4)

## Out of scope

- No global sanitizer claim
- No barrier promotion

## Notes

None.

## Result

Blocked 2026-11-24 — same producer routing gate as claim 041 (codeql-ucode
HEAD `734555a9f56893e89e678cdee63028fc17ea5bc8`, clean; probe P2 receipts in
`work/security-40/probe-ucode/VERDICT.md`): 7/7 application .uc backends
skipped; extractor `file_globs` literal basenames only (extractor.rs
~l.45–64) and RequestArgsExec.ql l.18 `getBaseName() = "luci"` — both
orchestrator-verified.

The M4 barrier model exists and is exercised on the routed luci-base rows
(`wrappedByShellquote` → "via shellquote" note on 6 of 7 P2 rows; setLocaltime
→ system ×1 with no shellquote), but application command templates are
unextracted, so the shellquote-placement inventory (complete-argument vs
executable position vs absent) over the manifested application set is not
possible at this HEAD. The barrier model was not extended (per method).

Unblock condition and evidence paths: see claim 041 Result. Security-40
lifts no gate.
