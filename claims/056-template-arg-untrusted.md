# Claim 056: Template/include argument propagation

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category E
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-q335-4c83-c88h (adblock-fast status errors from delegated blocklist names)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Within the bounded markup subset, which template/include call sites pass untrusted-derived arguments, and does the supported graph observe the argument→substitution edge?

## Method

New bounded decision justified by the XSS class (the old template-argument deferral required a distinct analysis need — this is it); stay inside documented subset; no production model.

## Required evidence

- Call-site multiset
- Argument-edge observation receipts
- Subset eligibility per site

## Controls

- Positive: include with request-derived argument in subset
- Near miss: literal argument
- Negative: site outside subset

## Out of scope

- No lift of the general template-argument deferral
- No interprocedural rendering claim

## Notes

None.

## Result

Not yet evaluated.
