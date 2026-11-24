#!/usr/bin/env python3
"""Recheck MVP corpus source identities against isolated clean checkouts.

This does not verify route decisions, installed package bytes or scan output.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import pathlib
import subprocess
import sys


def git(repo: pathlib.Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(repo), *args], text=True, stderr=subprocess.PIPE
    ).strip()


def source_path(root: pathlib.Path, relative: str) -> pathlib.Path:
    p = pathlib.PurePosixPath(relative)
    if p.is_absolute() or not p.parts or any(part in (".", "..") for part in p.parts):
        raise ValueError(f"unsafe source path: {relative!r}")
    target = root.joinpath(*p.parts)
    if target.is_symlink() or not target.is_file():
        raise ValueError(f"missing, symlinked or non-file source: {relative!r}")
    return target


def verify(manifest: dict, roots: dict[str, pathlib.Path]) -> dict:
    schema = manifest.get("schema")
    if schema not in ("mvp-bounded-corpus-v0.1", "mvp-bounded-corpus-v0.2",
                      "mvp-bounded-corpus-v0.3", "mvp-bounded-corpus-v0.4",
                      "mvp-bounded-corpus-v0.5-source-staged",
                      "mvp-bounded-corpus-v0.6"):
        raise ValueError("unexpected manifest schema")
    pins = manifest["pins"]
    for repo, root in roots.items():
        if git(root, "rev-parse", "HEAD") != pins[repo]:
            raise ValueError(f"{repo} checkout SHA differs from manifest")
        if git(root, "status", "--porcelain=v1"):
            raise ValueError(f"{repo} checkout is dirty")
    selected = manifest["selected"]
    identities = [(r["repo"], r["source_commit"], r["source_path"]) for r in selected]
    if len(set(identities)) != len(identities):
        raise ValueError("duplicate selected source identity")
    excluded = manifest["excluded"]
    excluded_identities = [(r["repo"], pins[r["repo"]], r["source_path"]) for r in excluded]
    expected_excluded = manifest["counts"]["excluded_luci"]
    if schema in ("mvp-bounded-corpus-v0.2", "mvp-bounded-corpus-v0.3",
                  "mvp-bounded-corpus-v0.4", "mvp-bounded-corpus-v0.5-source-staged",
                  "mvp-bounded-corpus-v0.6"):
        expected_excluded += manifest["counts"]["excluded_competing_wifi_shell"]
        expected_excluded += manifest["counts"].get("excluded_optional_prometheus_collectors", 0)
    if (len(excluded) != expected_excluded or
            len(set(excluded_identities)) != len(excluded_identities) or
            set(identities).intersection(excluded_identities)):
        raise ValueError("excluded source identities are missing, duplicate or selected")
    for row in excluded:
        if row["repo"] != "luci" and not (schema in ("mvp-bounded-corpus-v0.2", "mvp-bounded-corpus-v0.3", "mvp-bounded-corpus-v0.4", "mvp-bounded-corpus-v0.5-source-staged", "mvp-bounded-corpus-v0.6") and row["repo"] == "openwrt") and not (schema in ("mvp-bounded-corpus-v0.4", "mvp-bounded-corpus-v0.5-source-staged", "mvp-bounded-corpus-v0.6") and row["repo"] == "packages"):
            raise ValueError("unexpected excluded repository")
        rel = pathlib.PurePosixPath(row["source_path"])
        if rel.is_absolute() or not rel.parts or ".." in rel.parts:
            raise ValueError("unsafe excluded source path")
        path = roots[row["repo"]].joinpath(*rel.parts)
        content = os.readlink(path).encode() if path.is_symlink() else path.read_bytes()
        if hashlib.sha256(content).hexdigest() != row["sha256"]:
            raise ValueError(f"excluded source digest mismatch: {row['source_path']}")
        if row.get("git_blob") and git(roots[row["repo"]], "rev-parse", f"HEAD:{row['source_path']}") != row["git_blob"]:
            raise ValueError(f"excluded Git blob mismatch: {row['source_path']}")
    for row in selected:
        repo = row["repo"]
        if repo not in ("luci", "openwrt", "packages") or row["source_commit"] != pins[repo]:
            raise ValueError(f"unexpected selected source pin: {row}")
        content = source_path(roots[repo], row["source_path"]).read_bytes()
        if hashlib.sha256(content).hexdigest() != row["source_sha256"]:
            raise ValueError(f"source digest mismatch: {repo}:{row['source_path']}")
        blob = git(roots[repo], "rev-parse", f"HEAD:{row['source_path']}")
        if blob != row["git_blob"]:
            raise ValueError(f"Git blob mismatch: {repo}:{row['source_path']}")
    counts = collections.Counter(row["repo"] for row in selected)
    routes = collections.Counter(row["route_support"] for row in selected)
    expected = manifest["counts"]
    if schema == "mvp-bounded-corpus-v0.1":
        expected_counts = collections.Counter({"luci": expected["luci_selected"],
                                               "openwrt": expected["openwrt_selected"]})
        expected_routes = collections.Counter({"plain_route_observed_in_prior_slice": expected["plain_route_observed"],
                                               "markup_inconclusive": expected["markup_inconclusive"]})
        if (len(selected), counts, routes) != (expected["selected"], expected_counts, expected_routes):
            raise ValueError("manifest counts differ from selected identities")
    elif schema not in ("mvp-bounded-corpus-v0.5-source-staged", "mvp-bounded-corpus-v0.6"):
        expected_counts = collections.Counter({"luci": expected["luci_selected"],
                                               "openwrt": expected["openwrt_cli_selected"] + expected["openwrt_wifi_scripts_selected"] + expected.get("openwrt_unetmsg_selected", 0),
                                               "packages": expected.get("packages_prometheus_base_selected", 0)})
        route_classes = collections.Counter(row["expected_route"]["classification"] for row in selected)
        if (len(selected), counts, route_classes, routes["markup_inconclusive"],
                routes["plain_route_observed_in_wifi_slice"],
                routes["plain_route_source_expected_unetmsg"],
                routes["source_expected_prometheus_base"]) != (
                expected["selected"], expected_counts, expected["route_classes"],
                expected["markup_inconclusive"], expected["openwrt_wifi_scripts_selected"],
                expected.get("openwrt_unetmsg_selected", 0),
                expected.get("packages_prometheus_base_selected", 0)):
            raise ValueError("manifest counts differ from selected identities")
    else:
        expected_counts = collections.Counter({
            "luci": expected["luci_selected"],
            "openwrt": expected["openwrt_cli_selected"] + expected["openwrt_wifi_scripts_selected"] + expected.get("openwrt_unetmsg_selected", 0) + expected["openwrt_full_tree_candidates_selected"],
            "packages": expected.get("packages_prometheus_base_selected", 0),
        })
        route_classes = collections.Counter(row["expected_route"]["classification"] for row in selected)
        if (len(selected), counts, route_classes) != (
                expected["selected"], expected_counts, expected["route_classes"]):
            raise ValueError("manifest counts differ from selected identities")
        if routes["source_expected_v0.5_not_yet_run"] != expected.get("openwrt_v0_5_added", expected["openwrt_full_tree_candidates_selected"]):
            raise ValueError("v0.5 source-expected route count differs from selected identities")
        if schema == "mvp-bounded-corpus-v0.6" and routes["source_expected_v0.6_not_yet_run"] != expected["openwrt_v0_6_added"]:
            raise ValueError("v0.6 source-expected route count differs from selected identities")
    return {"selected": len(selected), "luci": counts["luci"],
            "openwrt": counts["openwrt"], "packages": counts["packages"],
            "plain_prior": routes["plain_route_observed_in_prior_slice"],
            "markup_inconclusive": routes["markup_inconclusive"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=pathlib.Path, required=True)
    parser.add_argument("--luci", type=pathlib.Path, required=True)
    parser.add_argument("--openwrt", type=pathlib.Path, required=True)
    parser.add_argument("--packages", type=pathlib.Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    result = verify(manifest, {"luci": args.luci, "openwrt": args.openwrt,
                               "packages": args.packages})
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as exc:
        print(f"source verification failed: {exc}", file=sys.stderr)
        sys.exit(1)
