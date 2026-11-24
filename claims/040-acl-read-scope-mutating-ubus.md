# Claim 040: Mutating ubus methods under read-only ACL

- Status: Partial
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

Partial — source traces complete and line-anchored; the mechanical
grant→handler→effect reconciliation failed its oracle gate on three
identified script defects (fix lane dispatched).

- 337 ubus-scope grants (240 read / 97 write), 55 distinct objects, 168
  distinct (object,function) pairs; multiset mechanically complete and
  oracle shape checks PASS; 17 ucode backends (10 extensionless).
- **8 read-scope grants across 5 packages cover mutating handlers**, in
  three traces orchestrator-verified at the cited lines:
  - A1 dockerman: read `docker:["*"]` L10 + `docker.*:["*"]` L11 →
    `docker_rpc.uc` `ttyd_start` L387 → `run_ttyd` L289 (`request.args.id`
    L291) → `system()` L319/L322, caller-influenced cmd. **GHSA-cq4h shape
    present under READ scope at this pin.**
  - A2 `luci.setInitAction` read-granted by ddns L7 / sqm L14 / upnp L7 →
    backend L75/L85 → `sys.uc` `init_action` L153 →
    `system(env -i /etc/init.d/${basename(name)} ${action})` L159;
    basename-guarded, action-whitelisted in the backend.
  - A3 `rc:init` read-granted by dockerman L15 / ocserv L17 → pinned rpcd
    `rc.c` `rc_init` L318 → `execl` L385; action-whitelisted.
- Counter-cases verified read-only (tailscale getters, advanced-reboot
  `obtain_device_info`); negative controls write-scoped only (tailscale
  `do_login`, advanced-reboot `boot_partition`); openvpn `generateKey`
  absent at this pin.
- Why Partial: mechanical reconciliation exit 1 (recorded stop) — C registry
  matches policy-field `.name` instead of object registration;
  `docker_rpc.uc` "return methods;" export form unparsed (A1 rows=0); verb
  classification too coarse for mixed-literal bodies (N1/N2 misclassified);
  255/337 join rows unresolved by the defective registry stage. Full join
  table retained; fix lane repairs the three defects and re-runs.
- Gaps: uhttpd ubus-scope enforcement layer outside pinned trees (no
  authorization claims); objects from unpinned packages honestly unresolved;
  JS syntax-level only.
- Evidence: `/root/workspace/work/security-40/040/` (ubus_grants.json,
  handler_registry.json, grant_handler_effect_table.json,
  oracle_comparison.json [FAIL record], controls.json, js_syntax_shapes.json,
  summary.md); orchestrator re-ran `ubus_inventory.py` (exit 1, same
  identified failures).
