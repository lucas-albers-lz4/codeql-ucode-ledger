# Historical security cases for a ucode scanning MVP

Inventory date: 2026-11-23; local OpenVPN baseline added 2026-11-24. This is a
source-backed selection and release plan, not a historical detection claim.
[Claim 075](../claims/075-historical-openvpn-baseline.md) records the baseline
CodeQL run. No default-suite SARIF or downstream acceptance result is asserted.

## Release-sized evidence target

Use **two independently documented historical defects** as the selected MVP
regression cases: OpenVPN key generation and Tailscale login. Each needs its
vulnerable and fixed source revisions. Require exact extraction
of the affected file, a finding at the vulnerable source location, absence of
that finding at the actual patched location, and an eligible unrelated negative
control. Retain a positive model control so an empty real-source result cannot
be mistaken for successful fix discrimination. Run the check in the default
suite on pinned Linux and inspect the emitted SARIF rule, source URI and range.
The downstream OpenWrt job must consume the actual fresh output and verify the
same location for each case. The second case is a holdout for generalization,
but it has different source propagation and shell nesting. It may need a
second narrowly scoped rule or an explicit extension of the first; do not
claim one query detects both until observed. Two cases do not estimate coverage
of OpenWrt security issues.

These are **cases**, not necessarily ledger claim numbers. One case may need a
source/extraction claim, a query/fix-discrimination claim and a live SARIF
producer-to-consumer claim. Combine them only when one run and one oracle
adequately support each boundary. Do not pad the claim count.

## First case: LuCI OpenVPN key generation

