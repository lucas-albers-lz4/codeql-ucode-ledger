#!/usr/bin/env python3
"""Fresh getBlockDevices extraction and query; run with REPO RUN arguments."""
import csv, hashlib, json, os, shutil, subprocess, sys
from pathlib import Path
repo, run = (Path(p).resolve() for p in sys.argv[1:])
run.mkdir(parents=True, exist_ok=False)
pack = repo / 'extractor-pack'
fixture = repo / 'ql/test/extractor-smoke/usr/share/rpcd/ucode/luci'
columns = ['observation_kind','method','sink_kind','command','source_path','start_line','start_column','end_line','end_column']
common = ['callback_body_call','getBlockDevices','popen','/sbin/block info 2>/dev/null']
log=[]
def execute(args, env=None, output=None):
    args=list(map(str,args)); p=subprocess.run(args,cwd=repo,env=env,capture_output=True)
    log.append({'argv':args,'exit':p.returncode,'stdout':p.stdout.decode(errors='replace'),'stderr':p.stderr.decode(errors='replace')})
    (run/'commands.json').write_text(json.dumps(log,indent=2)+'\n')
    if p.returncode: raise RuntimeError(f'failed: {args}, see commands.json')
    if output: output.write_bytes(p.stdout)
def copy(src,dst):
    dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(src,dst)
def csvrows(path):
    with path.open(newline='') as f:
        reader=csv.DictReader(f); return reader.fieldnames,list(reader)
def make_db(label, staged, files):
    base=run/label; src=base/'src'; db=base/'db'
    for rel, original in files.items(): copy(original,src/rel)
    execute(['codeql','database','init',db,'--language=ucode',f'--search-path={pack}',f'--source-root={src}'])
    env=os.environ.copy(); env.pop('CODEQL_UCODE_STAGED_ROOT',None)
    if staged: env['CODEQL_UCODE_STAGED_ROOT']=str(src)
    execute(['codeql','database','index-files',db,'--language=ucode','--include=**/rpcd/ucode/luci',f'--working-dir={src}'],env)
    shutil.copyfile(db/'trap/ucode/routing.json',base/'routing.json')
    execute(['codeql','database','finalize',db])
    for name, query in [('extracted','diagnostics/SuccessfullyExtractedFiles.ql'),('errors','diagnostics/ExtractionErrors.ql'),('effects','m4/GetBlockDevicesEffectTable.ql')]:
        bqrs=base/(name+'.bqrs')
        execute(['codeql','query','run',repo/'ql/src'/query,f'--database={db}',f'--search-path={pack}:{repo}/ql/lib:{repo}/ql/src',f'--output={bqrs}','--threads=1','--ram=2048'])
        execute(['codeql','bqrs','decode','--format=csv',bqrs],output=base/(name+'.csv'))
    _,extracted=csvrows(base/'extracted.csv'); _,errors=csvrows(base/'errors.csv'); fields,rows=csvrows(base/'effects.csv')
    assert len(extracted)==len(files) and {r['f'] for r in extracted}=={str(src/p) for p in files},extracted
    assert not errors,errors
    assert fields==columns,fields
    return rows
assert hashlib.sha256(fixture.read_bytes()).hexdigest()=='6f9d972958d9cfb8a7ba421f38f0a5b03718ffeb0e30d460b64c9faf725fc54e'
rel='usr/share/rpcd/ucode/luci'
rows=make_db('main',True,{rel:fixture})
expected=dict(zip(columns,common+[rel,'481','18','481','54']))
assert rows==[expected],rows
controls=repo/'ql/test/effect-controls/getblock'
files={f'modules/{name}/root/{rel}':controls/name/rel for name in ('positive','negative-command','negative-import')}
rows=make_db('controls',False,files)
expected=dict(zip(columns,common+[f'modules/positive/root/{rel}','4','5','4','41']))
assert rows==[expected],rows
print('main exact row and three extracted controls verified')
