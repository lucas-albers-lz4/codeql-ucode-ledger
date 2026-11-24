# Claim 057: Request values into uci.set in ucode backends

- Status: Blocked
- Program: [Security-40](../planning/security-40-20261124.md), category C
- Producer: `lucas-albers-lz4/codeql-ucode` (routing probe P2)
- Producer commit: codeql-ucode 734555a9f56893e89e678cdee63028fc17ea5bc8; luci b2e0be4b46ec0fd43394c081fa7c50657af14011
- Consumer: none
- Consumer commit: none
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-p35r-3323-6g7g (travelmate delegated UCI write → auto-login command)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned ucode backends write request-derived values via uci cursor set/set_list within the supported slice, and is any value validation observed in-source?

## Method

Bounded same-function slice over manifested application set; record value chains and observed validation (newline/metachar checks) as source observations.

## Required evidence

- Site multiset with chain identities
- Validation observation per site

## Controls

- Positive: request.args value into cursor.set without observed checks
- Near miss: value validated against a fixed allowlist in-source
- Negative: literal set value

## Out of scope

- No downstream injection verdict
- No uci runtime behavior

## Notes

None.

## Result

Blocked — producer routing gate (same as 041–045/047/051). codeql-ucode
`734555a9…` routes only luci-base `luci.uc` (literal-basename `file_globs`,
extractor.rs ~l.40–68; RequestArgsExec.ql l.18 `getBaseName() = "luci"`);
application ucode backends (travelmate.uc etc., the GHSA-p35r anchor scope)
are not extracted ("No matching language found, skipping file",
probe-ucode/VERDICT.md). The claimed bounded same-function request→uci.set/
set_list slice over the manifested application set cannot be produced. The
routed luci-base slice is observable but is not this claim's application
scope. Unblock: routing extension to application .uc + uci.set/set_list sink
model + value-chain/validation observation. The JS-side enumeration under the
execution hold is covered separately by claim 058. Receipts:
`/root/workspace/work/security-40/probe-ucode/{VERDICT.md,MANIFEST.yml,logs/}`.
