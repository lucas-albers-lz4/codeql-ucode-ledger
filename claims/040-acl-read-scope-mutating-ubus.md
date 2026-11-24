# Claim 040: Mutating ubus methods under read-only ACL

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category A
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-cq4h-h8jr-3xqv (dockerman ttyd_start under read ACL)
- GHSA-vrj9-6xwg-6cf9 (openvpn generateKey)
- GHSA-xwc5-mx58-rh35 (tailscale do_login)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned read-scope ubus grants expose methods whose handler source performs a mutating effect (exec, file write, service action), and can that effect be observed in pinned handler source?

## Method

Join read-scope ubus grant inventory to handler source effects: locate the granted object/method handler in pinned ucode/JS/shell source and record the observed effect shape. Effects are source observations, not runtime verdicts.

## Required evidence

- Grant→handler→effect table with source lines for each hop
- At least one fully traced advisory-shaped case and one read-only counter-case

## Controls

- Positive: read-granted method whose handler calls system()/fs.exec (advisory shape)
- Near miss: read-granted method with pure-read handler
- Negative: write-scope grant of the same method

## Out of scope

- No authorization_violation emission
- No claim the handler is registered/live at runtime
- JS handler effects stay syntax-level under existing holds

## Notes

Distinct from consumer handler_effects (which covers inventoried luci-ssl exec methods): this is the read-scope cross-application decision.

## Result

Not yet evaluated.
