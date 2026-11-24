# Incoming discovery live API preflight, 2026-11-24

These six manual, read-only probes used isolated outputs under ignored
`work/incoming-live-20261124-*`, the authenticated public GitHub REST API,
Python 3.15.2 and disposable `codeql-openwrt` poller checkout commits
`9f1172e`, `cfdc277` and `74ed270`. The checkout was clean before the first
probe and between prototype edits. The output directories were new for each
run. This is a failure-boundary record, not an upstream discovery checkpoint,
CodeQL scan or Gate 8 result.

The first 100-item pagination attempt retained five full OpenWrt PR pages;
page six exceeded the 2 MB response cap. The 25-item attempts passed the
per-response bound but twice encountered HTTP 401 after different page
counts. Exact failed endpoints subsequently returned 200 through `gh api`
and a direct authenticated urllib request, so the 401 cause is unresolved.
The fourth attempt retained 25 full 25-item PR pages, then reached the
16 MB encoded-request-history cap before completing OpenWrt pagination. A
fifth probe used the revised discovery-only v2 schema with a 128 MB record
bound and no per-PR tree lookups. It retained 52 full OpenWrt PR pages, then
received an HTTP 504 on page 53. It produced a failure receipt with the
attempted path, status and GitHub request ID, and no checkpoint. Bounded
retry of transient read-only GET failures is under review.
The sixth probe completed OpenWrt PR pagination (67 pages, 1,651 returned
rows) but failed during identity projection because one PR's head repository
was different from the base while GitHub reported `fork: false`. That public
API metadata must be retained as observed; the fork flag alone cannot decide
whether a cross-repository PR is valid. LuCI enumeration did not start and no
complete discovery checkpoint exists.
Independent bounded `gh api` page probes found page 60 full and page 70
empty for OpenWrt, and LuCI page 20 empty; these are time-specific API
observations, not an atomic open-PR count.

Each command exited 2, wrote `failure.json`, and wrote no `decisions.json`.
The retained raw failure receipts remain under ignored `work/` and are not
portable; [summary.json](summary.json) records their hashes, sizes, last
successful paths and explicit limits. The next prototype revision needs a
larger bounded receipt and must avoid a commit/tree API lookup for every
open PR. Discovery should retain full head/base SHA and provenance, with
tree resolution and fresh PR revalidation at selected-event scan time.
