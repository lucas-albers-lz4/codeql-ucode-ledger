# Claim 065: Keep-alive body drain and parse-error desync

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category F
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-c2wg-hcff-hqrm (CL.0)
- GHSA-wgwp-64hh-f52p / CVE-2026-55613 (parse-error desync)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Where does pinned uhttpd decide connection reuse, and what body-drain / error-state handling precedes that decision in-source?

## Method

Source oracle / P1-gated CodeQL C: transcribe reuse decision sites and preceding consume/reset calls.

## Required evidence

- Decision-site multiset with drain observation
- Source lines

## Controls

- Positive: reuse path with no observed body drain (if present)
- Near miss: reuse after observed consume
- Negative: close-on-error path

## Out of scope

- No smuggling execution
- No timing/runtime claim

## Notes

None.

## Result

Not yet evaluated.
