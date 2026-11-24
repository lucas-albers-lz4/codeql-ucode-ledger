# Claim 064: POST /ubus/call params type validation

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category F
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-2mpg-6wp5-435p (params type confusion → OOB write)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned uhttpd uh_ubus_call path, what type checks guard `params` before array/object use, and which blobmsg accessor follows each check?

## Method

Source oracle / P1-gated CodeQL C on uhttpd ubus.c: transcribe blobmsg type-check → accessor chains.

## Required evidence

- Check→accessor chain multiset
- Predeclared oracle

## Controls

- Positive: accessor without preceding type check (if present)
- Near miss: checked accessor
- Negative: params unused path

## Out of scope

- No OOB write demonstration
- No blobmsg library internals beyond pinned source

## Notes

None.

## Result

Not yet evaluated.
