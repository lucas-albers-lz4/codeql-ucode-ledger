# Claim 060: Newline-bearing UCI values into line-based formats

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category C
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-w6q2-vr4f-49x3 (ser2net UCI newline → YAML gensio stdio, critical)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned package init/config scripts render UCI values into line-based or structured config files (ser2net YAML, cron, hosts, dnsmasq conf) without observed newline rejection?

## Method

Source oracle over manifested init scripts: trace uci get → file write chains; record format type and any observed sanitization; cross-check ser2net advisory shape at pinned packages SHA.

## Required evidence

- Chain multiset with format classification
- Sanitization observation per chain

## Controls

- Positive: multi-line-capable value written into line-based config
- Near miss: value passed through observed newline strip
- Negative: numeric-only option

## Out of scope

- No downstream daemon parsing claim
- No runtime injection demonstration

## Notes

None.

## Result

Not yet evaluated.
