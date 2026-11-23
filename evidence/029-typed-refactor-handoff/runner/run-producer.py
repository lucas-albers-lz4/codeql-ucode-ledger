#!/usr/bin/env python3
"""Fresh setBlockDetect database, diagnostics and typed export; REPO CONSUMER RUN."""
import csv, hashlib, json, os, shutil, subprocess, sys, time
from pathlib import Path
repo, consumer, run = (Path(x).resolve() for x in sys.argv[1:])
run.mkdir(parents=True, exist_ok=False)
pack=repo/'extractor-pack'; codeql=os.environ.get('CODEQL', 'codeql')
env={**os.environ, 'PYTHONDONTWRITEBYTECODE':'1', 'TMPDIR':str(run.parent/'tmp'), 'XDG_CACHE_HOME':str(run.parent/'cache'), 'CODEQL_UCODE_CACHE':str(run.parent/'cache')}
common_cache=run.parent/'common-cache'
compilation_cache=run.parent/'cache/compilation'
assert common_cache.is_dir() and compilation_cache.is_dir()
# HOME is inherited; do not claim it is run-owned.
env.pop('CODEQL_UCODE_STAGED_ROOT',None)
commands=[]
def execute(label, args, *, e=env, output=None, expect=0):
    args=list(map(str,args)); t=time.monotonic()
    p=subprocess.run(['/usr/bin/time','-l',*args],cwd=repo,env=e,capture_output=True)
    (run/(label+'.stdout')).write_bytes(p.stdout); (run/(label+'.stderr')).write_bytes(p.stderr)
    if output is not None: output.write_bytes(p.stdout)
    commands.append({'label':label,'argv':args,'cwd':str(repo),'exit':p.returncode,'wall_seconds':round(time.monotonic()-t,3),'stdout':label+'.stdout','stderr_and_time':label+'.stderr'})
    (run/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
    if p.returncode != expect: raise RuntimeError(f'{label}: exit {p.returncode}, expected {expect}; see log')
    return p

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):
    with p.open(newline='') as f:
        r=csv.DictReader(f); return r.fieldnames,list(r)
def stage(dest, source):
    dest.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(source,dest)
