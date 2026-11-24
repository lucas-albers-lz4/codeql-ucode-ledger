# Claim 047: Request-controlled paths into ucode fs read/stat

- Status: Proposed
- Program: [Security-40](../planning/security-40-20261124.md), category D
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: not yet resolved for this claim
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-8qcq-jgrj-gvmj (BMX7 unchecked query traversal)
- GHSA-jjcx-c284-2qv8 (openvpn path traversal → root RCE)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned ucode backends pass request-controlled path strings to fs.open/fs.read/fs.stat/fs.readlink within the supported same-function slice, and is any canonicalization observed in-source?

## Method

Bounded slice over manifested application set; record path-construction chains and any observed `..` handling; canonicalization absence is a source observation, not a traversal verdict.

## Required evidence

- Site multiset with chain identities
- Predeclared oracle
- Canonicalization observation per site

## Controls

- Positive: request.args.path into fs.read without observed checks
- Near miss: path joined under a fixed prefix with observed `..` rejection
- Negative: literal path

## Out of scope

- No traversal exploitability claim
- No runtime filesystem state

## Notes

None.

## Result

Not yet evaluated.
