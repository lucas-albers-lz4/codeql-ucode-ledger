# Claim 058: JS rpc.declare UCI set call sites (enumeration only)

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category C
- Producer: syntax oracle (pinned luci JS rpc.declare census; no CodeQL run)
- Producer commit: luci b2e0be4b46ec0fd43394c081fa7c50657af14011
- Consumer: none
- Consumer commit: none
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- GHSA-p35r-3323-6g7g class
- 24-package program package 22 precedent

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

What is the complete pinned-site multiset of JS UCI set call shapes (rpc.declare with set/commit semantics) in the manifested application set, as source enumeration under the existing execution hold?

## Method

Source enumeration only, re-pinned manifest, receiver/computed-name/shadow controls recorded; no JS execution, no hold lift.

## Required evidence

- Full expected multiset from independent enumeration
- Control classification per site

## Controls

- Positive: literal rpc.declare set call
- Near miss: computed method name (classified, not resolved)
- Negative: rpc.declare read-only call

## Out of scope

- No execution
- No Track A promotion
- Hold remains until separately lifted

## Notes

None.

## Result

Demonstrated — syntax census at luci `b2e0be4b…` (clean); no CodeQL database,
no JS execution; JS UCI hold and Track A state unchanged; declaration-site
syntax only (no argument/taint/reachability tracking).

- 7 counted rpc.declare UCI-write sites, all `uci_write_literal` (literal
  object 'uci' + literal write-family method, module rpc receiver with
  'require rpc', unshadowed): uci.js:52 callOrder(order), :59 callAdd(add),
  :67 callSet(set), :74 callDelete(delete), :81 callApply(apply), :88
  callConfirm(confirm); wireless.js:836 callUciRename(rename). Method
  sub-census 1 each.
- Absence census (honest zeros): commit/set_list/revert/rollback/state/
  configs/reload_config declares 0; computed uci object/method 0; shadowed
  uci receiver 0. No literal commit declare — commit is reached via
  apply+confirm (uci.js:998/1004, doc-corroborated at pin).
- Completeness: 420-file manifest; 308 grep lines = 303 active member calls +
  5 comments = 7 counted + 301 exclusions (5 comment, 2 uci_read get/changes,
  294 non_uci incl. 24 computed-object app-plugin/hostapd + 3 alternate-
  receiver luci.js bootstrap); 0 uncovered / 0 phantom. Two independent
  passes (grep+regex-mask vs full JS tokenizer) agree field-by-field on all
  303 calls; 127 cited files sha256-verified, 23 nl -ba windows.
- Controls 3/3 (positive uci.js:67 set; near-miss dockerman common.js:90
  docker.container rename excluded + uci.js:44 get read; negative
  clamav.js:329 commented declare etc.).
- Gaps/incidents logged: rpcd uci.c taxonomy reference is upstream master
  (sha recorded), not pinned to the paired rpcd — family split corroborated
  by pinned uci.js docs; computed-object exclusion rests on expression shape,
  not a runtime resolver proof; mid-lane pass_b tokenizer reverted to a
  pre-patch hybrid (cause unknown), detected by the pipeline, rewritten, and
  2 regressions caught by the two-pass agreement gate; script sha256s recorded
  and re-verified post-run.
- Evidence: `/root/workspace/work/security-40/058/` (oracle.{md,json},
  js_uci_declares.json, controls.json, provenance.json, run_pipeline.sh,
  pass_{a,b}_*.py/json, evidence_byte_windows.txt, recon_manifest.txt).
  Orchestrator re-ran `run_pipeline.sh` (exit 0, GATE PASS); luci pin clean;
  spot-checked all 7 rpc.declare lines.
