# Claim 041: request.args to system() in application ucode backends

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category B
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- CVE-2026-69096 / GHSA-wjfh-jfr9-fxvm (dockerman docker_rpc.uc run_ttyd builds shell command from id/cmd/uid)
- GHSA-cq4h-h8jr-3xqv

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Does the M4 same-function request.args→system slice observe request-controlled arguments reaching `system()` in pinned application ucode backends (first target: dockerman docker_rpc.uc), with the documented binding limits?

## Method

Probe P2 extraction routing first; then run the supported RequestArgsExec-style query over a manifested application-backend file set at the pinned luci SHA; compare exact finding identities to a source-derived oracle.

## Required evidence

- Extraction routing receipt (P2)
- Predeclared expected finding multiset from source
- Query identity, pack digests, command/exit/time/memory
- Positive and near-miss fixture results

## Controls

- Positive: request.args field concatenated into system() command (advisory shape, synthetic fixture)
- Near miss: same shape with shellquote in complete-argument position
- Negative: fixed literal system() command

## Out of scope

- No interprocedural flow
- No taint-sanitizer guarantee
- No runtime exploitability
- No claim beyond the same-function binding subset

## Notes

If the pinned source still contains the unquoted advisory shape, record it as a bounded source observation; disclosure is a separate user decision.

## Result

Not yet evaluated.
