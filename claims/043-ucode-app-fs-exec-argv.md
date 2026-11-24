# Claim 043: request.args to fs.exec / fs.exec_direct argv

- Status: Blocked
- Program: [Security-40](../planning/security-40-20261124.md), category B
- Producer: `lucas-albers-lz4/codeql-ucode` — routing probe P2 at HEAD below; application backends not routed
- Producer commit: `734555a9f56893e89e678cdee63028fc17ea5bc8` (clean; probe-ucode/producer); luci slice pin `b2e0be4b46ec0fd43394c081fa7c50657af14011`
- Consumer: none (no consumer join reached)
- Consumer commit: none
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-vx64-mmp7-h36c (samba4 smbd file.exec)
- consumer M2 ubus file.exec models

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned ucode backends construct `fs.exec`/`fs.exec_direct` argv from request values, and does the executable position stay fixed while argument positions vary?

## Method

Bounded same-function slice over ucode fs.exec call sites in the manifested application set; classify executable-position vs argument-position request control; JS-side callers remain syntax inventory only (hold).

## Required evidence

- Call-site multiset with position classification
- Source oracle fixed before run

## Controls

- Positive: request value in argv argument position, fixed executable
- Near miss: request value in executable position (distinct risk class, recorded separately)
- Negative: fully literal argv

## Out of scope

- No execv modeling
- No live PATH search
- No ACL verdict

## Notes

None.

## Result

Blocked 2026-11-24 — same producer routing gate as claim 041 (codeql-ucode
HEAD `734555a9f56893e89e678cdee63028fc17ea5bc8`, clean; probe P2 receipts in
`work/security-40/probe-ucode/VERDICT.md`): 7/7 application .uc backends
skipped; extractor `file_globs` literal basenames only (extractor.rs
~l.45–64) and RequestArgsExec.ql l.18 `getBaseName() = "luci"` — both
orchestrator-verified.

Additional model gap (orchestrator-verified in RequestArgsExec.ql): the
supported sink set is `NamedFsPopenCall` / `BuiltinSystemCall` only —
`fs.exec` / `fs.exec_direct` are outside the M4 request-args sink model even
for routed files. Routing is the primary blocker; the executable-position vs
argument-position request-control classification was not performed. JS-side
callers remain syntax inventory only (hold unchanged).

Unblock condition: claim 041's routing unblock PLUS an fs.exec sink model
decision in the producer (new bounded decision, not implied by this program).
Evidence paths: see claim 041 Result. Security-40 lifts no gate.