[Maintainer advisory GHSA-pm9w-522m-8rrh](https://github.com/openwrt/luci/security/advisories/GHSA-pm9w-522m-8rrh)
describes shell command injection in the authenticated `generateKey` RPC method.
It identifies affected LuCI revision
`769cb13c6999afcd30fd63bad28e96f0a676534e` and a fix at
[`e4ff45ecbc6ad212951815c8c99b2749fbd7de6b`](https://github.com/openwrt/luci/commit/e4ff45ecbc6ad212951815c8c99b2749fbd7de6b).
The fix's parent is `b45584b4e6068b9b096872dd02494a048d869c36`.
In `protocols/luci-proto-openvpn/root/usr/share/rpcd/ucode/luci.openvpn.uc`,
the affected and parent source bytes match; line 71 interpolates
`req.args?.cl_meta` into a shell command without the quote helper and line 77
calls `popen(cmd)`. The fix wraps that argument in `shellquote(...)`; it leaves
the sink in place. The affected/parent file SHA-256 is
`051c8162f826683333e11264615806df5ab08415676c0bd098921cb1b05af991`;
the fixed file SHA-256 is
`6593792678951fd500c2b090d17d9e500a05a642cfb996ee02c1649473152410`.
The advisory's structured “patched versions” field says “None” while its text
names the fix commit. Use these exact source revisions until a package release
or OpenWrt feed lock is independently mapped to the fix.

The source-first oracle and byte-exact staged files are in ignored
`work/mvp-openvpn-oracle/`. They include a known query-positive fixture and a
near miss that has request-argument access and an execution sink but passes an
unrelated constant. A second reviewer confirmed staged Git blobs, digests and
source spans before any analysis run. This is preparation, not a result.

### Current model gap and gate

At clean producer `11a53fd8e911573860950ee8e549b337a8742438`, the
experimental `ShellInjection.ql` and `Models.qll` are byte-identical to the
source-first oracle's `6010ff2c0f101f7629c6fe117a421f671c311a2b` pin.
`RequestArgsAccess` matches a receiver literally named `request`, whereas the
historical file uses `req`. The current query therefore has a source-model
prerequisite to resolve before this case can be a successful detector test.
That is a source-code inference, not an observed CodeQL miss. Even after the
receiver is modeled, the quote barrier must distinguish the actual patched
form from the vulnerable form under the relevant shell context; merely trusting
the name `shellquote` is insufficient. The current candidate query is tagged
`testing` and excluded from `code-scanning.qls`. Existing [claims 018–019](../claims/018-pinned-luci-shellquote-candidates.md)
show bounded candidates on other LuCI inputs, not this historical finding or
default-suite SARIF.

Next run: retain the source oracle, then create separate run-owned databases
for parent, fix and controls. Check route, exact successful file identities,
zero extraction errors, AST source/sink witnesses, full candidate tuples and
multiplicity. If the actual case is absent with the positive control present,
record a bounded model gap. After a producer fix, rerun the same matrix and
promote the scoped check only once the vulnerable/fixed distinction and an
eligible near miss pass. Keep the release integration run separate and fresh.

[Claim 075](../claims/075-historical-openvpn-baseline.md) now records that
local CodeQL baseline at producer `6010ff2c0f101f7629c6fe117a421f671c311a2b`:
both historical files extracted and had exact target AST witnesses, the
candidate query returned zero target rows for both, and the positive/near-miss
controls returned the expected one/zero rows. This establishes the bounded
current-query gap, not a default-suite alert or Linux release acceptance.

## Second case: LuCI Tailscale login

[Maintainer advisory GHSA-xwc5-mx58-rh35](https://github.com/openwrt/luci/security/advisories/GHSA-xwc5-mx58-rh35)
documents root command execution from a delegated LuCI Tailscale account,
conditional on Tailscale being installed and logged out. The mainline source
pair is parent `46cd82328dfb7fbb15961c63f9e674a41cef2500` and
[`507ab5e45c304543d4111af9a331db0f03be6bcb`](https://github.com/openwrt/luci/commit/507ab5e45c304543d4111af9a331db0f03be6bcb).
The advisory also names a separate 25.12 branch fix,
[`756692bbe81c613b412a78df4abc2ab2e22ec7a7`](https://github.com/openwrt/luci/commit/756692bbe81c613b412a78df4abc2ab2e22ec7a7);
do not conflate those branches. Its structured “patched versions” value is
“None”; no package release boundary is established here.

The changed file is
`applications/luci-app-tailscale-community/root/usr/share/rpcd/ucode/tailscale.uc`.
The parent Git blob is `8e2b7aa56a0b37c0cf392fc4c182d6ae1167e858`
(file SHA-256 `3029c32d7ccd18efb95355aa915841e2bf467b0de147ce1a65b68c55fec9d280`);
the fix blob is `b7bf94b0baff7817dad2a010b04e1ba293d59733`
(file SHA-256 `12bffca1f06aae14363f12d98680c0ca3a07223babd26131cc7c1612baf8fc4e`).
In the mainline parent, lines 152–153 read `form_data.loginserver` and
`form_data.loginserver_authkey`; lines 156 and 158 quote the individual values;
line 163 joins them into `login_cmd`. At line 164, `popen` passes that string
within an outer double-quoted `/bin/sh -c` argument. The fix changes only line
164 to quote the *entire* `login_cmd + ' &'` argument. The advisory and commit
explain that command substitutions can be expanded by the outer shell despite
the inner per-value quoting. This mechanism is distinct from the missing quote
in the OpenVPN case.

The reviewed source pair and source-derived extraction/analysis expectations
were staged in ignored `work/mvp-tailscale-oracle/` before the baseline run.
That record remains the pre-run oracle, not a query result.

[Claim 076](../claims/076-historical-tailscale-baseline.md) now records the
post-merge local CodeQL baseline at producer
`18afe771568d373088edee7a790825ee46dec9e0`. The real parent/fix and four
controls extracted exactly; the predeclared AST witnesses appeared; the
current candidate query returned zero nested-path rows and one direct
positive-control row. This is not a default-suite alert or fix-discrimination
result.

Predeclare the source and sink identities and exact patched line before running
CodeQL. Use the actual parent/fix pair and at least one eligible near miss that
keeps the same RPC source and `popen('/bin/sh -c …')` sink but passes an
unrelated constant command, plus a positive model control. Ensure the control
truly preserves the relevant parsing and flow shape; a superficially similar
string is insufficient. The current `RequestArgsAccess` can recognize the initial
`request.args.form_data`, but the path to `login_cmd` passes through `trim`,
`push`, an array and `join`. Its bounded same-function binding model does not
establish that whole path or nested shell evaluation. This is a model inspection,
not an observed query miss. The real fix pair must be evaluated under a model
that accounts for both propagation and the outer shell context.

## Other candidates and scope

| Case | Primary source and change | Role |
|---|---|---|
| LuCI adblock-fast cron injection | [GHSA-ggpf-xrph-wg5v](https://github.com/openwrt/luci/security/advisories/GHSA-ggpf-xrph-wg5v), [fix `f67461fd0255bf992b2b559c22ec288067f2f9da`](https://github.com/openwrt/luci/commit/f67461fd0255bf992b2b559c22ec288067f2f9da), parent `f4d0a44950e42bcbb8eacf715a3493b276a4f3ac`. | Distinct ucode-to-crontab sink and policy context. Consider after the shell-command MVP; a `popen`-only rule cannot be credited with it. |
| LuCI uhttpd ACL read | [GHSA-4h7q-j9hv-2536](https://github.com/openwrt/luci/security/advisories/GHSA-4h7q-j9hv-2536), [fix `d38658bedbdd811b798da16b49301478c6cf21af`](https://github.com/openwrt/luci/commit/d38658bedbdd811b798da16b49301478c6cf21af), parent `b0cead459cfb434f2b2066e03f36c5bf39a583e7`. | Consumer policy/config candidate; not evidence that a ucode query or SARIF check works. |
| BMX7 CGI traversal | [GHSA-8qcq-jgrj-gvmj](https://github.com/openwrt/luci/security/advisories/GHSA-8qcq-jgrj-gvmj), [fix `5890760a454dad2cb00389dba2cdc5e779e0ffdd`](https://github.com/openwrt/luci/commit/5890760a454dad2cb00389dba2cdc5e779e0ffdd). | Shell CGI file, outside the ucode extractor's selected language. |

## Three release tickets and exit criteria

1. **Scoped query or queries:** select both parent/fix source pairs and their
   independent controls, establish extraction and AST witnesses, then implement
   only the source, propagation, sink and quoting semantics needed for defensible
   vulnerable-positive/fixed-negative rules. Evaluate the Tailscale nested-shell
   context separately from OpenVPN's direct interpolation. Retain all exact tuples and
   diagnostics. Keep broader imported-callee and dispatcher claims with their
   existing owners.
2. **Producer CI:** add the proven security query or queries to the default suite and
   run a pinned CodeQL version in Linux CI. Require a real source-location SARIF
   alert on each vulnerable pin, no corresponding fixed alert, the controls,
   and exact extracted file identities. Fail the job on any mismatch.
3. **OpenWrt consumer:** pin the corresponding LuCI corpus/feed revision and
   producer release; perform a fresh extraction and query run, pass its real
   SARIF to the consumer, and assert rule ID, URI and range for both cases plus
   their patched controls. Record package/source-to-installed-byte mapping. A fixture table or
   replayed SARIF does not satisfy this gate.

The first internal release gate can support claims about these **particular**
checks and version pairs after those gates pass. The Tailscale holdout tests a
materially different shell context; two successes still do not establish a
general command-injection detector or a maintainer-ready OpenWrt scanner.
The later [MVP-1.md](../MVP-1.md) adds current-corpus, incoming-change and
operational gates. No release criterion here depends on closing partial claim
005.

## Release execution

The later [MVP-1.md](../MVP-1.md) is the active staged plan. It uses the
user-selected exact model routes, records the current Terra routing failure,
and extends this two-case release gate to corpus-scale and incoming-change CI.
The source evidence in this dossier remains a pre-run oracle, not a detector
result.
