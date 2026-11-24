# Claim 055: uhttpd CGI error/URI reflection

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category E
- Producer: source oracle (pinned uhttpd C emission census; no CodeQL run)
- Producer commit: uhttpd 93b05e0b65d91c23c5aa8fdde378df1f174ec71d
- Consumer: none
- Consumer commit: none
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- CVE-2018-19630 (cgi_handle_request reflected XSS via URI)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned uhttpd source, where do error/response paths echo request URI or header data into HTML output, and is any encoding observed in-source?

## Method

Source oracle on uhttpd 93b05e0 cgi.c/uh_error paths; CodeQL C if P1 supports; record exact echo sites and any escaping calls.

## Required evidence

- Echo-site multiset with source lines
- Encoding observation per site

## Controls

- Positive: URI echoed into error body without observed encoding
- Near miss: echoed through an observed escape helper
- Negative: fixed literal error body

## Out of scope

- No reflected-XSS execution
- No HTTP parsing completeness

## Notes

None.

## Result

Demonstrated — at uhttpd `93b05e0b…` (clean). Bounded source observation;
source-only (P1 PASS makes C extraction viable, but the exhaustive census
left no distinct decision — 0 databases / 0 queries).

- Every request-URI→HTML echo passes through `uh_htmlescape`
  (utils.c:300–323; escape set exactly `" & ' < >` → `&#xNN;`,
  utils.c:284–298,318). **No unencoded URI→HTML reflection site at the pin.**
- 5 request-data sites, all encoding-observed: R1 CGI 403 cgi.c:79→81–83
  (OOM fallback literal "the url"); R2 file 403 file.c:727→729–731; R3 404
  file.c:1064→1066–1067 (fallback ""); R4 dirlist title/h1
  file.c:569→582–585 (emitted twice); R5 dirlist entries file.c:544→549–557
  (filesystem dirents, indirect; `'` in escape set covers single-quoted href).
- Negative context: 24 fixed-string/non-request error pages (27 emitter call
  sites enumerated: 11 uh_header_error + 10 uh_client_error + 6
  ops->client_error; `<h1>%s</h1>` summary slot fixed at every caller). 9
  non-HTML echoes out-of-scope (Location/CORS headers, plain-text
  CGI/lua/ucode 500s). Script-generated HTML relayed by relay.c/proc.c is a
  declared scope boundary.
- CVE-2018-19630 shape fixed in-pin: `cdfc902` "cgi: escape url in 403 error
  output" is an ancestor of HEAD (orchestrator-verified).
- Controls: near-miss PASS (R1 cgi.c:79–83 via escape helper); negative PASS
  (client.c:259, 400 fmt=NULL); positive FAIL-NO-ELIGIBLE-INSTANCE — census
  proves no unencoded emission at the pin; no synthetic instances (the
  historical unencoded shape is only studyable pre-cdfc902, outside claim).
- No exploitability/reachability/runtime/XSS verdict beyond the cited
  emission/encoding; no gate lifted. OOM fallbacks observed in-source, not
  runtime-exercised.
- Evidence: `/root/workspace/work/security-40/055/` (oracle.{md,json},
  reflection_sites.json, controls.json, provenance.json, run_pipeline.sh,
  results/verify_receipt.json citation_checks PASS, logs/). Orchestrator
  re-ran `run_pipeline.sh` (exit 0, verify exit 0); spot-checked utils.c
  300/318, cgi.c 79/81–83, file.c 727/729, client.c 259; cdfc902 ancestry
  confirmed.
