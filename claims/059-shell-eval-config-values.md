# Claim 059: Package shell eval/sh -c of config values

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category C
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-hfpc-hw28-69pj (ddns dynamic_dns_lucihelper.sh eval)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned package shell scripts pass UCI/config-derived values to `eval`, `sh -c`, or unquoted expansion in command position, and what is the value chain in-source?

## Method

Source oracle over pinned packages tree (shell is not CodeQL-extracted by either repo — method stated honestly); transcribe config_get → command chains for a manifested script set.

## Required evidence

- Chain multiset with script/line provenance
- Independent expected-case transcription

## Controls

- Positive: config_get value into eval (advisory shape)
- Near miss: value quoted and passed as single argv word
- Negative: literal-only eval

## Out of scope

- No shell runtime execution
- No claim of full packages-tree coverage

## Notes

None.

## Result

Not yet evaluated.
