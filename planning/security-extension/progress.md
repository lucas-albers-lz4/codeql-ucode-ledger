# Security extension progress — 2026-11-25

## State

- 091–105 Demonstrated (orchestrator re-ran pipelines, controls 3/3). Wave N (096–101) gated from lanes N1/N2/O; Wave P (105, ASU) gated from openwrt-org sweep.
- Lanes I/J/M hit provider quota after partial artifacts; orchestrator completed 091–094 source oracles from pinned blobs (lane I terminal receipt: quota exit 1; 091/093 pipelines re-run exit 0, controls 3/3). Lane M routing re-measurement still owed.
- Deferred uhttpd resource-lifecycle advisories: lane L decision packet accepted; claims 102–104 Demonstrated from pinned-source census/controls.
- Current-main application-routing re-measurement prompt prepared (lane M); heavy slot not yet acquired.
- No gate lifted; no worker commit/push.

## Log

- 2026-11-25: Reconciled ledger to `origin/main` `ec6e1c1`; verified current-model
  tool-use smoke by independent SHA-256 match. Confirmed eight unused catalog
  advisories. Resolved non-deferred source pins for LXC, adblock-fast, EAD,
  ltq-ptm, and jsonpath; created claims 091–095 and extension plan.
- 2026-11-25: Launched lanes I/J/K (091–095) and L (uhttpd decision). Re-checked
  current-main extractor/query source for #154 and posted two public comments
  (source re-check + 12-backend census). Discovered odhcpd/mdnsd project
  advisories; verified fix ancestry and reserved claims 096–101 (Wave N).
- 2026-11-25: Gated 092 (adblock-fast bounded cron-field chokepoint, setCronEntry
  absent from method table/ACL) and 094 (ltq-ptm CAP_NET_ADMIN + copy_*_user)
  Demonstrated after orchestrator pipeline re-runs; controls 3/3 each.
- 2026-11-25: Gated Wave N 096–101 Demonstrated after orchestrator re-ran all six
  pipelines (exit 0); oracle checks pass, controls 3/3 each, no gate lift/path_found.
- 2026-11-25: openwrt-org sweep (90 repos) found one unclaimed advisory (asu
  GHSA-r3gq-96h6-3v7q). Gated 105 Demonstrated (full request hash + STRING_PATTERN
  package/profile validation + list exec_run); oracle 9/9, controls 3/3.
- 2026-11-25: Lane I (091/093) background process exited 1 on provider quota after
  partial artifacts; orchestrator re-ran both pipelines (exit 0): 091 oracle PASS,
  controls 27/27 (gate 3/3); 093 oracle pass, controls 3/3. Claims remain Demonstrated.
