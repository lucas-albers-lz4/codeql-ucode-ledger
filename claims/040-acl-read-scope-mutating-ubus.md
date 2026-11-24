# Claim 040: Mutating ubus methods under read-only ACL

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category A
- Producer: source-oracle (pinned luci + rpcd source; no CodeQL run)
- Producer commit: luci b2e0be4b46ec0fd43394c081fa7c50657af14011; rpcd d99f703e4035d03fbcfbada3cb697db346c2b984
- Consumer: none
- Consumer commit: none
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

Demonstrated — at luci `b2e0be4b…` + rpcd `d99f703e…` (clean). The
mechanical grant→handler→effect reconciliation passes its predeclared oracle
gate (exit 0; 21/21 oracle checks, 5/5 controls gate-enforced) after repair
of three script defects: D1 C object registry built from `struct ubus_object`
`.name` registrations (not policy fields); D2 both ucode export forms plus
quoted-key / block-comment / regex-literal / arrow-entry parsing repairs;
D3 per-method/per-call-site literal verb classification with string-safe
identifier tracing. Source-observation only; no CodeQL run; no
authorization/vulnerability claim.

- Base multiset byte-identical (grants.json sha `4d47fe68…`, ubus_grants.json
  `ec861e55…`): **337 ubus grants (240 read / 97 write)**, 55 objects, 168
  (object,function) pairs. Full 337-row join: 226 resolved (369 pairs), 111
  honestly unresolved (110 NOT_IN_PINNED_TREES across 31 unpinned-package
  objects + 1 `luci:p910nd` method absent at this pin).
- **15 read-scope grants across 10 packages cover mutating handlers**
  (corrects the prior lane's 8/5):
  - A1 dockerman `docker.*:["*"]` L11 → `docker.container.ttyd_start` L387 →
    `run_ttyd` L289 (`request.args.id` L291) → `system()` L319/L322,
    caller-influenced cmd (**GHSA-cq4h shape under READ scope**). Note:
    `docker:["*"]` L10 reaches only the GET-method `docker` — rpcd's fnmatch
    matcher (session.c L143–147, `FNM_NOESCAPE`) does not match object
    `docker` against `docker.container`; ttyd_start flows through `docker.*`
    only.
  - A2 `luci.setInitAction` read-granted ddns/sqm/upnp → `sys.uc`
    `init_action` L153 → `system(env -i /etc/init.d/<basename(name)>
    <action>)` L159; basename-guarded, action-whitelisted.
  - A3 `rc:init` read-granted dockerman/ocserv → `rc.c` `rc_init` L318 →
    `execl` L385; action-whitelisted.
  - Nine `file:exec`/`file:*` read grants (dockerman, ocserv, rustdesk-server,
    luci-mod-dashboard/network×2/status×2/system) → rpcd `file.c`
    `rpc_file_exec_run` L1034 → fork + `execv` L1172 of a caller-supplied
    command (`file.write`/`file.remove` mutating writes). `rpc_file_access`
    checks at L1065 (executable) / L1086 (per-cmdstr) noted as source
    observation, no authorization claim. These were invisible to the broken
    C registry pre-fix.
- Counter-cases read-only (tailscale getters, `obtain_device_info`);
  write-scope negatives (`do_login`, `boot_partition`) pass; openvpn
  `generateKey` absent.
- Gaps: uhttpd ubus-scope enforcement outside pinned trees (no authorization
  claims); unpinned-package objects a disclosed coverage limit; JS
  syntax-level only.
- Evidence: `/root/workspace/work/security-40/040/` (ubus_inventory.py,
  handler_registry.json, grant_handler_effect_table.json,
  oracle_comparison.json [all_pass], controls.json, inventory_stats.json,
  ubus_grants.json, summary.md). Orchestrator re-ran `ubus_inventory.py`
  (exit 0, ORACLE+CONTROLS PASS); base hashes immutable; spot-checked
  dockerman acl L10/L11, docker_rpc.uc 289/319/387, session.c 143–147,
  file.c 1034/1065/1086/1172.
