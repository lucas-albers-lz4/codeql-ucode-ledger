# Claim 066: Basic Auth realm enforcement on handler dispatch

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category F
- Producer: source oracle (pinned uhttpd C census; no CodeQL run)
- Producer commit: uhttpd 93b05e0b65d91c23c5aa8fdde378df1f174ec71d
- Consumer: none
- Consumer commit: none
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-5cgm-8h9x-v28c (release-note cited; realms not enforced for Lua/ucode handlers)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned uhttpd dispatch, which handler paths pass through realm checks and which bypass them, as observable in-source?

## Method

Source oracle / P1-gated CodeQL C: enumerate dispatch branches (cgi/lua/ucode/ubus) and realm-check call presence per branch.

## Required evidence

- Branch→check table with source lines

## Controls

- Positive: dispatch branch without observed realm check (if present)
- Near miss: branch with check
- Negative: non-handler path

## Out of scope

- No auth bypass demonstration
- Realm configuration is runtime state — not modeled

## Notes

None.

## Result

Demonstrated — source oracle at uhttpd `93b05e0b…` (clean); enumeration
complete; a BYPASS BRANCH is OBSERVED in-source (config-gated reachability, NOT
claimed exploitable); the advisory NORMAL-PATH shape is FIXED-IN-PIN (3aa7e1c
ancestor); no CodeQL database; source-shape observation only.

- Realm enforcement is a property of the dispatch CALL SITE: uh_invoke_handler
  (file.c:881) and uh_invoke_script (:766) carry no realm check themselves.
  dispatch_find (file.c:742-764): pi==NULL → check_url only; pi!=NULL →
  check_path only.
- 5 branches (4 dispatch_handler sites + 1 json-script non-dispatch):
  - B066-01 normal check_url (lua/ucode/ubus): uh_invoke_handler file.c:1039,
    uh_auth_check_url :1038 PRESENT → checked (advisory shape, fixed).
  - B066-02 error-handler check_url: uh_invoke_handler file.c:924 inside
    if(is_error_handler):920 — NO realm call in :920-928 → BYPASS.
  - B066-03 check_path prefix (cgi): uh_invoke_handler :951, uh_auth_check :941
    PRESENT → checked.
  - B066-04 static file / CGI script: uh_file_request :953, uh_auth_check :941
    PRESENT → checked.
  - B066-05 json-script command stage: uh_handler_run :1027 (handler.c:235,
    json_script_run_file :252) → non_handler (not a dispatch_handler).
- Registrations: lua.c:327 / ucode.c:432 / ubus.c:1219 check_url; cgi.c:129
  check_path. ubus.c uh_ubus_allowed_cb (:305) is ubus-level ACL, distinct from
  the HTTP realm check; lua/ucode/cgi carry no internal HTTP realm enforcement.
- Controls 3/3: POS :924 → bypass (positive instance EXISTS); NEAR :1039 →
  checked (uh_auth_check_url :1038); NEG :1027 → non_handler. Second pass 4/4
  dispatch sites + 4/4 registrations agree; no revisions (first-run agree).
- Condition (not exploitability): bypass B066-02 fires only when
  conf.error_handler matches a check_url prefix — runtime config, OUT OF SCOPE
  for a source verdict; recorded as a condition, not asserted exploitable.
- Evidence: `/root/workspace/work/security-40/066/` (oracle.{md,json},
  chains.json, census.json, controls.json, provenance.json, run_pipeline.sh,
  build_066.py). Orchestrator re-ran `run_pipeline.sh` (exit 0); uhttpd pin
  clean; spot-checked file.c:920/924/941/1038/1039; ancestry 3aa7e1c confirmed.
