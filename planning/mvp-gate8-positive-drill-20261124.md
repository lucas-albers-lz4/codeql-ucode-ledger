# Gate 8 known-alert event drill: source and acceptance plan

Status: prepared 2026-11-24; no released event drill has run.

## Inputs already established

- The source-first OpenWrt PR #26933 head manifest selects 128 identities and
  excludes 13. Its captured canonical base
  `727d8d2f8e5b19a2121e2cf05824e9e5cac35310` passes a separate
  [control oracle](../evidence/mvp-event-control-preflight-pr26933-20261124/README.md)
  with the same counts. That PR changes only `package/utils/bzip2/Makefile`;
  it is a clean incoming-path drill candidate, not a known-alert source.
- The default-suite OpenVPN historical positive has a verified R2 alert, but
  `protocols/luci-proto-openvpn/root/usr/share/rpcd/ucode/luci.openvpn.uc`
  is absent from the current v0.6 selected policy. Feeding that historical
  commit to the current selector would require a reviewed historical policy;
  bypassing candidate drift would invalidate the event coverage claim.
- A [local inert feasibility probe](../evidence/mvp-inert-positive-local-20261124/README.md)
  shows that a change to the v0.6-selected LuCI `example.uc` path can produce
  exactly one `ucode/m4/direct-rpc-shell-word` tuple at installed URI
  `usr/share/rpcd/ucode/example.uc`, line 53, columns 26–44 (SARIF end
  exclusive), while a quoted control produces zero. It used an unreleased
  dirty experimental producer and single-file databases. The route oracle
  correction followed an earlier mismatch; this is feasibility evidence,
  not a held-out Gate 8 positive.

## Next execution sequence

1. Producer PR #161 passed its revised native-CLI-provenance head's hosted
   gates and merged as `104a398468f214961168d2edc9a10be45b80062f`.
   Confirm release immutability before a version
   tag, publish the immutable release, independently pin the downstream lock,
   and run the fresh R3 and full 128-path Linux corpus gates. Keep their
   actual timings and peak memory for the event budget.
2. Dispatch the released event job against a freshly API-verified OpenWrt PR
   #26933 head and its canonical base. Require both full selected-corpus
   scans, exact extraction identities, release and source pins, retained
   routing/diagnostics/SARIF and `clean_scan` on the control. This checks the
   clean path only; it cannot satisfy the known-alert criterion.
3. Prepare a known-alert event source without adding a callable dangerous
   change to upstream product code. The current local `example.uc` fixture
   can first exercise internal CI wiring in a disposable fork, but that is
   an internal drill, not evidence of canonical upstream PR coverage. A
   maintainer-facing upstream PR needs explicit authorization and an agreed
   test-only source policy before creation. Alternatively, review a bounded
   historical LuCI policy at the real OpenVPN parent/fix window and accept
   historical PR state in a separately labeled replay; this tests the actual
   advisory but does not demonstrate automatic new-PR detection.
4. Before either positive run, freeze the exact source commit/tree, selected
   identities, source hashes, expected route, rule ID, URI, UTF-16 range,
   multiplicity, clean control and failure/triage disposition in a reviewed
   source-derived oracle. Run actual producer and consumer with separate
   run-owned databases; compare all rows and extraction identities. Retain
   the earlier local probe as a design aid, not the independent oracle.
5. After the manual drill, define the read-only upstream poller using measured
   full-corpus cost and an explicit backlog budget. A branch workflow in
   `codeql-openwrt` is not an upstream trigger. Gate 8 stays open until an
   incoming canonical upstream change is scanned by a released check and
   its result or failure is visible to the maintainer.

No route above establishes actual package-installed bytes. Markup remains
model-inconclusive on the selected `.ut` sources and must remain visible in
each coverage receipt.
