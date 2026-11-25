#!/usr/bin/env python3
"""Enumerate .uc/.ut regular members of one pinned luci-base IPK."""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile

LUCI_SHA = "b2e0be4b46ec0fd43394c081fa7c50657af14011"
IPK_SHA = "1a2188f5206ce61c993fdcc451781a06994ae2175b489eef56595858ef22b363"
PREFIX = "./usr/share/ucode/luci/"
SOURCE_PREFIX = "modules/luci-base/ucode/"
VERSION = b"26.284.22350~8125d12"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(source, *args):
    return subprocess.check_output(["git", "-C", str(source), *args], text=True).strip()


def inventory(ipk, source):
    if git(source, "rev-parse", "HEAD") != LUCI_SHA or git(source, "status", "--porcelain=v1"):
        raise ValueError("LuCI checkout pin or dirty status differs")
    raw = ipk.read_bytes()
    if sha(raw) != IPK_SHA:
        raise ValueError("IPK digest differs")
    tracked = set(git(source, "ls-files", SOURCE_PREFIX).splitlines())
    expected = {p[len(SOURCE_PREFIX):] for p in tracked if p.endswith((".uc", ".ut"))}
    if len(expected) != 15:
        raise ValueError("source suffix set differs")
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as outer:
        data_files = [m for m in outer if m.name == "./data.tar.gz" and m.isfile()]
        if len(data_files) != 1:
            raise ValueError("data archive identity differs")
        data = outer.extractfile(data_files[0]).read()
    rows = []
    seen = set()
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as inner:
        for member in inner:
            if not member.name.endswith((".uc", ".ut")):
                continue
            if not member.isfile() or member.name in seen or not member.name.startswith(PREFIX):
                raise ValueError("invalid or duplicate suffix member")
            seen.add(member.name)
            rel = member.name[len(PREFIX):]
            if not rel or any(part in ("", ".", "..") for part in rel.split("/")):
                raise ValueError("unsafe member path")
            blob = inner.extractfile(member).read()
            row = {"installed_path": member.name[2:], "ipk_sha256": sha(blob), "bytes": len(blob)}
            if rel == "version.uc":
                row["class"] = "generated"
                row["content"] = blob.decode("utf-8")
            elif rel in expected:
                source_path = SOURCE_PREFIX + rel
                source_bytes = (source / source_path).read_bytes()
                row.update(source_path=source_path, source_sha256=sha(source_bytes))
                if rel == "template/header.ut":
                    token = b"{# PKG_VERSION #}"
                    if source_bytes.count(token) != 1 or source_bytes.replace(token, VERSION) != blob:
                        raise ValueError("header version substitution differs")
                    row["class"] = "version_substitution"
                else:
                    if source_bytes != blob:
                        raise ValueError("unexpected source-to-IPK byte difference: " + rel)
                    row["class"] = "source_equal"
            else:
                raise ValueError("unexpected suffix member: " + rel)
            rows.append(row)
    if {r["installed_path"][len(PREFIX)-2:] for r in rows if r["class"] != "generated"} != expected:
        raise ValueError("source/IPK identity set differs")
    if sorted(r["class"] for r in rows).count("generated") != 1 or len(rows) != 16:
        raise ValueError("member count differs")
    return {"schema": "luci-base-ipk-suffix-inventory-v1", "luci_commit": LUCI_SHA,
            "ipk_sha256": IPK_SHA, "selection": "all regular .uc/.ut data.tar.gz members",
            "rows": sorted(rows, key=lambda r: r["installed_path"])}


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: verify.py <retained-luci-base.ipk> <clean-luci-checkout>")
    print(json.dumps(inventory(Path(sys.argv[1]), Path(sys.argv[2])), indent=2, sort_keys=True))
