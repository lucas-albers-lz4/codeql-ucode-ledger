# Bounded event corpus oracle, OpenWrt PR #26933

This local source-only control used the captured PR base
`727d8d2f8e5b19a2121e2cf05824e9e5cac35310` and head
`bce40f6a15c273778061e8fceced7b9e0f58d99b`, whose tree was
`aad77be60ad2931cfc99f6eb49afd7d72843325e`. The checked-out PR head
was clean. The frozen v0.6 source policy digest was
`9c004ed477665f6567a071eac45051445c61019af927bfa4e51bae4c50ebd490`.
The event resolver, full-tree selector and new event manifest generator all
exited zero. The generator re-enumerated the Git objects and required exact
agreement with the retained selector report before writing output.

From the disposable consumer checkout under ignored `work/`:

```sh
python3 -B tools/incoming_event.py ../gate8-event-manifest-run-20261124/event.json ../incoming-live-pr26933-20261124/pull-api-response.json ../incoming-live-pr26933-20261124/source ../incoming-live-pr26933-20261124/control ../gate8-event-manifest-run-20261124/receipt.json
python3 -B tools/full_tree_candidates.py docs/current-corpus-source-v0.6.json openwrt ../incoming-live-pr26933-20261124/source 727d8d2f8e5b19a2121e2cf05824e9e5cac35310 bce40f6a15c273778061e8fceced7b9e0f58d99b ../gate8-event-manifest-run-20261124/inventory.json
python3 -B -m tools.event_corpus_manifest docs/current-corpus-source-v0.6.json ../gate8-event-manifest-run-20261124/receipt.json ../gate8-event-manifest-run-20261124/inventory.json ../incoming-live-pr26933-20261124/source ../gate8-event-manifest-run-20261124/manifest-final.json
```

The source-first output contains 128 selected identities and 13 explicit
exclusions. Its selected installed paths are unique, with 93 plain and 35
markup-inconclusive expected routes. OpenWrt contributes 51 selected files;
the other repositories remain at their frozen source pins. The raw 92 KB
manifest and 193 KB candidate report remain in ignored `work/`; their exact
SHA-256 values, tool versions, checkout states and counts are in
[summary.json](summary.json). This portable summary records the relationship
to raw output and does not claim that another machine can access `work/`.

The disposable consumer branch passed 23 combined event/resolver tests, 14
selector controls, `actionlint`, and `git diff --check`. A separate local
comparison at the exact LuCI, OpenWrt and packages pins found zero route-oracle
disagreements across all 128 selected source bytes. These tests do not verify
release equivalence or hosted manual dispatch.

This is a local oracle preparation, not a CodeQL extraction, released Linux
scan, installed-byte check or producer-to-consumer handoff. Recipe policy
checks compare the frozen policy pin to the event head and are bounded to
selected owners and shared build inputs. The route
oracle names the reviewed producer PR source; equivalence to an eventual
immutable release remains unverified.
