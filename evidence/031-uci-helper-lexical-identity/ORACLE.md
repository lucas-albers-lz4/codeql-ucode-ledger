# Source-first oracle

Prepared before the corrected detached-checkout query run. It fixes the three intended inputs, source facts, and expected query/diagnostic identities. It does not assume that a command succeeds or that a runtime call occurs.

## Pinned upstream positive

Producer `1ccf5268e6915dc8d4cbb926b28be8ff79bcb0ed` contains the unchanged observer introduced at `d3981986ac685d6fcbb78a3b369aa4ed526c1e4b`. The pinned LuCI file is revision `b2e0be4b46ec0fd43394c081fa7c50657af14011`, blob `c38a42b10bfefbaa31741feae9395abd8a1f8e40`, SHA-256 `ac75cfef7d74f87ed7f957778004a7bf486c76df699398c215795b4947e0c93e`. Source lines 79 and 28 contain the selected `ubus_call('uci', 'commit', object)` call and `ubus.call(object, method, args)` helper forwarding call, respectively. Expected observer row if reached: caller `uci.uc:79:9–79:81`, helper label `25:28`, forwarding call `uci.uc:28:12–28:42`.

## Positive control: formal reassigned

`reassigned-formals.uc` has `ubus_call('uci', 'commit', {})` at line 5; the helper assigns `'changes'` to `method` at line 2 and passes identifier `method` in argument position 1 of `ubus.call` at line 3. Expected observer row if reached: caller `reassigned-formals.uc:5:1–5:30`, helper label `1:3`, forwarding call `reassigned-formals.uc:3:10–3:40`. This distinguishes a lexical binding check from a value-preservation check.

## Eligible near miss: copied alias

`alias-instead-of-formal.uc` has the same caller shape at line 5 and a top-level same-file helper. Its helper passes identifier `forwardedMethod` as argument 1 of direct `ubus.call` at line 3 after copying `method` into a local on line 2. Expected observer output: no row. The separate eligibility diagnostic should still identify the caller/helper candidate, direct forwarding call `3:10–3:49`, and argument-1 identifier `forwardedMethod` at `3:28–3:43`, resolving to the local declaration, not the formal.

The `3:28–3:43` source-only argument span uses an end-exclusive byte position. The producer's decoded CodeQL entity uses the observed inclusive end-column convention and reports `3:28–3:42`. This discrepancy is retained in the run record; this oracle has not been rewritten to match output.
