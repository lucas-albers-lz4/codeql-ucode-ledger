# Application source and catalog inventory for OpenWrt #151

These independently reviewed, source-first observations cover the seven named application backends and 13 associated object/method candidates. [Six backends](SIX-BACKENDS.md) record 12 exact ACL declarations and [Dockerman](DOCKERMAN.md) records one candidate associated with wildcard ACL entries. DDNS `get_services_log` is not repeated. These are source relationships, not effect joins or evidence of call binding, runtime behavior, installed packages, effective grants, authorization or security coverage. OpenWrt [#151](https://github.com/lucas-albers-lz4/codeql-openwrt/issues/151) remains open and gated by the applicable producer scope, models and owner decisions; this packet changes no claim status. No CodeQL execution was performed for this inventory. Historical claims [043](../../claims/043-ucode-app-fs-exec-argv.md), [047](../../claims/047-ucode-request-path-read.md), and [051](../../claims/051-ucode-request-path-write.md) retain their own scope and limits.

The source pin is [LuCI `b2e0be4b46ec0fd43394c081fa7c50657af14011`](https://github.com/openwrt/luci/tree/b2e0be4b46ec0fd43394c081fa7c50657af14011/applications). The source and ACL paths and exact blob and SHA-256 identities are in the two documents. Each source is under `applications/luci-app-<package>/root/usr/share/rpcd/ucode/`, and each ACL under the same package's `root/usr/share/rpcd/acl.d/`. Package names are ddns, dockerman, example, rustdesk-server, tailscale-community, weechat, and wifihistory; backend filenames are respectively ddns.uc, docker_rpc.uc, example.uc, rustdesk-server.uc, tailscale.uc, weechat.uc, and wifihistory.uc. Source hashes can be checked on a clone containing the pin with `git show "$pin:$path" | shasum -a 256` and blobs with `git rev-parse "$pin:$path"`. The staged seven files were compared to the pinned Git bytes; this does not establish installed package bytes. A textual scan over those exact seven files used `rg -n '\b(exec_direct|exec|popen|system)\s*\(' <seven-files>`; its full hit inventory and limitations are in the documents. The seven-file source manifest had SHA-256 `aa73b3d266e8687581476de97294205708ed292650d162c19e22e5bd6d031fc1`.

The [consumer catalog](https://github.com/lucas-albers-lz4/codeql-openwrt/blob/a1c9875575814329e5abdc70bc36e30f5ef0b987/policy/grants.json) is at consumer `a1c9875575814329e5abdc70bc36e30f5ef0b987`, Git blob `47a522fa080acd554e7fa941ec4ad8f7a94efd54`, SHA-256 `b34cdc9b9403c0ca21761ca340d6840e2b23f522486c4d6f7e139a4fa77b12bc`; corpus lock digest is `b4cbdabb76df90a807aba7d42ae675198c7b7b09c3b84db259a3a4c941b0ea9a`. An independent reviewer checked the commit/blob mapping via GitHub GraphQL, all seven source and ACL identities, scan hits, 13 candidates and catalog rows. Full scan of its 110 rows found no exact object/method match for any of the 13 candidates. This is a catalog snapshot observation; wildcard interpretation and grants elsewhere remain unresolved.

To reproduce the catalog comparison from these portable inputs, obtain the catalog bytes at the pinned commit and run:

```sh
shasum -a 256 grants.json
python3 - <<'PY'
import json
rows = json.load(open('grants.json'))
pairs = [('docker.container','ttyd_start'),
 ('luci.ddns','get_services_status'), ('luci.ddns','get_ddns_state'), ('luci.ddns','get_env'),
 ('luci.rustdesk-server','get_version'), ('tailscale','get_status'), ('tailscale','get_subroutes'),
 ('tailscale','set_settings'), ('tailscale','do_login'), ('tailscale','do_logout'),
 ('tailscale','setup_firewall'), ('weechat','get_daemon_info'), ('weechat','generate_certificate')]
print('rows', len(rows))
for obj, method in pairs:
    matches = [r for r in rows if r.get('ubus_object') == obj and r.get('method') == method]
    print(obj, method, len(matches))
PY
```

The original reviewed scratch inputs had SHA-256 `7c95381624594a4512e8193203a7dda846f18e626b8dc749d4dc72961529b3cb` (Dockerman) and `0efc1d0ca9e0cb4c61b00e559a0d04fb756683c6420eb0756467aeab677c8c72` (six backends). The copied documents replace workspace-specific paths with portable descriptions; their observations are unchanged.
