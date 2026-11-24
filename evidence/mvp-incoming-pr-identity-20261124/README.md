# Live incoming PR identity preflight, 2026-11-24

**Result:** one local identity-only smoke passed. This did not run in hosted
CI, select a dynamic Ucode corpus, run CodeQL, or pass SARIF to the consumer.
It does not satisfy MVP Gate 8.

The resolver was the isolated, clean consumer branch
`c1355ccfd999adc8ac0175981e737c430cb26002`, based on PR #155 head
`82c4aef3a3d2e847df70d34a9700b2488580d740`. Git was 2.56.1. The
run-owned directory under ignored `work/incoming-live-pr26933-20261124`
retains the full API response, event input, source/control Git checkouts and
raw receipt. About 122 GiB of disk was free before fetch. No CodeQL database
or caches were used.

The selected open upstream [OpenWrt PR #26933](https://github.com/openwrt/openwrt/pull/26933)
had a fork head. The exact captured GitHub pull API response SHA-256 is
`e3f2227ef4709d155760f96cc879f7bde12e41ecf2f868b31a48ca7108434f47`.
The input event SHA-256 is
`6e5694b0d196acce8be395e6baef722c2882e54ead43e43b903967b22a629517`.
The source checkout fetched `refs/pull/26933/head` from the canonical
`openwrt/openwrt.git` remote and detached at
`bce40f6a15c273778061e8fceced7b9e0f58d99b` (tree
`aad77be60ad2931cfc99f6eb49afd7d72843325e`). The separate canonical
control checkout detached at
`4e9642517b48bae612ff10fb72fb9199e559500e` (tree
`328d4df01c038d365176b72753b778e10c3ff413`). Both checkouts were
clean after the resolver. The event and API head SHAs agreed; the API head
repository was `Jalakas/openwrt` and its fork flag was true.

The substantive commands, each exiting 0, were:

```sh
gh api repos/openwrt/openwrt/pulls/26933 > work/incoming-live-pr26933-20261124/pull-api-response.json
git -C work/incoming-live-pr26933-20261124/source fetch --depth=1 origin refs/pull/26933/head
git -C work/incoming-live-pr26933-20261124/control fetch --depth=1 origin 4e9642517b48bae612ff10fb72fb9199e559500e
git -C work/incoming-live-pr26933-20261124/source checkout --detach FETCH_HEAD
git -C work/incoming-live-pr26933-20261124/control checkout --detach FETCH_HEAD
python3 -B tools/incoming_event.py ../../work/incoming-live-pr26933-20261124/event.json ../../work/incoming-live-pr26933-20261124/pull-api-response.json ../../work/incoming-live-pr26933-20261124/source ../../work/incoming-live-pr26933-20261124/control ../../work/incoming-live-pr26933-20261124/receipt.json
```

The Python command ran from the isolated consumer checkout. Its
[portable receipt](receipt.json) has SHA-256
`a2c77523049694933021fdf90245ca586ea2434c7792cb3f8258f2273e017441`.
It records `identities_resolved_only` and exact source/control commits and
trees. Wall time and peak memory were not measured for this identity smoke.
The retained local API JSON is a point-in-time response; this receipt does
not authenticate a later moving PR head or a future hosted execution.

The source-policy comparator was then reviewed and corrected twice: shallow
history must not suppress the diff, and ordinary source content changes must
not be classified as coverage drift. Its final clean branch revision was
`3a2197cd087bb5b76e4ffaaa3fe2df3e829a3f55`. The source checkout fetched
the exact captured API base commit
`727d8d2f8e5b19a2121e2cf05824e9e5cac35310` (exit 0), then this command
from the isolated consumer checkout exited 0:

```sh
python3 -B tools/source_policy_drift.py docs/current-corpus-source-v0.4.json openwrt ../incoming-live-pr26933-20261124/source bce40f6a15c273778061e8fceced7b9e0f58d99b 727d8d2f8e5b19a2121e2cf05824e9e5cac35310 ../incoming-live-pr26933-20261124/source-policy-drift.json
```

The [portable drift report](source-policy-drift.json), SHA-256
`b6815c8b6bd28641566ee1c7f3b6af50bd655e08c90b03379e896614456118ee`,
has 34 selected and one excluded OpenWrt baseline identities, 22 content
changes since the historical v0.4 pin, no missing or new candidate path, and
no selected-owner policy drift. It reports the PR's unrelated
`package/utils/bzip2/Makefile` edit separately. Earlier comparator revisions
exited 1 on this PR: first because all 22 old-pin content changes were treated
as coverage drift, then because every package Makefile was treated as a
selected-owner policy input. Those were implementation defects, not findings
about the PR. The final result is still a bounded source-policy preflight;
it does not establish full-tree candidate discovery or a CodeQL scan.
