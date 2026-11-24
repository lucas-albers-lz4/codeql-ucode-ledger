# Experimental historical shell rules: integration decision

Status: local review snapshot, 2026-11-24. These are experimental rules in
disposable producer branches, not a released suite or a claim of ongoing
OpenWrt security coverage. See [MVP-1.md](../MVP-1.md), claims 075–036 and
the historical case dossier for source-first baselines.

## Local implementation identities

| Case | Producer branch/commit | Rule | Latest evidence |
|---|---|---|---|
| OpenVPN | `security/openvpn-metadata-shell` at `c4829ff1d30225ca758b0f7979f47c3265cf882d` | `ucode/m4/openvpn-raw-metadata-command`, query SHA-256 `559c5174ace56a3b5081906849e3584c4019de14292fbd5ebf34dd97fcb155d5` | Fresh final-commit run under ignored `work/openvpn-rule-shadow-final-20261124-f/`; six-case rule counts 1/0/0/0/0/0, exact extraction once each, zero errors, source/sink AST witnesses, one explicit-query SARIF result at 71:115–132. |
| Tailscale | `tailscale-nested-shell-bounded` at `2dde7010e9bcf7cb445743fc48221bbfadfcaa34` | `ucode/m4/tailscale-nested-shell-candidate`, query SHA-256 `136ec48e2f38c0da03d3dd975fcccae348997dbb6e6ec4a014444c42b6e09bfc` | Fresh final-commit run under ignored `work/tailscale-rule-final-20261124-d/`; parent/fix 1/0, 11 controls one total (`nested_pos.uc`), all 13 files extracted once with zero errors, exact two-field AST and SARIF source locations. |

The OpenVPN final run's `source-first.json` pins its committed query hash and
six independent stage source hashes before execution. Its receipt contains
54 exit-zero extraction, diagnostic and query commands. The explicit SARIF
artifact is a format probe on a copied vulnerable database, not a resolved
default-suite run. The only reported OpenVPN SARIF warning concerned the
1256 MB query-loading cache limit; it did not invalidate the result. The
earlier `work/openvpn-rule-shadow-run-20261124-e/` has a query-byte mismatch
against the final commit and is superseded for this rule. The Tailscale
run-d preflight pins the clean producer commit, source manifest SHA-256
`b1a538d03d60e356ae94cf374a2bfdc9338d81068b9e0a7233ac3bcbf89ac114`
and final query hash; all 36 commands exited zero. Its explicit SARIF has
parent 164:3–49, fixed zero, and sole control `nested_pos.uc` 18:5–51.
The three source-first `constant ||` controls exercise the prior descendant
match issue and now produce zero. A read-only security review found that
specific false-positive concern resolved, while name-based call binding and
runtime helper behavior remain outside the rule's proof.

The first current 21-file slice exposed a global `before/2` query-plan cost:
the prior Tailscale query was interrupted after 187.742 seconds, exit 130,
with 1,354,055,680 bytes peak RSS. The committed revision anchors comparisons
to an exact nested-shell sink and same file. A fresh historical run-d preserved
the matrix, with each candidate query taking 3.099–3.350 seconds. On a copied
21-file database the final query exited zero in 3.196 seconds, peak
450,052,096 bytes, with zero candidate rows. That copied-database check is
only a performance/result probe; its database was built in a separate run.
Same-line constructions are now conservatively excluded. Independent
read-only review found the revision only narrows matching, preserves the
source/sink shapes and has no new false-positive path in the inspected diff.
The same-line exclusion remains a documented false-negative boundary.

## Review boundary and next decisions

Both rules have `@tags testing`; neither is in `code-scanning.qls` or an
immutable producer release. The OpenVPN query restricts the file path to
`usr/share/rpcd/ucode/luci.openvpn.uc`, the RPC name to `generateKey`, and the
argument to `cl_meta`. The Tailscale query models a specific two-field
`trim`/`push`/`join` and nested `sh -c` construction. Their historical
pre/post distinction is a useful regression gate, while these scopes leave
other incoming shell patterns untested. Do not present either as a broad
shell-injection detector or infer runtime exploitability from a row.

Before any default-suite promotion, add stable
metadata/help and review whether a path-specific historical rule is useful
in the default scan. A broader incoming-change check needs separately justified
source/sink/quote coverage and current-corpus alert-quality measurements.
The consumer's local SARIF parser prototype remains offline until a trusted
Linux job generates and passes the actual fresh producer artifact.

An isolated local integration branch `mvp/direct-rpc-suite-draft` at
`299731d8e22112cf88680b89ee08915ff531d273` combines the reviewed direct
handler rule (metadata-only `security`/`medium` default-suite draft) with the
testing-tagged Tailscale rule. On copied historical databases, the default
suite resolved the direct rule plus two diagnostics and emitted the OpenVPN
parent result at 71:115–132 with zero fixed results. An explicit Tailscale
query on copies of its separate databases emitted parent 164:3–49 and zero
fixed results in 3.510/3.505 seconds. These are macOS copied-database
integration probes, not fresh Linux extraction or a versioned release. The
two historical rules remain available as separate regressions; only the
direct handler candidate is drafted for default inclusion.
