# Claim 066: Basic Auth realm enforcement on handler dispatch

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category F
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-5cgm-8h9x-v28c (release-note cited; realms not enforced for Lua/ucode handlers)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned uhttpd dispatch, which handler paths pass through realm checks and which bypass them, as observable in-source?

## Method

Source oracle / P1-gated CodeQL C: enumerate dispatch branches (cgi/lua/ucode/ubus) and realm-check call presence per branch.

## Required evidence

- Branch→check table with source lines

## Controls

- Positive: dispatch branch without observed realm check (if present)
- Near miss: branch with check
- Negative: non-handler path

## Out of scope

- No auth bypass demonstration
- Realm configuration is runtime state — not modeled

## Notes

None.

## Result

Not yet evaluated.
