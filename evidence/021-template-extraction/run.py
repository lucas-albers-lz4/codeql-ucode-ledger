#!/usr/bin/env python3
"""Isolated wave 1 extraction runner. Preparation only; invoking it runs CodeQL.

Manifest JSON contract (paths are relative to source_root; relative source_root
is resolved from the manifest directory):
{
  "source_root": "/path/to/staged/source", "expected_input_count": 3,
  "files": [{"path":"usr/share/ucode/luci/a.ut", "sha256":"...",
    "route":{"reason":"markup_not_modeled"},
    "control":"markup_positive|plain_control|corpus|near_miss",
    "expected_extraction":"success|error|either"}]
}
Route fields are compared against matching routing decision fields. Every listed
path must be unique; duplicates in query results are preserved and reported.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlparse


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def die(message):
    raise SystemExit(message)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("producer", type=Path, help="disposable producer checkout")
    ap.add_argument("run_dir", type=Path, help="new, run-owned directory under work/")
    ap.add_argument("manifest", type=Path, help="predeclared source/routing/control oracle")
    ap.add_argument("codeql", type=Path, help="CodeQL executable")
    ap.add_argument("--cache-source", type=Path, required=True,
                    help="read-only CodeQL packages directory copied under isolated HOME")
    a = ap.parse_args()
    producer, run, manifest_path, codeql, cache_source = [p.resolve() for p in
        (a.producer, a.run_dir, a.manifest, a.codeql, a.cache_source)]
    ledger_root = Path(__file__).resolve().parents[2]
    if ledger_root / "work" not in run.parents:
        die("run_dir must be a fresh child of this repository's ignored work/ tree")
    if not (producer / "extractor-pack").is_dir():
        die("producer checkout has no extractor-pack")
    if not codeql.is_file() or not os.access(codeql, os.X_OK):
        die("CodeQL path must name an executable file")
    if not cache_source.is_dir(): die("--cache-source must name an existing directory")
    try:
        manifest = json.loads(manifest_path.read_text())
    except Exception as e:
        die(f"cannot read manifest: {e}")
    staged_root = Path(manifest.get("source_root", ""))
    if not str(staged_root): die("manifest must name source_root")
    if not staged_root.is_absolute(): staged_root = manifest_path.resolve().parent / staged_root
    staged_root = staged_root.resolve()
    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        die("manifest files must be a nonempty list")
    paths = [x.get("path") for x in files]
    if any(not isinstance(p, str) or Path(p).is_absolute() or ".." in Path(p).parts for p in paths):
        die("each manifest path must be a safe relative path")
    if len(paths) != len(set(paths)):
        die("manifest contains duplicate source paths")
    if manifest.get("expected_input_count", len(files)) != len(files):
        die("expected_input_count does not match manifest multiplicity")
    if not any(x.get("control") == "markup_positive" for x in files):
        die("manifest must predeclare a known valid markup_positive control")
    if not any(x.get("control") == "plain_control" for x in files):
        die("manifest must predeclare an eligible plain_control")
    if run.exists():
        die("run directory already exists; use a fresh, exclusively owned path")
    run.mkdir(parents=True)
    source_root = run / "source"
    source_root.mkdir()
    out, db = run / "output", run / "output" / "db"
    out.mkdir()
    home, tmp = run / "home", run / "tmp"
    home.mkdir(); tmp.mkdir()
    cache = run / "cache"
    cache.mkdir()
    packages = home / ".codeql" / "packages"
    packages.parent.mkdir(parents=True)
    shutil.copytree(cache_source, packages, symlinks=True)
    cache_files = sorted(p for p in packages.rglob("*") if p.is_file())
    (run / "cache-copy.json").write_text(json.dumps({"source": str(cache_source),
        "destination": str(packages),
        "files": [{"path": str(p.relative_to(packages)), "sha256": sha256(p)} for p in cache_files]},
        indent=2) + "\n")
    if not staged_root.is_dir():
        die(f"manifest source_root does not exist: {staged_root}")

    # Source-first oracle is persisted before any CodeQL output is examined.
    oracle = []
    for item in files:
        rel = Path(item["path"])
        p = staged_root / rel
        if not p.is_file():
            die(f"manifest source missing: {rel}")
        actual = sha256(p)
        if actual != item.get("sha256"):
            die(f"staged source hash mismatch for {rel}: {actual}")
        target = source_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, target)
        if item.get("control") not in {"markup_positive", "plain_control", "corpus", "near_miss"}:
            die(f"unknown control classification for {rel}")
        if item.get("expected_extraction", "either") not in {"success", "error", "either"}:
            die(f"invalid expected_extraction for {rel}")
        if not isinstance(item.get("route"), dict) or not item["route"]:
            die(f"route expectation must be predeclared for {rel}")
        oracle.append({"path": str(rel), "sha256": actual,
                      "route": item["route"], "control": item["control"],
                      "expected_extraction": item.get("expected_extraction", "either")})
    (out / "source-oracle.json").write_text(json.dumps({"source_root": str(source_root),
        "expected_input_count": len(oracle), "files": oracle}, indent=2) + "\n")

    env = os.environ.copy()
    for key in ("CODEQL_UCODE_STAGED_ROOT", "CODEQL_UCODE_CACHE", "XDG_CACHE_HOME"):
        env.pop(key, None)
    env.update({"HOME": str(home), "TMPDIR": str(tmp), "TMP": str(tmp), "TEMP": str(tmp),
                "XDG_CACHE_HOME": str(cache), "CODEQL_UCODE_CACHE": str(cache),
                "PYTHONDONTWRITEBYTECODE": "1"})
    pack = producer / "extractor-pack"
    qlpath = f"{pack}:{producer / 'ql/lib'}:{producer / 'ql/src'}"
    commands = []

    def call(label, argv, environment=env):
        argv = [str(v) for v in argv]
        start = time.monotonic()
        p = subprocess.run(["/usr/bin/time", "-l", *argv], cwd=producer,
                           env=environment, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        elapsed = time.monotonic() - start
        (out / f"{label}.stdout").write_bytes(p.stdout)
        (out / f"{label}.stderr-time.txt").write_bytes(p.stderr)
        record = {"label": label, "argv": argv, "cwd": str(producer),
                  "exit_status": p.returncode, "wall_seconds": round(elapsed, 6),
                  "stdout": f"{label}.stdout", "stderr_and_time": f"{label}.stderr-time.txt"}
        commands.append(record)
        (out / "commands.json").write_text(json.dumps(commands, indent=2) + "\n")
        return p

    init = call("database-init", [codeql, "database", "init", db, "--language=ucode",
        f"--search-path={pack}", f"--source-root={source_root}"])
    if init.returncode: die(f"database init failed ({init.returncode}); see output/commands.json")
    staged_env = env.copy(); staged_env["CODEQL_UCODE_STAGED_ROOT"] = str(source_root)
    include_args = [f"--include=**/{p}" for p in paths]
    index = call("index-files", [codeql, "database", "index-files", db,
        "--language=ucode", *include_args, f"--working-dir={source_root}"], staged_env)
    if index.returncode: die(f"index-files failed ({index.returncode}); see output/commands.json")

    route_file = db / "trap" / "ucode" / "routing.json"
    if not route_file.is_file(): die(f"routing receipt missing: {route_file}")
    shutil.copyfile(route_file, out / "routing.json")  # intentionally before finalize
    routing = json.loads(route_file.read_text())
    decisions = routing.get("decisions", [])
    route_findings = []
    for expected in oracle:
        full = str(source_root / expected["path"])
        path_matches = [d for d in decisions if d.get("path") == full]
        found = path_matches[0] if len(path_matches) == 1 else None
        ok = found is not None and all(found.get(k) == v for k, v in expected["route"].items())
        route_findings.append({"path": expected["path"], "matched": found, "expected": expected["route"], "matches": ok})
    (out / "routing-comparison.json").write_text(json.dumps(route_findings, indent=2) + "\n")

    fin = call("database-finalize", [codeql, "database", "finalize", db])
    if fin.returncode: die(f"database finalize failed ({fin.returncode}); routing retained")

    def query_decode(label, query):
        bqrs = out / f"{label}.bqrs"
        p = call(label + "-query", [codeql, "query", "run", producer / "ql/src" / query,
            f"--database={db}", f"--search-path={qlpath}", f"--output={bqrs}",
            "--threads=1", "--ram=2048"])
        if p.returncode: die(f"{label} query failed ({p.returncode})")
        d = call(label + "-decode", [codeql, "bqrs", "decode", "--format=json",
            "--entities=url,string", bqrs])
        if d.returncode: die(f"{label} decode failed ({d.returncode})")
        return d.stdout.decode("utf-8", "replace")

    extracted_json = query_decode("extracted", "diagnostics/SuccessfullyExtractedFiles.ql")
    errors_json = query_decode("errors", "diagnostics/ExtractionErrors.ql")
    local_query = producer / "ql/src" / "Wave1AllDiagnostics.ql"
    local_query_text = '''/** Wave 1 ledger-local all-diagnostics inventory; not an upstream query. */
import codeql.ucode.Diagnostics
import codeql.files.FileSystem

string diagnosticPath(Diagnostic d) {
  exists(File f | f = d.getLocation().getFile() and result = f.getRelativePath())
  or exists(File f | f = d.getLocation().getFile() and
    not exists(f.getRelativePath()) and result = f.getAbsolutePath())
  or
  not exists(File f | f = d.getLocation().getFile()) and result = "<unattributed>"
}
int diagnosticLine(Diagnostic d) {
  exists(int n | n = d.getLocation().getStartLine() and result = n)
  or not exists(int n | n = d.getLocation().getStartLine()) and result = -1
}
int diagnosticColumn(Diagnostic d) {
  exists(int n | n = d.getLocation().getStartColumn() and result = n)
  or not exists(int n | n = d.getLocation().getStartColumn()) and result = -1
}
string diagnosticSeverityText(Diagnostic d) {
  exists(string s | s = d.getSeverityText() and result = s)
  or not exists(string s | s = d.getSeverityText()) and result = "<unknown-severity-text>"
}
from Diagnostic d
select d, diagnosticPath(d), diagnosticLine(d), diagnosticColumn(d),
  d.getSeverity(), diagnosticSeverityText(d), d.getTag(), d.getMessage()
'''
    if local_query.exists():
        if local_query.read_text() != local_query_text:
            die(f"refusing to overwrite different local query: {local_query}")
    else:
        local_query.write_text(local_query_text)
    diag_bqrs = out / "all-diagnostics.bqrs"
    dq = call("all-diagnostics-query", [codeql, "query", "run", local_query,
        f"--database={db}", f"--search-path={qlpath}", f"--output={diag_bqrs}",
        "--threads=1", "--ram=2048"])
    if dq.returncode: die(f"all-diagnostics query failed ({dq.returncode})")
    dd = call("all-diagnostics-decode", [codeql, "bqrs", "decode", "--format=json",
        "--entities=url,string", diag_bqrs])
    if dd.returncode: die(f"all-diagnostics decode failed ({dd.returncode})")
    diagnostics_json = dd.stdout.decode("utf-8", "replace")
    (out / "extracted.json").write_text(extracted_json)
    (out / "errors.json").write_text(errors_json)
    (out / "all-diagnostics.json").write_text(diagnostics_json)

    def tuple_rows(raw):
        root = json.loads(raw)
        found = []
        def visit(node):
            if isinstance(node, dict):
                tuples = node.get("tuples")
                if isinstance(tuples, list): found.extend(tuples)
                else:
                    for value in node.values(): visit(value)
            elif isinstance(node, list):
                for value in node: visit(value)
        visit(root)
        return found

    def as_scalar(value):
        if isinstance(value, (str, int, float)): return value
        if isinstance(value, dict):
            return value.get("label", value.get("value", value.get("url")))
        return None

    def exact_file_url(value):
        """Extract a file entity URL; never infer identity from unrelated columns."""
        candidates = []
        def visit(node):
            if isinstance(node, dict):
                url = node.get("url")
                if isinstance(url, str): candidates.append(url)
                for child in node.values(): visit(child)
            elif isinstance(node, list):
                for child in node: visit(child)
        visit(value)
        for url in candidates:
            parsed = urlparse(url)
            if parsed.scheme == "file": return Path(unquote(parsed.path)).as_posix()
            if Path(url).is_absolute(): return Path(url).as_posix()
        # Some decoders encode the selected File entity as a bare URL string.
        scalar = as_scalar(value)
        if isinstance(scalar, str):
            parsed = urlparse(scalar)
            if parsed.scheme == "file": return Path(unquote(parsed.path)).as_posix()
            if Path(scalar).is_absolute(): return Path(scalar).as_posix()
        return None

    def exact_entity_url(value):
        urls = []
        def visit(node):
            if isinstance(node, dict):
                if isinstance(node.get("url"), str): urls.append(node["url"])
                for child in node.values(): visit(child)
            elif isinstance(node, list):
                for child in node: visit(child)
        visit(value)
        return urls[0] if urls else (value if isinstance(value, str) and ":" in value else None)

    extracted_rows = tuple_rows(extracted_json)
    error_rows = tuple_rows(errors_json)
    diagnostic_rows = tuple_rows(diagnostics_json)
    # Producer successful-file query selects File as its first entity column.
    extracted_ids = [exact_file_url(row[0]) for row in extracted_rows if row]
    extracted_ids = [x for x in extracted_ids if x]
    # Diagnostics query emits its Diagnostic entity first; file path comes from
    # its location column, which is explicit and includes <unattributed>.
    def diag_value(row, index): return as_scalar(row[index]) if len(row) > index else None
    file_rows = [row for row in diagnostic_rows if len(row) >= 8]
    error_details = [{"diagnostic_url": exact_entity_url(row[0]),
                      "path": diag_value(row, 1), "line": diag_value(row, 2),
                      "column": diag_value(row, 3), "severity_numeric": diag_value(row, 4),
                      "severity": diag_value(row, 5), "tag": diag_value(row, 6),
                      "message": diag_value(row, 7)}
                     for row in file_rows if diag_value(row, 6) == "parse_error"]
    error_ids = [str(x["path"]) for x in error_details if x["path"] not in (None, "<unattributed>")]
    source_prefix = source_root.as_posix().rstrip("/") + "/"
    error_ids = [x[len(source_prefix):] if x.startswith(source_prefix) else x for x in error_ids]
    producer_error_urls = [exact_entity_url(row[0]) for row in error_rows if row]
    diagnostic_error_urls = [x["diagnostic_url"] for x in error_details]
    parse_error_urls_match = Counter(producer_error_urls) == Counter(diagnostic_error_urls)
    locationless = [row for row in file_rows if diag_value(row, 1) == "<unattributed>"]
    def count_for(rel, ids):
        exact = (source_root / rel).as_posix() if ids is extracted_ids else rel
        return sum(1 for x in ids if x == exact)
    results = []
    for item in oracle:
        n_ok = count_for(item["path"], extracted_ids)
        n_err = count_for(item["path"], error_ids)
        expected = item["expected_extraction"]
        extraction_outcome = ("success" if n_ok == 1 and n_err == 0 else
                              "parse_error" if n_ok == 0 and n_err > 0 else "unknown")
        checks = {"route_matches": next(x["matches"] for x in route_findings if x["path"] == item["path"]),
                  "success_multiplicity": n_ok, "error_multiplicity": n_err,
                  "observed_extraction": extraction_outcome,
                  "expected_extraction": expected,
                  "extraction_expectation_matches": (expected == "either" and extraction_outcome != "unknown" or
                    expected == "success" and n_ok == 1 and n_err == 0 or
                    expected == "error" and n_err > 0 and n_ok == 0),
                  "positive_or_control_clean": item["control"] not in {"markup_positive", "plain_control"} or (n_ok == 1 and n_err == 0)}
        results.append({"path": item["path"], "control": item["control"], **checks})
    # Verify bytes again after extraction to catch accidental staging mutation.
    changed = [x["path"] for x in oracle if sha256(source_root / x["path"]) != x["sha256"]]
    expected_extracted_ids = []
    for item, observed in zip(oracle, results):
        if item["expected_extraction"] == "success" or (
            item["expected_extraction"] == "either" and observed["observed_extraction"] == "success"):
            expected_extracted_ids.append((source_root / item["path"]).as_posix())
    expected_ids = [(source_root / x["path"]).as_posix() for x in oracle]
    expected_route_paths = [str(source_root / x["path"]) for x in oracle]
    actual_route_counts = Counter(d.get("path") for d in decisions)
    unexpected_routes = {k: v for k, v in actual_route_counts.items() if k not in expected_route_paths}
    missing_or_duplicate_routes = {k: v for k, v in Counter(expected_route_paths).items()
                                   if actual_route_counts[k] != v}
    extracted_counts = Counter(extracted_ids)
    unexpected_extracted = {k: v for k, v in extracted_counts.items() if k not in expected_ids}
    missing_or_wrong = {k: v for k, v in Counter(expected_extracted_ids).items() if extracted_counts[k] != v}
    def manifest_relative(path):
        if path in [x["path"] for x in oracle]: return path
        full = (source_root / path).as_posix()
        return next((x["path"] for x in oracle if (source_root / x["path"]).as_posix() == full), None)
    normalized_errors = [manifest_relative(path) or path for path in error_ids]
    errors_outside_manifest = {k: v for k, v in Counter(normalized_errors).items()
                               if k not in [x["path"] for x in oracle]}
    diagnostics_by_file = {x["path"]: [row for row in file_rows
        if diag_value(row, 1) == x["path"]] for x in oracle}
    unattributed_rows = [row for row in file_rows if diag_value(row, 1) == "<unattributed>"]
    report = {"source_hashes_unchanged": not changed, "changed_paths": changed,
              "routing_input_count": routing.get("input_count"),
              "routing_input_count_matches_manifest": routing.get("input_count") == len(oracle),
              "routing_decision_count": len(decisions), "files": results,
              "extracted_identity_multiplicity": dict(extracted_counts),
              "error_identity_multiplicity": dict(Counter(error_ids)),
              "producer_error_entity_urls": producer_error_urls,
              "diagnostic_error_entity_urls": diagnostic_error_urls,
              "producer_and_supplemental_error_urls_match": parse_error_urls_match,
              "parse_error_diagnostics": error_details,
              "errors_outside_manifest": errors_outside_manifest,
              "unexpected_extracted_identities": unexpected_extracted,
              "missing_or_wrong_extracted_multiplicity": missing_or_wrong,
              "unexpected_routing_paths": unexpected_routes,
              "missing_or_duplicate_routing_paths": missing_or_duplicate_routes,
              "diagnostics_by_file": diagnostics_by_file,
              "all_diagnostic_rows": len(diagnostic_rows),
              "locationless_diagnostics": locationless,
              "unattributed_diagnostics": unattributed_rows,
              "all_checks_match": not changed and not unexpected_extracted and not missing_or_wrong and
                  not unexpected_routes and not missing_or_duplicate_routes and
                  routing.get("input_count") == len(oracle) and
                  not errors_outside_manifest and parse_error_urls_match and
                  not locationless and not unattributed_rows and all(x["route_matches"] and
                  x["extraction_expectation_matches"] and x["positive_or_control_clean"] for x in results)}
    (out / "verification.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"run_dir": str(run), "verification": str(out / "verification.json"),
                      "all_checks_match": report["all_checks_match"]}))
    return 0 if report["all_checks_match"] else 2


if __name__ == "__main__":
    sys.exit(main())
