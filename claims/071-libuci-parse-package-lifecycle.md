# Claim 071: libuci uci_parse_package object lifecycle

- Status: Demonstrated
- Program: [Security-40](../planning/security-40-20261124.md), category H
- Producer: `lucas-albers-lz4/codeql-ucode` (ucode lanes) / `lucas-albers-lz4/codeql-openwrt` (policy, C and JS lanes); pin resolved at execution
- Producer commit: source-oracle pin uci `66127cd76c5d0bd46d5a90302cc6110f53a4e2f8` (no CodeQL run)
- Consumer: `lucas-albers-lz4/codeql-openwrt` where a join is named; otherwise none
- Consumer commit: not yet resolved for this claim
- Environment: local CodeQL CLI 2.27.4 (`gh codeql`), no CI; host details recorded per run

## Historical anchor

- CVE-2020-28951 (UAF via malicious package names, uci_parse_package/uci_strdup)

Anchor role: motivation and source-shape specification only. The claim tests
analyzer observability of the shape at pinned sources; it does not assert the
historical vulnerability is present, exploitable, or patched in any build.

## Bounded question

In pinned libuci file.c/util.c, what is the ownership/lifecycle of package-name strings through uci_parse_package, and is the historical UAF shape observable?

## Method

Source oracle / P1-gated CodeQL C on libuci (resolve pin at execution): transcribe alloc/free/use chains for package names.

## Required evidence

- Lifecycle chain multiset with source lines

## Controls

- Positive: use-after-free chain (if present)
- Near miss: strdup-owned name
- Negative: literal name path

## Out of scope

- No UAF execution
- No full libuci model

## Notes

None.

## Result

Demonstrated (source oracle): FIXED_IN_PIN_NO_ELIGIBLE_INSTANCE WITH census; controls 3/3; gate run_pipeline.sh exit 0. No runtime/exploit/vulnerability verdict; no gate lifted.

fail-no-eligible-instance — FIXED-IN-SOURCE at pin.

The historical UAF shape is a borrow-before-realloc ordering defect: pre-fix uci_parse_package
captured `name = pctx_str(pctx, ofs_name)` BEFORE `assert_eol(ctx)`; assert_eol can fetch more
input (next_arg -> parse_str -> uci_getln -> uci_realloc(pctx->buf)), moving the buffer the
borrow points into; the stale pointer was stored in pctx->name and later read by
uci_switch_config -> uci_alloc_package -> uci_alloc_generic -> uci_strdup(name).

At the pin the ordering is reversed and the name is deep-copied before any realloc can intervene:

    file.c:401  ofs_name = next_arg(ctx, true, true, true);   /* validates: file.c:266 -> util.c:71 */
    file.c:402  assert_eol(ctx);                              /* realloc-capable call BEFORE borrow */
    file.c:403  name = pctx_str(pctx, ofs_name);              /* borrow AFTER (fix a3e6509) */
    file.c:407  ctx->pctx->name = name;
    file.c:408  uci_switch_config(ctx);
    file.c:385  pctx->package = uci_alloc_package(ctx, name);
    list.c:49   e->name = uci_strdup(ctx, name);              /* deep copy -> util.c:59 strdup */

Window scans (independent pass B, brace-tracked function bodies): no realloc-capable call in
(borrow@403, switch@408), and none in the bodies of uci_switch_config, uci_alloc_package,
uci_alloc_generic, uci_strdup. pctx->buf realloc exists only in uci_getln (file.c:54/74). The
owned copy lives in e.name until free(e->name) at list.c:66 via uci_free_package (list.c:248-266),
reached from uci_free_context (libuci.c:85), uci_unload (list.c:754), commit-reload (file.c:775),
or uci_cleanup for unattached packages (libuci.c:142-143; NULL-outs file.c:371/710 prevent double
free). Parse buffer/pctx die at libuci.c:146/148 after import; the name copy is independent.

Census: 124 lifecycle sites across file.c/util.c/list.c/libuci.c; 12 chains; 83 sites cited by
chains + 41 local_only dispositions; uncovered 0. Eligible advisory-family parse-intake chains in
pin bytes: {C01}; UNGUARDED among them: 0. Two independent passes agree exactly on site set,
classes, lifecycle multiset, and ordering facts.

Fix ancestry: a3e6509 "fix heap use after free in uci_parse_package" (2020-10-03) is an ancestor
of the pin; its diff moves the borrow after assert_eol. Related ancestors: eae126f (bounds),
52bbc99 (calloc), 3cda251 (merge import). The 2023 element-update UAF family (9b6605e/47697e6)
is a different site (uci_set/add_list), recorded as context only.
