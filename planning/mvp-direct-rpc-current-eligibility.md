# Current LuCI rpcd direct-rule eligibility, 2026-11-24

This is a source-first denominator for the existing 17-file rpcd slice in
[the bounded corpus manifest](mvp-bounded-corpus-v0.1.json), selected by prior
claim 081. The disposable LuCI checkout was clean at
`b2e0be4b46ec0fd43394c081fa7c50657af14011`; the current producer rule
reviewed was `DirectRpcShellWord.ql` at clean producer
`7c62553b7a81b236b75d1b1fa0d50c612a020cc5`. Source bytes and route
expectations for the 17 files are pinned in the manifest. The
[site table](mvp-direct-rpc-current-sites-v0.1.csv), SHA-256
`4cb78b8dde274e020010afdf3b8d9e4bf01a232f1578c79357c3307f3b033528`,
lists all 24 noncomment textual `popen(` lines in those files, across ten
source files. A local independent text scan matched the table's exact
path/line set and multiplicity. This is a source-site census, not an AST
identity or reachability proof.

| Direct-rule relation | Sites | Source observation |
| --- | ---: | --- |
| Supported raw direct handler-field template positives | 0 | No selected current site has the rule's unquoted direct `request.args.field` substitution in a command passed directly to imported `fs.popen`. |
| Quoted structural near misses | 2 | `modules/luci-base/root/usr/share/rpcd/ucode/luci` lines 343 and 400 pass `swconfig` templates containing `shellquote(request.args.switch)` directly to `popen` in returned call handlers. |
| Fixed literal commands | 9 | The `popen` argument is a fixed command at the listed source site. |
| Unsupported helper or assembled-command forms | 13 | Examples include the lldpd helper sink at line 6, the WOL request-derived executable and `map`/`join` command at line 42, and Tailscale's nested `/bin/sh -c` construction at line 207. No safety judgment follows from exclusion. |

The 76-file source-staged local scan's zero SARIF results are consistent with
this narrow classification. They do not establish precision, safety,
installed-byte coverage or the absence of unsupported flow.
[Claim 087](../claims/087-current-luci-quoted-switch-ast.md) later checked
distinct AST identities for the two quoted near misses and a synthetic raw
sibling positive in the same staged slice. It did not establish a new
default-suite alert or broader flow. A separate claim
can test helper caller-to-formal flow using lldpd; it must not silently extend
the promoted direct rule. Broader query/model scope belongs with open
[ucode #54](https://github.com/lucas-albers-lz4/codeql-ucode/issues/54) and
blocked [#50](https://github.com/lucas-albers-lz4/codeql-ucode/issues/50).
Deferred markup dataflow remains [#57](https://github.com/lucas-albers-lz4/codeql-ucode/issues/57).