rel='usr/share/rpcd/ucode/luci'
fixture=repo/'ql/test/extractor-smoke'/rel
sibling=repo/'ql/test/effect-controls/setblockdetect/sibling-shadow'/rel
formal=repo/'ql/test/effect-controls/setblockdetect/negative-formal-parameter'/rel
assert sha(fixture)=='6f9d972958d9cfb8a7ba421f38f0a5b03718ffeb0e30d460b64c9faf725fc54e'
assert sha(sibling)=='97353f888f4663bd7cd7b2cf5a7d697121c81d7b88dad3a46ac848646a7c2890'
assert sha(formal)=='14af49d0d4c2653e5e064aa7fd8d9eef357eb5684666c832b0a0b7e1bf567b26'
lock=consumer/'corpus/lock.json'
assert sha(lock)=='b4cbdabb76df90a807aba7d42ae675198c7b7b09c3b84db259a3a4c941b0ea9a'
assert json.loads(lock.read_text())['repos']['luci']['sha']=='b2e0be4b46ec0fd43394c081fa7c50657af14011'
fields=['observation_kind','method','sink_kind','command','source_path','start_line','start_column','end_line','end_column']
common=['callback_body_call','setBlockDetect','system','/sbin/block detect > /etc/config/fstab']
# Expected paths, values and multiplicity are fixed from source and query before database creation.
expectations={'main':[(rel,'532','21','532','68')], 'controls':[(f'modules/sibling/root/{rel}','8','7','8','54'),(f'modules/sibling/root/{rel}','14','5','14','52')]}
(run/'expectations.json').write_text(json.dumps({'fields':fields,'common':common,'rows':expectations,'fixture_sha256':sha(fixture),'sibling_sha256':sha(sibling),'formal_sha256':sha(formal),'lock_sha256':sha(lock)},indent=2)+'\n')
def database(label, inputs, staged):
    base=run/label; src=base/'src'; db=base/'db'
    for name, original in inputs.items(): stage(src/name,original)
    execute(label+'-init',[codeql,'database','init',db,'--language=ucode',f'--search-path={pack}',f'--common-caches={common_cache}',f'--source-root={src}'])
    indexenv=env.copy()
    if staged:indexenv['CODEQL_UCODE_STAGED_ROOT']=str(src)
    execute(label+'-index',[codeql,'database','index-files',db,'--language=ucode','--include=**/rpcd/ucode/luci',f'--working-dir={src}',f'--common-caches={common_cache}'],e=indexenv)
    shutil.copyfile(db/'trap/ucode/routing.json',base/'routing.json')
    routing=json.loads((base/'routing.json').read_bytes())
    counts={'input_count':len(inputs),'plain_count':len(inputs),'markup_count':0,'markup_inconclusive_count':0,'uncertain_count':0,'excluded_count':0,'duplicate_input_count':0}
    wanted=[{'path':str(src/name),'installed_path':rel,'classification':'plain','reason':'rpcd_raw_mode_full_path','status':'plain_route_selected'} for name in inputs]
    assert all(routing.get(k)==v for k,v in counts.items()) and sorted(routing['decisions'],key=lambda d:d['path'])==sorted(wanted,key=lambda d:d['path']),routing
    execute(label+'-finalize',[codeql,'database','finalize',db,f'--common-caches={common_cache}'])
    qlpath=f'{pack}:{repo}/ql/lib:{repo}/ql/src'
    for name,query in [('extracted','diagnostics/SuccessfullyExtractedFiles.ql'),('errors','diagnostics/ExtractionErrors.ql'),('effects','m4/SetBlockDetectEffectTable.ql')]:
        bqrs=base/(name+'.bqrs')
        execute(label+'-'+name+'-query',[codeql,'query','run',repo/'ql/src'/query,f'--database={db}',f'--search-path={qlpath}',f'--common-caches={common_cache}',f'--compilation-cache={compilation_cache}','--no-default-compilation-cache',f'--output={bqrs}','--threads=1','--ram=2048'])
        execute(label+'-'+name+'-decode',[codeql,'bqrs','decode','--format=csv',bqrs],output=base/(name+'.csv'))
    _,extracted=rows(base/'extracted.csv'); _,errors=rows(base/'errors.csv'); gotfields,effects=rows(base/'effects.csv')
    assert all(sha(src/name)==sha(original) for name,original in inputs.items())
    assert len(extracted)==len(inputs) and sorted(r['f'] for r in extracted)==sorted(str(src/p) for p in inputs),extracted
    assert not errors,errors
    expected=[dict(zip(fields,common+list(x))) for x in expectations[label]]
    assert gotfields==fields and sorted(effects,key=lambda x:(x['source_path'],int(x['start_line'])))==sorted(expected,key=lambda x:(x['source_path'],int(x['start_line']))),effects
    return base
main=database('main',{rel:fixture},True)
controls=database('controls',{f'modules/sibling/root/{rel}':sibling,f'modules/formal/root/{rel}':formal},False)
typed=run/'typed.json'
args=[sys.executable,'-B',repo/'tools/export_setblock_detect.py','--csv',main/'effects.csv','--extracted',main/'extracted.csv','--errors',main/'errors.csv','--source-root',main/'src','--lock',lock]
execute('export',args,output=typed)
assert sha(typed)=='5c619d5aa3566c5296080b0a9be7072b38d6eb7a98eae647d68c5dcf09b2b59b'
record=json.loads(typed.read_text()); assert len(record)==1 and record[0]['record_id']=='m4:effect:luci-setBlockDetect-system' and record[0]['assessment']=='unassessed'
with (main/'effects.csv').open(newline='') as f: bad=list(csv.reader(f))
bad[1][5]='533'
with (run/'bad-span.csv').open('w',newline='') as f: csv.writer(f,lineterminator='\n').writerows(bad)
badargs=args.copy(); badargs[badargs.index(main/'effects.csv')]=str(run/'bad-span.csv')
p=execute('export-bad-span',badargs,expect=1); assert not p.stdout
print('main and control identities, diagnostic counts, exact rows and exporter control verified')

for path,digest in ((fixture,'6f9d972958d9cfb8a7ba421f38f0a5b03718ffeb0e30d460b64c9faf725fc54e'),(sibling,'97353f888f4663bd7cd7b2cf5a7d697121c81d7b88dad3a46ac848646a7c2890'),(formal,'14af49d0d4c2653e5e064aa7fd8d9eef357eb5684666c832b0a0b7e1bf567b26'),(lock,'b4cbdabb76df90a807aba7d42ae675198c7b7b09c3b84db259a3a4c941b0ea9a')):
    assert sha(path)==digest, path
