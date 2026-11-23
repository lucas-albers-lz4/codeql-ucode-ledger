from pathlib import Path
import collections
import csv
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import zipfile

root = Path(__file__).resolve().parent
source = root / 'source'
output = root / 'output'
database = root / 'database/db'
extractor_pack = root / 'extractor-pack'
oracle = json.loads((root / 'source-first-oracle.json').read_text())
route_oracle = json.loads((root / 'source-first-routing.json').read_text())
cli = root / 'bin/codeql'
environment = os.environ.copy()
for key in ('TMPDIR', 'TMP', 'TEMP'):
    environment[key] = str(root / 'tmp')
environment['XDG_CACHE_HOME'] = str(root / 'cache/xdg')
environment['PYTHONDONTWRITEBYTECODE'] = '1'

def run(*args, env=environment):
    proc = subprocess.run([cli, *args], env=env, cwd=root, stdout=subprocess.PIPE, check=True)
    return proc.stdout

def file_sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check_sources():
    for fixture in route_oracle['files']:
        p = source / fixture['path']
        assert file_sha(p) == fixture['sha256'] and p.stat().st_size == fixture['size_bytes'], fixture
        assert fixture['sha256'] == oracle['expectations'][p.name]['sha256'], fixture

def query(relpath, fmt='csv'):
    q = root / 'ql/src' / relpath
    bqrs = output / f'{q.stem}.bqrs'
    run('query', 'run', q, f'--database={database}', f'--search-path={extractor_pack}',
        f'--output={bqrs}', '--threads=1', '--ram=2048')
    payload = run('bqrs', 'decode', f'--format={fmt}', '--entities=url,string', bqrs)
    (output / f'{q.stem}.{fmt}').write_bytes(payload)
    if fmt == 'json':
        return json.loads(payload)['#select']['tuples']
    return [tuple(row) for row in list(csv.reader(io.StringIO(payload.decode())))[1:]]

def main():
    check_sources()
    if sys.argv[1:] == ["--resume-queries"]:
        assert (database / "codeql-database.yml").is_file()
        assert (output / "routing.json").is_file()
    else:
        assert not database.exists()
        (root / 'logs/preflight.json').write_text(json.dumps({
            'base_sha': oracle['base_sha'], 'grammar_sha': oracle['grammar_sha'],
            'source_and_oracle_sha256': {str(p.relative_to(root)): file_sha(p)
                for p in [*source.rglob('*.ut'), *root.glob('source-first-*.json')]},
            'project_locks_sha256': {str(p.relative_to(root)): file_sha(p)
                for p in root.glob('ql/*/codeql-pack.lock.yml')},
            'pack_sha256': {str(p.relative_to(root)): file_sha(p)
                for p in extractor_pack.rglob('*') if p.is_file()},
            'free_disk_bytes': shutil.disk_usage(root).free,
            'home_set_by_run': False,
            'database': str(database), 'tmpdir': environment['TMPDIR'],
            'common_cache': str(root / 'common-cache'),
        }, indent=2) + '\n')
        run('database', 'init', database, '--language=ucode', f'--search-path={extractor_pack}',
            f'--source-root={source}')
        index_environment = {**environment, 'CODEQL_UCODE_STAGED_ROOT': str(source)}
        run('database', 'index-files', database, '--language=ucode', f'--working-dir={source}',
            *[f'--include=**/{f}' for f in oracle['expectations']], env=index_environment)
        shutil.copyfile(database / 'trap/ucode/routing.json', output / 'routing.json')
        run('database', 'finalize', database)
    comparisons = {}
    def compare(label, actual, expected):
        actual = collections.Counter(actual)
        expected = collections.Counter(expected)
        comparisons[label] = {'pass': actual == expected,
                              'actual_count': actual.total(), 'expected_count': expected.total(),
                              'missing': list((expected - actual).elements()),
                              'unexpected': list((actual - expected).elements())}
    routing = json.loads((output / 'routing.json').read_text())
    counts = route_oracle['expected_routing_counts']
    compare('routing_counts', ((k, routing.get(k)) for k in counts), counts.items())
    route_keys = ('classification', 'reason', 'status', 'inconclusive_reason')
    compare('routing_decisions',
        [(d.get('installed_path'), *(d.get(k) for k in route_keys)) for d in routing['decisions']],
        [(f['path'], *(f['route'][k] for k in route_keys)) for f in route_oracle['files']])
    success = query('diagnostics/SuccessfullyExtractedFiles.ql', 'json')
    compare('successful_files', [(row[0]['url']['uri'], row[1]) for row in success],
        [((source / f['path']).as_uri(), '') for f in route_oracle['files']])
    compare('extraction_errors', (json.dumps(row, sort_keys=True) for row in query('diagnostics/ExtractionErrors.ql', 'json')), [])
    compare('file_diagnostics', query('markup-cfg-diagnostics-test.ql'), [])
    with zipfile.ZipFile(database / 'src.zip') as archive:
        archived_files = [name for name in archive.namelist() if not name.endswith('/')]
        actual_source = [(name, hashlib.sha256(archive.read(name)).hexdigest())
                         for name in archived_files]
    compare('source_archive_bytes', actual_source,
        [(str(source / f['path']).lstrip('/'), f['sha256']) for f in route_oracle['files']])
    ast, cov, nodes, edges = [], [], [], []
    roles = {'RawText': 'raw-text', 'Identifier': 'identifier', 'ExpressionTag': 'tag-completion'}
    for name, data in oracle['expectations'].items():
        ast.extend(map(tuple, data['ast']))
        cov.append((name, 'covered' if data['coverage'] else 'unsupported'))
        for ident in data['graph_path']:
            nodes.append((name, roles.get(ident.split(':')[0], ident), ident, '1'))
        edges.extend((name, a, b, '1') for a, b in data['edge_pairs'])
    compare('ast_identity_and_field_multiplicity', query('markup-cfg-delimiters-ast-test.ql'), ast)
    compare('coverage', query('markup-cfg-delimiters-coverage-test.ql'), cov)
    compare('nodes', query('markup-cfg-nodes-test.ql'), nodes)
    compare('edges', query('markup-cfg-test.ql'), edges)
    check_sources()
    (output / 'oracle-comparison.json').write_text(json.dumps(comparisons, indent=2) + '\n')
    print(json.dumps(comparisons, indent=2))
    assert all(v['pass'] for v in comparisons.values())

if __name__ == '__main__':
    main()
