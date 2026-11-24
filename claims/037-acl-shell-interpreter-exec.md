# Claim 037: Shell-interpreter exec grants

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category A
- Producer: source-oracle method — pinned `openwrt/luci` + `openwrt/rpcd` checkouts, busybox derivation from pinned `openwrt/openwrt` bytes, and an independent libc fnmatch witness; no CodeQL producer run for this claim
- Producer commit: luci `b2e0be4b46ec0fd43394c081fa7c50657af14011`; rpcd `d99f703e4035d03fbcfbada3cb697db346c2b984`; openwrt `4e9642517b48bae612ff10fb72fb9199e559500e` (read via `git show`; working tree not used)
- Consumer: none (no consumer join named in this claim)
- Consumer commit: none
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-vj96-f37g-37f6 / CVE-2026-55897 (advanced-reboot read ACL exposes /bin/sh via file.exec)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

Which pinned ACLs grant exec on shell interpreters or busybox (`/bin/sh`, `/bin/ash`, `/bin/bash`, `/usr/bin/env`, `/bin/busybox`) in any scope?

## Method

Source inventory of exec-grant command strings against an interpreter allowlist fixed before inspection; include symlinked/alternative paths only when the pinned filesystem layout evidence supports them.

## Required evidence

- Interpreter-grant multiset with provenance
- Allowlist derivation recorded (pinned busybox config or package manifest, not assumption)

## Controls

- Positive: `/bin/sh` exec grant fixture
- Near miss: `/bin/shutdown` (not an interpreter)
- Negative: `/etc/init.d/uhttpd restart` pinned exec

## Out of scope

- No claim about what an interpreter grant enables at runtime
- No argv injection modeling

## Notes

None.

## Result

Demonstrated 2026-11-24 (local source-oracle + libc witness; no CodeQL run).

Allowlist (fixed before inspection): `/bin/sh`, `/bin/ash`, `/bin/bash`,
`/usr/bin/env`, `/bin/busybox`. Derivation recorded from pinned busybox 1.37.0
package bytes at openwrt corpus-lock `4e9642517b48bae612ff10fb72fb9199e559500e`
via `git show` (shared working tree dirty — not used as a pin):
`Config-defaults.in` ASH=y / SHELL_ASH=y, ENV=y, BASH_IS_NONE=y, HUSH=n;
`/bin/busybox` installed per Makefile `PKG_FILE_MODES` (4755); tarball sha256
`3311dff32e746499f4df0d5df04d7eb396382d7e108bb9250e7b519b837043a4`.
Disclosed limitation: applet→install-path mapping lives in `applets.src.h`
inside the hash-pinned tarball (not staged); `/bin/sh`, `/bin/ash`, `/bin/bash`
paths are question-fixed, and no symlinked/alternative paths are admitted
without pinned filesystem-layout evidence.

Semantics verified against pinned rpcd source: exec-capable = file scope with
functions ∩ {exec, *} ≠ ∅ in any recognized block; function matching fnmatch
`FNM_NOESCAPE` (`session.c:146-147`). The bare-executable check
(`file.c:1065`, `rpc_file_access(sid, executable, "exec")` with
`rpc_canonicalize_path(rpc_file_exec_lookup(cmd))`, lookup `file.c:852-890`)
fnmatches the ACL pattern against the executable WITHOUT argv — so glob
coverage is tested against the five bare allowlist paths, and the executable
token is `object.split(" ")[0]` with exact string equality (not prefix:
`/bin/shutdown` must not match `/bin/sh`).

Corpus: same complete enumeration as 035/036 — 119 rpcd-loaded ACL JSONs +
1 foreign excluded; 914 rpcd entries; 173 exec-capable file entries.

Headline: interpreter_exact grants = 0 (no ACL at this pin names an allowlist
path as executable token with exec/* function). Glob-covering grants = 1:
`applications/luci-app-filemanager/.../luci-app-filemanager.json:10`, write
block, `"/*": ["list","read","write","exec"]` — witness confirms `/*` MATCHes
all five allowlist paths, so exec on any interpreter is covered for
write-permitted users of that group (source observation only). The historical
anchor (GHSA-vj96-f37g-37f6 / CVE-2026-55897, advanced-reboot read ACL
`/bin/sh` exec) is ABSENT at this pin — advanced-reboot read is ubus-only; its
sole file exec is `/sbin/poweroff` under write (not an interpreter). 12
bracket-argv patterns (wget/vnstati/ip/mmcli) hand-fixed before the witness:
tokens non-interpreter, wildcards sit in argv which the bare-executable check
never sees; all 55 allowlist probes NOMATCH.

Witness: same binary/hash as 035 (glibc, C locale, FNM_NOESCAPE only);
220/220 probe pairs matched, 0 mismatches; rebuild byte-identical;
aggregation recomputed glob coverage from witness output with 0 disagreements.
Six-package hand oracle fixed before inventory; exact-multiset and
classification comparisons ALL PASS. Controls 5/5 PASS (positive `/bin/sh`
exec; near-miss `/bin/shutdown` excluded by exact equality; negative mirroring
real pinned uhttpd init-script exec; extras `/bin/sh -c id` and
`/bin/busybox sh` token checks).

Evidence: `work/security-40/037/` (summary.md, interpreter_multiset.json,
classification.json, multiset.json, oracle.md/json with derivation citations,
hand_fixed.json, probes/expectations.tsv, witness_output.tsv,
witness_results.json, controls.json, fixtures/, witness_receipts.json,
provenance.json, run_pipeline.sh). Reproduce: `sh 037/run_pipeline.sh` from
`work/security-40`. Orchestrator re-ran 2026-11-24: 173 exec-capable,
0 exact + 1 glob-covering, 220/220 witness, all controls pass.

Gaps: glibc only (musl not exercised); allowlist install paths question-fixed
as disclosed; no argv-injection modeling; no runtime or authorization claim.
