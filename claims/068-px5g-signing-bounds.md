# Claim 068: px5g certificate-signing buffer bounds

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category H
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-jgc3-4q3p-g6xh (2040-bit cert signing heap overflow)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned luci-lib-px5g source, what buffer sizes govern key/signature handling during certificate signing, and is the 2040-bit overflow shape observable?

## Method

Source oracle / P1-gated CodeQL C on px5g at pinned luci SHA: transcribe allocation sizes vs key-size inputs in the signing path.

## Required evidence

- Size-input table with source lines
- Historical-shape presence statement

## Controls

- Positive: fixed buffer smaller than max key-derived write (if present)
- Near miss: size-derived allocation
- Negative: unrelated fixed buffer

## Out of scope

- No overflow execution
- No crypto correctness claim

## Notes

None.

## Result

Not yet evaluated.
