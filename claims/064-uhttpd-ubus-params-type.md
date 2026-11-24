# Claim 064: POST /ubus/call params type validation

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category F
- Producer: source oracle (pinned uhttpd C census; no CodeQL run)
- Producer commit: uhttpd 93b05e0b65d91c23c5aa8fdde378df1f174ec71d
- Consumer: none
- Consumer commit: none
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-2mpg-6wp5-435p (params type confusion → OOB write)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned uhttpd uh_ubus_call path, what type checks guard `params` before array/object use, and which blobmsg accessor follows each check?

## Method

Source oracle / P1-gated CodeQL C on uhttpd ubus.c: transcribe blobmsg type-check → accessor chains.

## Required evidence

- Check→accessor chain multiset
- Predeclared oracle

## Controls

- Positive: accessor without preceding type check (if present)
- Near miss: checked accessor
- Negative: params unused path

## Out of scope

- No OOB write demonstration
- No blobmsg library internals beyond pinned source

## Notes

None.

## Result

Demonstrated — source oracle at uhttpd `93b05e0b…` (clean); advisory shape
FIXED-IN-PIN (fail-no-eligible-instance WITH census); no CodeQL database;
source-shape observation only, no runtime/exploit/vuln verdict.

- params parsed under rpc_policy with RPC_PARAMS = BLOBMSG_TYPE_UNSPEC
  (ubus.c:68) → any JSON value accepted, copied verbatim by blob_memdup (:893,
  type-AGNOSTIC raw-byte copy). The only type-SENSITIVE params consumer is
  blobmsg_for_each_attr (:641, uh_ubus_send_request), guarded at :638-639
  (rejects non-table params → ERROR_PARAMS before iteration). That guard is fix
  e76736e (ancestor of HEAD confirmed) → the advisory array-iteration OOB sink
  is closed.
- cur = tb[RPC_JSONRPC] (:878); blobmsg_data (:879) reads the jsonrpc field
  (policy STRING :66), not params. Legacy call/list: ARRAY early-return (:910) +
  blobmsg_parse_array (:745/:816); uh_ubus_valid_list_params ARRAY guard (:804) +
  blobmsg_data_len (:811); send_list iterator (:764) guarded by caller (:804).
- 18 chains (6 primary uh_ubus_call + 12 secondary legacy-call/list census);
  checked_by_policy 5, untyped_copy 3, near_miss 10, eligible (unguarded) 0.
- Controls 3/3: POS :641 → near_miss (guarded :638); NEAR :879 → near_miss
  (wrong field, STRING policy); NEG uh_ubus_call → negative (obj!=object guard
  :1077 dominates first data.params use :1089). Second pass 18/18 agree. Scanner
  fixed 3× (multi-line parse_array detection; NEG redefined to guard-dominates;
  2-line condition+goto recognition); chain data unchanged.
- Evidence: `/root/workspace/work/security-40/064/` (oracle.{md,json},
  chains.json, census.json, controls.json, provenance.json, run_pipeline.sh,
  build_064.py). Orchestrator re-ran `run_pipeline.sh` (exit 0); uhttpd pin
  clean; spot-checked ubus.c:68/638-639/641/893; ancestry e76736e confirmed.
  Note: lane prose quoted the :638 guard as ARRAY; pinned bytes check
  BLOBMSG_TYPE_TABLE — guard presence and conclusion unchanged.
