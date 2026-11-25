# Current open OpenWrt PR Ucode path screen (2026-11-25)

## Decision and boundary

This is a bounded changed-file lead inventory for the Gate 8 known-alert
drill. It is not a CodeQL run, a full head-tree or installed-byte inventory,
a clean control, a vulnerability finding, or evidence that no issue exists.
The portable [candidate manifest](candidates.json) records 58 PRs and 83
changed Ucode paths with full head/base commits, GitHub changed-file blob SHA
and status. A removed-file SHA names the removed blob rather than a current
head blob. PRs can move after this non-atomic snapshot; no blob was
independently fetched for semantic proof.

## Collection

At 2026-11-25 03:10:27 UTC, `gh` 2.104.0 and Python 3.15.2 listed the
then-open `openwrt/openwrt` PRs through
`gh api 'repos/openwrt/openwrt/pulls?state=open&per_page=100' --paginate --slurp`.
Seventeen returned pages contained 1,653 distinct PR numbers and full
head/base SHAs. Enumeration was not atomic across pages. An ignored,
resumable script in `work/gate8-openwrt-open-pr-paths-root-20261125/`
requested each PR's changed-file pages with `per_page=100`, two workers and
a 90-second request timeout. All 1,653 requests exited 0. The script selected
paths ending `.uc`, `.ucode`, `.ut`, or containing `/rpcd/ucode/`: 58 PRs had
83 matching changed paths. The largest returned file list contained 1,042
entries. API list limits and the path rule qualify completeness; the path rule can
miss extensionless Ucode installed by a recipe elsewhere.

A second pass fetched patch metadata for all 58 path candidates and re-read
their PR head/base identities. All 58 pairs still matched the first list;
there were no request errors or missing patch bodies. A case-insensitive
textual screen for `request.args`, `popen(`, `system(`, `shellquote`, `fs.exec`
or `exec_direct(` found 12 PRs with a hit in a matching changed-file patch.
This broad token screen is a lead filter, not the CodeQL rule.

Raw API responses, per-PR exits and patch data remain in ignored `work/` on
the collection machine and are not portable. SHA-256 digests of those raw
files are: paginated PR response
`e63592ed6b516106e05ab02c69ea1e01263af87f6ff82383c6ca727e3d5ac3d5`,
normalized PR identity list
`f694a1d4cd38942cfb652411e7135e7a70d49b349506f8b972524d7a4ec9688c`,
file-list summary
`03babbb07e6ead9997c30fa6073c6a796877913a7a5add2a5e80c2aff9b28834`,
and patch-screen summary
`3f38249ee5275a25d2fd5c193f30c02c4d569a1de3558a787d0700b1b7e6ddd4`.
The committed candidate manifest is a small reviewed projection with SHA-256
`f7da0d11afbf6b85e0858ba6c40ebf2890f511f24f8d904b8bfa15437fc5ad0f`.

## Security triage of changed patches

Defensive source review found no eligible **changed-patch** positive among
the 12 textual-hit PRs for the current narrow `DirectRpcShellWord.ql` rule.
The closest lead, OpenWrt #20104, adds
`package/utils/airoha/xpon-agent/files/usr/share/rpcd/ucode/xpon.agent`
at head `68f25b077fe40be020fbfc1bb51c2f2b11be6670`, changed-file blob
`bbf762bb37f8953399d1b7c9efd5b654516491bd`. Its patch has returned RPC
handlers and `request.args` fields but no `popen(` or `system(` sink.
OpenWrt #25175 and #25438 have `fs.popen` in `wireguard.uc` without a
returned RPC handler or `request.args`; #26477 has `fs.popen` argv calls
outside handlers. #23792 quotes a PPP server in `popen` outside an RPC
handler. Other reviewed hits are fixed literals, builtin `system`, or
network/wifi helper calls outside the rule's sink and handler shape.

This patch-level review does not inspect all unchanged files in every head
tree, prove eligibility under the frozen v0.6 selection policy, or authenticate
runtime behavior. No exact positive location is available to predeclare.
The next Gate 8 candidate still requires exact head/base source blobs,
source-derived route and alert oracles, an independent clean control, and a
released Linux producer-to-consumer run.
