# uhttpd resource-lifecycle decision packet

Status: DECISION INPUT ONLY. This packet creates no ledger claim, lifts no gate,
asserts no analyzer `path_found`, and reports no runtime or exploit verdict.
It answers the Security-40 deferral condition ("a distinct static-observation
decision") for three published uhttpd advisories.

- Corpus: `openwrt/uhttpd` (https://github.com/openwrt/uhttpd)
- Primary pin: `93b05e0b65d91c23c5aa8fdde378df1f174ec71d`
  ("ubus: keep ubus list response encoding within encodable bounds", 2026-11-05)
- Pin alignment: equals upstream `master` HEAD at check time (git ls-remote,
  recorded in `provenance.json`).
- Method: pinned-blob reads only (`git show <commit>:<path>`), sha256 recorded
  per file, structural line-order oracle, positive/near-miss/negative controls.
  No CodeQL database, no heavy run, no runtime measurement.
- Regenerate: `./run_pipeline.sh` (exits 0 only on complete pinned reads and
  passing control discrimination). Outputs: `source-census.json`,
  `provenance.json`.

Core blob identities (sha256 of `git show <pin>:<path>` output):

    ubus.c    11638cf888043136b0822133f6b314b7518f7187c56f9254b36506306e8a6e77
    client.c  54b93e18e3f2199906297995460504490409c84747d3a6551a0e075f34692607
    uhttpd.h  cbd046b4d0c1b8fa9b189b3c381403a0309854959d9480e71c79d73c2c396629

Full per-file hashes, blob ids, advisory snapshot hash and retrieval timestamps:
`provenance.json`. Advisory text is used as motivation/source-shape only.

## Recommendation

Option B — source-oracle claims with fail-no-eligible-instance + census.

All three advisory shapes are FIXED at the pin. Each fix is an upstream commit
ancestral to the pin, and a bounded structural oracle (O1/O2/O3 below) finds
zero eligible instances at the pin while firing correctly on the pre-fix
parent blobs and on minimal synthetic regressions. The deferral condition is
satisfied by a static-observation decision that needs no runtime measurement.
Record, per advisory: verdict `fixed_at_pin`, fix commit, census, eligible
instance count 0 (fail-no-eligible-instance). Do not assert analyzer
`path_found`; do not lift gates; any ledger recording is a separate authorized
step — this packet itself creates no claims.

## Advisories and pin verdicts

### 1. GHSA-wvgh-cm54-q6f6 — subscribe client refcount leak (moderate)

Published 2026-11-25. Advisory shape (as reported): `/ubus/subscribe` takes a
client reference that the success path never releases; the client is not freed
at close and subscriptions keep firing.

Pin verdict: FIXED. Fix commit
`3c48b9e17d2086f9756b97e5825c2ebdf3ed233a` ("ubus: release client refcount on
successful /ubus/subscribe", 2026-08-03), ancestral to the pin.
https://github.com/openwrt/uhttpd/commit/3c48b9e17d2086f9756b97e5825c2ebdf3ed233a

Evidence at pin (path:line):

    ubus.c:445   uh_client_ref(cl)                      ref taken
    ubus.c:465   cl->dispatch.free = uh_ubus_subscription_free   release hook installed
    ubus.c:467   uh_client_unref(cl)                    SUCCESS-path unref (the fix)
    ubus.c:468   return
    ubus.c:471-474  err_unregister -> err_unref: uh_client_unref(cl)   error-path unref
    ubus.c:409-411  remove_cb: uloop_timeout_cancel + ubus_unregister_subscriber
    client.c:860-861  client_close: if (cl->refcount) return   close guard
    client.c:877      uh_dispatch_done(cl) before free(cl) at client.c:887
    uhttpd.h:443-452  uh_client_unref: refcount==0 && CLIENT_STATE_CLEANUP
                      -> ustream_state_change (close wakeup)

Ref/unref balance at pin (call sites): subscribe 1 ref / 2 unref (success and
error paths, mutually exclusive); send_list 1/1 (799/844); request_object 1/1
(953/1003); call 1/1 (1075/1110). No unbalanced path in the corpus.

Oracle O1 observes: ref presence; success-path unref between the
`dispatch.free` install and the success `return`; error-path unref; close
guard and dispatch-done-before-free ordering; unref close-wakeup.
Oracle O1 cannot observe: runtime refcount values; whether rpcd ACLs admit
`subscribe` for a given credential (external configuration); callback vs
client-free event interleaving; libubox internals.

### 2. GHSA-83vv-qrc6-h3hx — non-POST /ubus url_path leak (moderate)

Published 2026-08-03. Advisory shape (as reported): `uh_ubus_handle_request`
strdups the URL into `du->url_path` but installs `d->free` only for POST;
non-POST methods reach the dispatch memset with the allocation live.

Pin verdict: FIXED. Fix commit
`42e30caa704e4e6e28fc7412e0006959eb247c44` ("ubus: set d->free unconditionally
to fix url_path leak", 2026-08-03), ancestral to the pin.
https://github.com/openwrt/uhttpd/commit/42e30caa704e4e6e28fc7412e0006959eb247c44

Evidence at pin:

    ubus.c:1175   du->url_path = strdup(url)            allocation
    ubus.c:1182   d->free = uh_ubus_request_free        UNCONDITIONAL install (the fix),
                                                       before the method switch at 1184
    ubus.c:1184-1196  GET / POST / default branches
    ubus.c:1197   uh_request_done(cl)                   trailing request_done
    ubus.c:1205-1206  free(du->url_path); du->url_path = NULL   covers paths that
                                                       return without request_done
    ubus.c:617-618  uh_ubus_request_free: free + NULL
    client.c:130  uh_request_done: uh_dispatch_done(cl)
    client.c:132  memset(&cl->dispatch, 0, ...)         AFTER dispatch_done
    client.c:88-91  uh_dispatch_done invokes cl->dispatch.free(cl)

Oracle O2 observes: strdup site; free-hook install ordered before the method
switch (unconditional); free+NULL inside `uh_ubus_request_free`;
dispatch-done-before-memset ordering; trailing free+NULL.
Oracle O2 cannot observe: runtime allocation sizes or heap state; whether a
non-POST `/ubus` request passes the auth gate (client.c:698 dispatches
`/ubus` only after `uh_path_allowed`); actual request mixes.

### 3. GHSA-vhx4-3p5q-m59q — header accumulation (moderate)

Published 2026-07-30. Advisory shape (as reported): header lines accumulate
into `cl->hdr` with no cumulative count/byte ceiling; the advisory describes
OOM and an unreachable listener as the reported consequence (that consequence
statement is the advisory's, not a verdict of this packet).

Pin verdict: FIXED. Fix commit
`f6c2fcfa539de49ddf6de8f805110c8804602e98` ("client: cap cumulative header count
and bytes per request", 2026-07-24), ancestral to the pin; companion
`f682ccabee9ed5f39dd3b0aaf96228975eeb478d` (chunked-trailer parsing, same day)
extends the cap to trailers.
https://github.com/openwrt/uhttpd/commit/f6c2fcfa539de49ddf6de8f805110c8804602e98

Evidence at pin:

    uhttpd.h:75-76  UH_LIMIT_HEADER_COUNT 100 / UH_LIMIT_HEADER_BYTES 16384
    uhttpd.h:360-361  size_t header_count / header_bytes fields
    client.c:550-551  per-line increments (name+value+NUL bytes)
    client.c:552-556  cap check -> uh_header_error(cl, 431, ...) -> return,
                      BEFORE the append at client.c:658
    client.c:658      blobmsg_add_string(&cl->hdr, data, val)   accumulation site
    client.c:720-727  chunked-trailer branch applies the same caps
                      (connection_close on overflow)
    client.c:401      memset(&cl->request, 0, ...)   per-request counter reset
    client.c:58       blob_buf_init(&cl->hdr, 0)     per-request buffer re-init
    client.c:884      blob_buf_free(&cl->hdr)        reclaim on close

Other `cl->hdr` writers are bounded, non-loop additions: file.c:945-946
(auth user/pass, 2 entries) and handler.c:94 (rewrite URL, 1 entry). The only
accumulation loop is client.c:658, and it is capped.

Oracle O3 observes: counter increments; count AND byte cap checks ordered
before the append; 431 rejection; constant definitions; per-request reset and
re-init; trailer cap; reclaim on close.
Oracle O3 cannot observe: adequacy of the cap values for legitimate traffic;
libubox `blob_buf_grow` ceiling/fatal-exit behavior (external dependency);
actual RSS growth or listener state; keep-alive traffic patterns.

## Cleanup census (pin, call sites; full inventory in source-census.json)

    uh_client_ref(cl)          4   ubus.c 445, 799, 953, 1075
    uh_client_unref(cl)        5   ubus.c 467, 473, 844, 1003, 1110
    dispatch.free assignments  4   file.c:665, proc.c:376, ubus.c:465, ubus.c:1182
    dispatch.req_free          2   ubus.c 1012, 1191
    memset(&cl->dispatch)      1   client.c:132 (after uh_dispatch_done at 130)
    uh_request_done(cl)       21   (ubus.c 8, client.c 4, file.c 7, auth.c 1, handler.c 1)
    uh_dispatch_done(cl)       2   client.c 130, 877
    blob_buf_free             10   (cl->hdr client.c:884; cl->rhdr 885; ubus/proc buffers)
    free()                    25
    ubus_unregister_subscriber 3   ubus.c 414, 424, 471
    cl->hdr append sites       5   client.c 223, 658; file.c 945, 946; handler.c 94
    header cap checks          4   client.c 552, 553, 721, 722
    url_path strdup / free     1 / 2   ubus.c 1175 / 617, 1205

## Oracle controls and discrimination

Positive controls are pinned pre-fix blobs (parents of the fix commits);
near-misses are synthetic single-edit regressions of the pin (labeled, never
corpus); the negative control is the pin itself. All discriminated as designed
(`run_pipeline.sh` exits non-zero if any control fails):

    P1  d6205aad:ubus.c (pre-fix 1)      O1 eligible=true   PASS
    P2  e76736e5:ubus.c (pre-fix 2)      O2 eligible=true   PASS
    P3  7b1bec4:client.c+uhttpd.h        O3 eligible=true   PASS
    NM1 success-path unref deleted       O1 eligible=true   PASS
    NM2 free install moved into POST     O2 eligible=true   PASS
    NM3 cap block deleted, counters kept O3 eligible=true   PASS
    NM4 count cap only (byte cap gone)   O3 eligible=true, bytes_cap=false   PASS
    NM5 comment-only edit                all verdicts unchanged             PASS
    NEG pin 93b05e0                      O1/O2/O3 eligible=false            PASS

NM3/NM4 matter: counters without a dominating cap, and a partial (count-only)
cap, are both still eligible — the oracle does not accept "some mitigation"
as "fixed".

## Options comparison

A. Remain deferred.
   Keeps the three advisories unresolved indefinitely even though the corpus
   is fixed and the shapes are statically decidable. The deferral was
   conditioned on a distinct static-observation decision; this packet is that
   decision, so the condition no longer supports deferral. Rejected as a
   terminal state (acceptable only if the program refuses source-oracle
   claims wholesale, which is a policy choice, not an evidence gap).

B. Source-oracle claims with fail-no-eligible-instance + census.  RECOMMENDED.
   Bounded, structural, reproducible; zero eligible instances at the pin;
   negative result is auditable via census + controls rather than asserted.
   No runtime claim, no gate lift, no fabricated instance, no `path_found`.
   Residual risk: a semantically equivalent refactor could break balance in a
   way line-order checks miss (mitigated by function-scoped checks and
   near-miss controls; interprocedural dataflow is explicitly out of scope).
   Re-running the pipeline against a future pin re-decides automatically.

C. Analyzer coverage-gap ticket only.
   Records a tooling gap but yields no per-advisory decision and leaves the
   deferral open. It also overstates the gap: these three shapes ARE decidable
   by a bounded structural oracle, as demonstrated. Rejected as the sole
   action; a coverage-gap note may accompany B for shapes beyond this oracle
   (event-ordering races, external-dependency behavior).

Rejected alternatives summary: A rejected because the deferral condition is
now satisfied; C rejected because it decides nothing and mischaracterizes a
decidable shape class as undecidable.

## Non-goals (explicit)

- No runtime/exploit verdict; no reproduction of OOM, crash, or listener loss.
- No claim about rpcd ACL reachability of `subscribe`/`/ubus` (external config).
- No claim about libubox allocation-ceiling behavior (external dependency).
- No judgment that cap values (100 / 16384) are adequate for all legitimate
  traffic — only that a cumulative cap exists and dominates the append.
- No proof of absence of callback/client-free ordering races; the static
  chain (dispatch.free installed before unref; uh_dispatch_done before
  free(cl)) is present, event interleaving is not statically decided.
- No CodeQL database, no analyzer `path_found`, no gate lift, no ledger claim
  created or edited by this packet.

## Residual static observations (context, not claims)

- The subscribe success path overwrites `dispatch.free` (ubus.c:465) over the
  request hook (ubus.c:1182). On the GET-subscribe path the only `du`
  allocations are `url_path` (freed at ubus.c:1205 before return) and
  `subscriber` (unregistered at ubus.c:420-425 on error); `jstok`/`jsobj`/`buf`
  are POST-only. The overwrite therefore strands no enumerated allocation at
  the pin. This is a static enumeration, not a runtime guarantee.
- `uh_ubus_remove_cb` (ubus.c:406-417) unregisters then calls
  `uh_request_done` on the still-live client; ordering is coherent in source.
- Adjacent resource hardening in the same upstream window (list-response
  encoding bounds 93b05e0; script-slot cap 8791d39 and peer-close slot release
  8e0d492) shows active lifecycle maintenance; noted as context only.

## Public-safety note

This packet cites only public upstream commits and published GitHub security
advisories. Operational provenance (local checkout path, retrieval timestamps,
per-file hashes, control blob ids) is confined to `provenance.json` and the
pipeline scripts. Advisory descriptions are quoted as reported shapes, not as
findings of this investigation.