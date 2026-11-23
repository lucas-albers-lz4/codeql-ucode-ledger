#!/usr/bin/env python3
"""Package 6 isolated run. Inspect and validate before invoking; no HOME override."""
import collections, csv, datetime, hashlib, json, os, pathlib, shutil, subprocess, sys, time
from expected import expected
P = pathlib.Path(__file__).resolve().parent
LEDGER = P.parents[2]
SRC = LEDGER/'work/pkg1-codeql-ucode'
OLD = LEDGER/'work/cfg-trim-oracle/run-20261122-a'
CODEQL = LEDGER.parent/'.tools/codeql-2.27.4/codeql/codeql'
PIN = '6010ff2c0f101f7629c6fe117a421f671c311a2b'
FIXTURES = {'siblings.ut':'940472ed365ba3c40aed4b42427ca703c05ece028069e696eb98d850808d7d16', 'siblings-all-covered.ut':'885ea36bf4edfa571a860c0226642a491b007f40d58ca8ed660a7bea2a46fb23'}
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def tree(p): return {str(x.relative_to(p)): h(x) for x in sorted(p.rglob('*')) if x.is_file() and not x.is_symlink()}
def dump(p,x): p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def run():
 if len(sys.argv)!=2: raise RuntimeError('supply a new unique run path beneath work/')
 run=pathlib.Path(sys.argv[1]).resolve(); work=(LEDGER/'work').resolve()
 if not run.is_relative_to(work) or run.exists(): raise RuntimeError('run must be new and beneath work/')
 run.mkdir(); log=run/'logs'; out=run/'output'; tmp=run/'tmp'; cache=run/'cache'; common=run/'common-cache'; source=run/'source'; pack=run/'pack'; ql=run/'producer-ql'; db=run/'database/db'
 for p in (log,out,tmp,db.parent,cache/'compilation',common,source,pack,ql): p.mkdir(parents=True,exist_ok=True)
 env=dict(os.environ,TMPDIR=str(tmp),TMP=str(tmp),TEMP=str(tmp),XDG_CACHE_HOME=str(cache),CODEQL_UCODE_CACHE=str(cache),PYTHONDONTWRITEBYTECODE='1'); env.pop('CODEQL_UCODE_STAGED_ROOT',None)
 commands=[]
 def invoke(label,args,extra=None):
  en=env.copy(); en.update(extra or {}); argv=list(map(str,args)); start=time.monotonic(); proc=subprocess.run(['/usr/bin/time','-l',*argv],cwd=run,env=en,capture_output=True); elapsed=time.monotonic()-start
  (out/(label+'.stdout')).write_bytes(proc.stdout); (out/(label+'.stderr-time.txt')).write_bytes(proc.stderr)
  commands.append({'label':label,'argv':argv,'cwd':str(run),'exit':proc.returncode,'elapsed_seconds':elapsed,'stdout':label+'.stdout','stderr_time':label+'.stderr-time.txt'}); dump(log/'commands.json',commands)
  if proc.returncode: raise RuntimeError(label+' failed; see stderr-time')
  return proc.stdout
 def check(label,actual,expected):
  a=collections.Counter(map(tuple,actual)); e=collections.Counter(map(tuple,expected)); dump(out/('assert-'+label+'.json'),{'passed':a==e,'actual':actual,'expected':expected});
  if a!=e: raise AssertionError(label)
 try:
  # Never start a heavy run concurrently. Record process state; fail closed instead of waiting.
  ps=subprocess.run(['ps','-ax','-o','pid=,etime=,command='],capture_output=True,text=True,check=True); heavy=[x for x in ps.stdout.splitlines() if ('/codeql/codeql ' in x or 'com.semmle.cli2.CodeQL' in x) and 'ps -ax' not in x]
  dump(log/'process-preflight.json',{'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'codeql_processes':heavy});
  if heavy: raise RuntimeError('live CodeQL process detected; abort without retry')
  def git(*args): return subprocess.check_output(['git','-C',str(SRC),*args],text=True).strip()
  if git('rev-parse','HEAD')!=PIN or git('status','--porcelain=v1'): raise RuntimeError('producer pin/clean preflight failed')
  prev=json.loads((OLD/'preparation.json').read_text()); prior_sha=prev['pack_source_build_revision']
  delta=git('diff','--name-only',prior_sha,PIN,'--','extractor','extractor-pack','Cargo.toml','Cargo.lock','codeql-extractor.yml','.codeqlmanifest.json','ql/src/qlpack.yml','ql/src/codeql-pack.lock.yml','ql/lib/qlpack.yml','ql/lib/codeql-pack.lock.yml','scripts/create-extractor-pack.sh','scripts/clone-grammar.sh','ql/lib/ucode.dbscheme','ql/lib/ucode.dbscheme.stats','ql/lib/codeql/ucode/ast/internal/TreeSitter.qll','tools','downgrades')
  if delta: raise RuntimeError('pack source changed since build: '+delta)
  if h(CODEQL)!=prev['codeql_sha256']: raise RuntimeError('CodeQL binary digest differs from reuse provenance')
  lock={x:h(SRC/x) for x in ('ql/lib/codeql-pack.lock.yml','ql/src/codeql-pack.lock.yml')}
  if lock!=prev['lock_digests']: raise RuntimeError('QL lock digest mismatch')
  # Verify retained grammar checkout and bootstrap transformation against build record.
  grammar=LEDGER/'work/typed-20261121/producer/extractor/tree-sitter'
  ghead=subprocess.check_output(['git','-C',str(grammar),'rev-parse','HEAD'],text=True).strip()
  gstatus=subprocess.check_output(['git','-C',str(grammar),'status','--porcelain=v1'],text=True).strip()
  gdiff=subprocess.check_output(['git','-C',str(grammar),'diff','--','Cargo.toml'],text=True)
  if ghead!='4a243af329fae2f4ff01e0fc80133cbab8314600' or gstatus!='M Cargo.toml' or '-tree-sitter = "0.27.1"' not in gdiff or '+tree-sitter = "=0.26.8"' not in gdiff: raise RuntimeError('grammar provenance mismatch')
  build_log=LEDGER/'work/typed-20261121/build-offline.log'
  if 'Finished `release`' not in build_log.read_text(): raise RuntimeError('offline build completion missing')
  # Verify reused installed pack against independently retained build manifest.
  build=json.loads((LEDGER/'work/wave10-ast-run/preparation-manifest.json').read_text())
  pack_source=OLD/'pack/ucode-extractor-pack'
  build_files={x['path']:x['sha256'] for x in build['source_pack_files'] if x.get('sha256')}
  if tree(pack_source)!=build_files: raise RuntimeError('installed pack differs from retained build manifest')
  # Dependencies must come from retained package source, not a mutated common cache.
  cache_source=LEDGER/'work/wave10-ast-run/home/.codeql/packages'
  if tree(cache_source)!=tree(OLD/'common-cache/packages'): raise RuntimeError('common cache differs from retained dependency source; inspect layout and provenance')
  # Copy package 4 owned copies, then compare all file hashes. Never share writable paths.
  for origin,dest in ((OLD/'pack/ucode-extractor-pack',pack/'ucode-extractor-pack'),(OLD/'common-cache',common),(SRC/'ql',ql/'ql')):
   shutil.copytree(origin,dest,dirs_exist_ok=True,symlinks=True)
   if tree(origin)!=tree(dest): raise RuntimeError('copy digest mismatch '+str(origin))
  shutil.copy2(SRC/'.codeqlmanifest.json',ql/'.codeqlmanifest.json')
  for filename,expected_digest in FIXTURES.items():
   src=P.parent/filename
   if h(src)!=expected_digest: raise RuntimeError('fixture mismatch '+filename)
   target=source/'usr/share/ucode/controls'/filename; target.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(src,target)
  for query in (P/'queries').glob('*.ql'): shutil.copy2(query,ql/'ql/src'/('pkg6-'+query.name))
  shutil.copy2(OLD/'producer-ql/ql/src/pkg4-diagnostics.ql',ql/'ql/src/pkg6-diagnostics.ql')
  dump(log/'preflight.json',{'producer':PIN,'producer_dirty':False,'pack_build_revision':prior_sha,'grammar_revision':ghead,'grammar_status':gstatus,'grammar_diff_sha256':hashlib.sha256(gdiff.encode()).hexdigest(),'build_log_sha256':h(build_log),'build_toolchain':'Cargo 1.100.0 recorded in claim 008; retained target rustc metadata references 1.100.0 but build-time rustc invocation was not separately logged','pack_source_manifest':tree(OLD/'pack/ucode-extractor-pack'),'pack_copied_manifest':tree(pack/'ucode-extractor-pack'),'common_cache_manifest':tree(common),'locks':lock,'fixtures':FIXTURES,'codeql_sha256':h(CODEQL),'home_inherited':True,'tmp':str(tmp),'cache':str(cache),'common_cache':str(common),'disk_free':shutil.disk_usage(run).free,'cpu_count':os.cpu_count(),'ql_source_manifest':tree(SRC/'ql'),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
  oracle=expected(); dump(out/'expected-tuples.json',oracle)
  version=invoke('version',[CODEQL,'version']);
  if b'2.27.4' not in version: raise RuntimeError('CodeQL version mismatch')
  invoke('init',[CODEQL,'database','init',db,'--language=ucode',f'--search-path={pack}/ucode-extractor-pack',f'--source-root={source}',f'--common-caches={common}'])
  invoke('index',[CODEQL,'database','index-files',db,'--language=ucode','--include=**/siblings.ut','--include=**/siblings-all-covered.ut',f'--working-dir={source}',f'--common-caches={common}'],{'CODEQL_UCODE_STAGED_ROOT':str(source)})
  routing=json.loads((db/'trap/ucode/routing.json').read_text()); dump(out/'routing.json',routing)
  expected_routes=[{'path':str(source/'usr/share/ucode/controls'/n),'installed_path':'usr/share/ucode/controls/'+n,'classification':'markup','reason':'ut_markup_extension','status':'inconclusive','inconclusive_reason':'markup_not_modeled'} for n in FIXTURES]
  count={'input_count':2,'plain_count':0,'markup_count':2,'markup_inconclusive_count':2,'uncertain_count':0,'excluded_count':0,'duplicate_input_count':0}
  if any(routing.get(k)!=v for k,v in count.items()) or sorted(routing['decisions'],key=lambda x:x['path'])!=sorted(expected_routes,key=lambda x:x['path']): raise AssertionError('routing')
  invoke('finalize',[CODEQL,'database','finalize',db,f'--common-caches={common}'])
  search=':'.join(map(str,[pack/'ucode-extractor-pack',ql/'ql/lib',ql/'ql/src']))
  def query(name,path,fmt='csv'):
   b=out/(name+'.bqrs'); decoded=out/(name+'.'+fmt)
   invoke(name,[CODEQL,'query','run',path,f'--database={db}',f'--search-path={search}',f'--common-caches={common}',f'--compilation-cache={cache}/compilation','--no-default-compilation-cache','--threads=1','--ram=2048',f'--output={b}'])
   args=[CODEQL,'bqrs','decode',f'--format={fmt}',f'--output={decoded}'];
   if fmt=='json': args+=['--entities=url,string']
   invoke(name+'-decode',args+[b]); return decoded
  files=query('extracted',ql/'ql/src/diagnostics/SuccessfullyExtractedFiles.ql','json'); urls=[r[0]['url']['uri'] for r in json.loads(files.read_text())['#select']['tuples']]
  check('files',[[x] for x in urls],[[ (source/'usr/share/ucode/controls'/n).resolve().as_uri()] for n in FIXTURES])
  err=query('errors',ql/'ql/src/diagnostics/ExtractionErrors.ql','json'); check('errors',json.loads(err.read_text())['#select']['tuples'],[])
  def rows(p):
   with p.open(newline='') as f: return list(csv.reader(f))[1:]
  check('diagnostics',rows(query('diagnostics',ql/'ql/src/pkg6-diagnostics.ql')),[])
  got={n:rows(query(n,ql/'ql/src'/('pkg6-'+n+'.ql'))) for n in ('roots','scopes','ast','nodes','edges')}
  for n in ('roots','scopes','nodes','edges'): check(n,got[n],oracle[n])
  # AST query returns additional kinds: compare every independently specified selected tuple,
  # with exact per-tuple entity count, while retaining the full observed AST table.
  wanted={tuple(row[:-1]) for row in oracle['ast_selected']}
  check('ast-selected',[row for row in got['ast'] if tuple(row[:-1]) in wanted],oracle['ast_selected'])
  for name,digest in FIXTURES.items():
   if h(source/'usr/share/ucode/controls'/name)!=digest: raise AssertionError('source changed after run: '+name)
  dump(log/'result.json',{'status':'complete','finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commands':len(commands)})
 except BaseException as exc:
  dump(log/'result.json',{'status':'failed','error':repr(exc),'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commands':len(commands)})
  raise
if __name__=='__main__': run()
