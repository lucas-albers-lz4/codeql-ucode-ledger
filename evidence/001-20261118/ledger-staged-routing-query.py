"""Extract both layouts and verify real diagnostic and AST entity identities."""
import json
import contextlib
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'extractor-pack'
FIXTURE = ROOT / 'ql/test/extractor-smoke/usr/share/rpcd/ucode/luci'
RELATIVE = Path('usr/share/rpcd/ucode/luci')


def run(*args, env=None):
    return subprocess.run([str(a) for a in args], check=True, text=True, env=env,
                          stdout=subprocess.PIPE).stdout


def verify_extracted(source, extracted):
    rows = extracted['#select']['tuples']
    assert len(rows) == 1, rows
    assert rows[0][0]['url']['uri'] == (source / RELATIVE).as_uri(), rows


def verify(source, receipt, extracted, errors, ast):
    plugin = source / RELATIVE
    decisions = receipt['decisions']
    assert receipt['input_count'] == 1 and receipt['plain_count'] == 1, receipt
    assert receipt['excluded_count'] == receipt['uncertain_count'] == 0, receipt
    assert len(decisions) == 1 and decisions[0] == {
        'path': str(plugin), 'installed_path': str(RELATIVE), 'classification': 'plain',
        'reason': 'rpcd_raw_mode_full_path', 'status': 'plain_route_selected'}, decisions
    verify_extracted(source, extracted)
    assert errors['#select']['tuples'] == [], errors
    target = {'uri': plugin.as_uri(), 'startLine': 17, 'startColumn': 1,
              'endLine': 19, 'endColumn': 1}
    matches = [r for r in ast['#select']['tuples']
               if r[0].get('url') == target and r[1] == 'FunctionDeclaration']
    assert len(matches) == 1, matches


def execute(base, layout, staged):
    source = base / layout
    plugin = source / RELATIVE
    plugin.parent.mkdir(parents=True)
    shutil.copyfile(FIXTURE, plugin)
    if layout == 'src' and not staged:
        # Keep a nonempty database so missing input is tested at the query gate.
        (source / 'control.uc').write_text('let control = 1;\n')
    db = base / 'db'
    run('codeql', 'database', 'init', db, '--language=ucode', f'--search-path={PACK}',
        f'--source-root={source}')
    env = os.environ.copy()
    env.pop('CODEQL_UCODE_STAGED_ROOT', None)
    if staged:
        env['CODEQL_UCODE_STAGED_ROOT'] = str(source)
    run('codeql', 'database', 'index-files', db, '--language=ucode',
        '--include=**/rpcd/ucode/luci', '--include=**/*.uc',
        f'--working-dir={source}', env=env)
    receipt = json.loads((db / 'trap/ucode/routing.json').read_text())
    run('codeql', 'database', 'finalize', db)
    results = []
    for label, query in [('extracted', 'diagnostics/SuccessfullyExtractedFiles.ql'),
                         ('errors', 'diagnostics/ExtractionErrors.ql'),
                         ('ast', 'extractor-smoke/PrintLuciAst.ql')]:
        output = base / (label + '.bqrs')
        run('codeql', 'query', 'run', ROOT / 'ql/src' / query, f'--database={db}',
            f'--search-path={PACK}', f'--output={output}', '--threads=1', '--ram=2048')
        results.append(json.loads(run('codeql', 'bqrs', 'decode', '--format=json',
                                      '--entities=url,string', output)))
    (base / 'routing-retained.json').write_text(json.dumps(receipt, indent=2) + '\n')
    for name, result in zip(('extracted', 'errors', 'ast'), results):
        (base / (name + '.json')).write_text(json.dumps(result, indent=2) + '\n')
    return source, receipt, *results


if __name__ == '__main__':
    root = Path(os.environ['LEDGER_RUN_DIR'])
    data = execute(root / 'ordinary', 'src', True)
    verify(*data)
    print('ordinary: routing, extracted identity, empty errors and AST span verified', flush=True)
