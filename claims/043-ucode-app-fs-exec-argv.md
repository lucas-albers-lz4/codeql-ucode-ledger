# Claim 043: request.args to fs.exec / fs.exec_direct argv

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category B
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
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

Not yet evaluated.
