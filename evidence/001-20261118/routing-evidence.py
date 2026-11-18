import json, pathlib, shutil, subprocess
base = pathlib.Path(__file__).resolve().parent
repo = base / 'producer'
run = base / 'direct'
root = run / 'stage'
positive = root / 'usr/share/rpcd/ucode/luci'
outside = run / 'outside/usr/share/rpcd/ucode/luci'
fixture = repo / 'ql/test/extractor-smoke/usr/share/rpcd/ucode/luci'
for f in (positive, outside):
    f.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(fixture, f)
(run / 'inputs').write_text(f'{positive}\n{outside}\n')
cmd = [str(repo / 'extractor-pack/tools/linux64/extractor'), 'extract', '--source-archive-dir', str(run / 'archive'), '--output-dir', str(run / 'trap'), '--file-list', str(run / 'inputs'), '--staged-root', str(root)]
result = subprocess.run(cmd, text=True, capture_output=True)
(run / 'command.json').write_text(json.dumps({'argv':cmd,'exit':result.returncode,'stdout':result.stdout,'stderr':result.stderr}, indent=2)+'\n')
assert result.returncode == 0, result.stderr
receipt = json.loads((run / 'trap/routing.json').read_text())
a, b = receipt['decisions']
assert a['path'] == str(positive) and a['installed_path'] == 'usr/share/rpcd/ucode/luci' and a['reason'] == 'rpcd_raw_mode_full_path' and a['status'] == 'plain_route_selected', a
assert b['path'] == str(outside) and b['reason'] == 'outside_staged_root' and b['status'] == 'excluded', b
assert receipt['plain_count'] == 1 and receipt['excluded_count'] == 1, receipt
assert len(list((run / 'trap').rglob('luci.trap.gz'))) == 1
print('positive selected and outside-root identical fixture excluded; receipt retained')
