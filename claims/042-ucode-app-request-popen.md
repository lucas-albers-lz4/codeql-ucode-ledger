# Claim 042: request.args to popen() in application ucode backends

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category B
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- CVE-2026-69096 class
- M4 luci-base getSwconfigFeatures/getRealtimeStats precedent

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned application ucode backends pass request-controlled values to `popen()` within the supported same-function slice, and with what quoting context?

## Method

Same method as 041 with popen sink; reuse M4 shellquote observation fields; manifested application file set.

## Required evidence

- Predeclared site multiset
- Query receipts
- Quoting-context classification per site

## Controls

- Positive: unquoted request value into popen template
- Near miss: shellquote complete-argument site
- Negative: literal popen command

## Out of scope

- Same limits as 041
- No global flow

## Notes

None.

## Result

Not yet evaluated.
