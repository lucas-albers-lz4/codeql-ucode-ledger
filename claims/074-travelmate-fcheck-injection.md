# Claim 074: travelmate f_check script/script_args injection

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category G
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- travelmate 2.4.5-r3 f_check report (OpenCVE; script set to /bin/sh with attacker-controlled args)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned travelmate functions shell, how do script/script_args flow into command execution in f_check, and what validation is observed in-source?

## Method

Source oracle over pinned travelmate package (resolve pin at execution): transcribe config → script/script_args → exec chains.

## Required evidence

- Chain multiset with source lines
- Pin receipt

## Controls

- Positive: config-derived script_args into unquoted exec (advisory shape)
- Near miss: argv-pinned invocation
- Negative: literal-only command

## Out of scope

- No shell execution
- No travelmate runtime behavior

## Notes

None.

## Result

Not yet evaluated.
