#!/usr/bin/env python3
"""Fresh package-6 delta run; logs all commands and preserves failed attempts."""
import collections, csv, datetime, hashlib, json, os, pathlib, shutil, subprocess, sys, time
from expected import expected
P = pathlib.Path(__file__).resolve().parent
LEDGER = P.parents[1]
SRC = LEDGER/'work/creation-delta-source-20261123'
OLD = LEDGER/'work/creation-sibling-oracle/run-20261122-d'
CODEQL = LEDGER.parent/'.tools/codeql-2.27.4/codeql/codeql'
PIN = '11a53fd8e911573860950ee8e549b337a8742438'
BUILD_PIN = '8375887ed14825dd59addbfd0df43616d9e684fb'
FIXTURES = {
 'siblings.ut':'940472ed365ba3c40aed4b42427ca703c05ece028069e696eb98d850808d7d16',
 'siblings-all-covered.ut':'885ea36bf4edfa571a860c0226642a491b007f40d58ca8ed660a7bea2a46fb23',
 'siblings-computed-callee.ut':'e4781ff609e500d449f48641a418a8ee1f211ef6d68fea080d71826d6b728885',
}
PACK_PATHS=('extractor','extractor-pack','Cargo.toml','Cargo.lock','codeql-extractor.yml','.codeqlmanifest.json','ql/src/qlpack.yml','ql/src/codeql-pack.lock.yml','ql/lib/qlpack.yml','ql/lib/codeql-pack.lock.yml','scripts/create-extractor-pack.sh','scripts/clone-grammar.sh','ql/lib/ucode.dbscheme','ql/lib/ucode.dbscheme.stats','ql/lib/codeql/ucode/ast/internal/TreeSitter.qll','tools','downgrades')
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def tree(p): return {str(x.relative_to(p)):h(x) for x in sorted(p.rglob('*')) if x.is_file() and not x.is_symlink()}
def dump(p,x): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def git(*args): return subprocess.check_output(['git','-C',str(SRC),*args],text=True).strip()
def run():
 if len(sys.argv)!=2: raise RuntimeError('supply a new, nonexistent run path beneath work/creation-delta-oracle-20261123/')
 R=pathlib.Path(sys.argv[1]).resolve()
 if not R.is_relative_to(P) or R.exists(): raise RuntimeError('run must be new and beneath the oracle workspace')
 R.mkdir(parents=True); log=R/'logs'; out=R/'output'; tmp=R/'tmp'; cache=R/'cache'; common=R/'common-cache'; source=R/'source'; pack=R/'pack'; ql=R/'producer-ql'; db=R/'database/db'
 for d in (log,out,tmp,cache/'compilation',common,source,pack,ql,db.parent): d.mkdir(parents=True,exist_ok=True)
 env=dict(os.environ,TMPDIR=str(tmp),TMP=str(tmp),TEMP=str(tmp),XDG_CACHE_HOME=str(cache),CODEQL_UCODE_CACHE=str(cache),PYTHONDONTWRITEBYTECODE='1'); env.pop('CODEQL_UCODE_STAGED_ROOT',None)
 commands=[]
 def invoke(label,args,extra=None):
  en=env.copy(); en.update(extra or {}); argv=list(map(str,args)); started=time.monotonic()
  proc=subprocess.run(['/usr/bin/time','-l',*argv],cwd=R,env=en,capture_output=True)
  elapsed=time.monotonic()-started
  (out/(label+'.stdout')).write_bytes(proc.stdout); (out/(label+'.stderr-time.txt')).write_bytes(proc.stderr)
  commands.append({'label':label,'argv':argv,'cwd':str(R),'exit':proc.returncode,'elapsed_seconds':elapsed,'stdout':label+'.stdout','stderr_time':label+'.stderr-time.txt'})
  dump(log/'commands.json',commands)
  if proc.returncode: raise RuntimeError(label+' exited '+str(proc.returncode)+'; retained stderr/time')
  return proc.stdout
 def check(label,actual,wanted):
  a=collections.Counter(map(tuple,actual)); e=collections.Counter(map(tuple,wanted)); ok=a==e
  dump(out/('assert-'+label+'.json'),{'passed':ok,'actual':actual,'expected':wanted,'actual_count':len(actual),'expected_count':len(wanted)})
  if not ok: raise AssertionError(label+' mismatch')
 try:
  ps=subprocess.run(['ps','-ax','-o','pid=,etime=,command='],capture_output=True,text=True,check=True)
  heavy=[s for s in ps.stdout.splitlines() if ('/codeql/codeql ' in s or 'com.semmle.cli2.CodeQL' in s) and 'ps -ax' not in s]
  dump(log/'process-preflight.json',{'observed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'codeql_processes':heavy})
  if heavy: raise RuntimeError('live CodeQL process detected; fail closed')
  if git('rev-parse','HEAD')!=PIN or git('status','--porcelain=v1'): raise RuntimeError('producer pin/clean state mismatch')
  delta=git('diff','--name-only',BUILD_PIN,PIN,'--',*PACK_PATHS)
  if delta: raise RuntimeError('extractor/pack input delta since build: '+delta)
  locks={x:h(SRC/x) for x in ('ql/lib/codeql-pack.lock.yml','ql/src/codeql-pack.lock.yml')}
  if locks!={'ql/lib/codeql-pack.lock.yml':'bce2891940f09fcac3337b250707047ba9fd06d307abdbc7cb42c2ed193751a3','ql/src/codeql-pack.lock.yml':'bce2891940f09fcac3337b250707047ba9fd06d307abdbc7cb42c2ed193751a3'}: raise RuntimeError('lock digest mismatch')
  oldpre=json.loads((OLD/'logs/preflight.json').read_text())
  if h(CODEQL)!=oldpre['codeql_sha256']: raise RuntimeError('CodeQL binary digest differs from package 6 provenance')
  pack_source=OLD/'pack/ucode-extractor-pack'; pack_manifest=tree(pack_source)
  build=json.loads((LEDGER/'work/wave10-ast-run/preparation-manifest.json').read_text())
  build_files={x['path']:x['sha256'] for x in build['source_pack_files'] if x.get('sha256')}
  if pack_manifest!=build_files: raise RuntimeError('installed extractor pack differs from retained build manifest')
  cache_source=LEDGER/'work/wave10-ast-run/home/.codeql/packages'; common_source=OLD/'common-cache'
  if tree(cache_source)!=tree(common_source/'packages'): raise RuntimeError('dependency package copy differs from retained cache provenance')
  grammar=LEDGER/'work/typed-20261121/producer/extractor/tree-sitter'
  ghead=subprocess.check_output(['git','-C',str(grammar),'rev-parse','HEAD'],text=True).strip()
  gstatus=subprocess.check_output(['git','-C',str(grammar),'status','--porcelain=v1'],text=True).strip()
  gdiff=subprocess.check_output(['git','-C',str(grammar),'diff','--','Cargo.toml'],text=True)
  if ghead!='4a243af329fae2f4ff01e0fc80133cbab8314600' or gstatus!='M Cargo.toml' or '-tree-sitter = "0.27.1"' not in gdiff or '+tree-sitter = "=0.26.8"' not in gdiff: raise RuntimeError('grammar build provenance mismatch')
  for origin,dest in ((pack_source,pack/'ucode-extractor-pack'),(common_source,common),(SRC/'ql',ql/'ql')):
   shutil.copytree(origin,dest,dirs_exist_ok=True,symlinks=True)
   if tree(origin)!=tree(dest): raise RuntimeError('copy hash mismatch: '+str(origin))
  shutil.copy2(SRC/'.codeqlmanifest.json',ql/'.codeqlmanifest.json')
  for name,digest in FIXTURES.items():
   source_fixture=P/'fixtures'/name
   if h(source_fixture)!=digest: raise RuntimeError('source-first fixture hash mismatch: '+name)
   target=source/'usr/share/ucode/controls'/name; target.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(source_fixture,target)
  for file in (P/'queries').glob('*.ql'): shutil.copy2(file,ql/'ql/src'/('pkg6-'+file.name))
  (ql/'ql/src/pkg6-diagnostics.ql').write_text('import codeql.ucode.Diagnostics\nfrom Diagnostic d\nwhere d.getLocation().getFile().getBaseName() = ["siblings.ut", "siblings-all-covered.ut", "siblings-computed-callee.ut"]\nselect d.getLocation().getFile().getBaseName(), d.getTag(), d.getMessage()\n')
  prep={
   'producer_pin':PIN,'producer_dirty':False,'producer_status':'clean','pack_build_pin':BUILD_PIN,
   'pack_input_delta':delta,'grammar_revision':ghead,'grammar_status':gstatus,'grammar_bootstrap_diff_sha256':hashlib.sha256(gdiff.encode()).hexdigest(),
   'codeql_version_expected':'2.27.4','codeql_binary_sha256':h(CODEQL),'locks':locks,
   'pack_build_provenance':'reused from package 6 validated pack copied from build manifest; build revision 8375887..., CodeQL 2.27.4, grammar 4a243af with bootstrap pin 0.26.8; see prior run preflight and claim 028',
   'pack_manifest_sha256_by_path':pack_manifest,'dependency_cache_sha256_by_path':tree(common/'packages'),
   'fixtures':FIXTURES,'oracle_sha256':h(P/'expected.json'),'oracle_generator_sha256':h(P/'expected.py'),'inherited_HOME':os.environ.get('HOME'),
   'tmp':str(tmp),'cache':str(cache),'common_cache':str(common),'db':str(db),'source_root':str(source),
   'ql_source_hashes':tree(SRC/'ql'),'free_disk_bytes_before_run':shutil.disk_usage(R).free,'cpu_count':os.cpu_count(),
   'prepared_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
  dump(log/'preflight.json',prep)
  oracle=expected(); dump(out/'expected-tuples.json',oracle)
  ver=invoke('version',[CODEQL,'version'])
  if b'2.27.4' not in ver: raise RuntimeError('CodeQL version mismatch')
  invoke('init',[CODEQL,'database','init',db,'--language=ucode',f'--search-path={pack/"ucode-extractor-pack"}',f'--source-root={source}',f'--common-caches={common}'])
  invoke('index',[CODEQL,'database','index-files',db,'--language=ucode','--include=**/*.ut',f'--working-dir={source}',f'--common-caches={common}'],{'CODEQL_UCODE_STAGED_ROOT':str(source)})
  route=json.loads((db/'trap/ucode/routing.json').read_text()); dump(out/'routing.json',route)
  names=sorted(FIXTURES)
  expected_routes=[{'path':str(source/'usr/share/ucode/controls'/n),'installed_path':'usr/share/ucode/controls/'+n,'classification':'markup','reason':'ut_markup_extension','status':'inconclusive','inconclusive_reason':'markup_not_modeled'} for n in names]
  counts={'input_count':3,'plain_count':0,'markup_count':3,'markup_inconclusive_count':3,'uncertain_count':0,'excluded_count':0,'duplicate_input_count':0}
  if any(route.get(k)!=v for k,v in counts.items()) or collections.Counter(map(json.dumps,route.get('decisions',[])))!=collections.Counter(map(json.dumps,expected_routes)): raise AssertionError('routing identity/multiplicity mismatch')
  invoke('finalize',[CODEQL,'database','finalize',db,f'--common-caches={common}'])
  search=':'.join(map(str,[pack/'ucode-extractor-pack',ql/'ql/lib',ql/'ql/src']))
  def query(name,path,fmt='csv'):
   b=out/(name+'.bqrs'); decoded=out/(name+'.'+fmt)
   invoke(name,[CODEQL,'query','run',path,f'--database={db}',f'--search-path={search}',f'--common-caches={common}',f'--compilation-cache={cache}/compilation','--no-default-compilation-cache','--threads=1','--ram=2048',f'--output={b}'])
   args=[CODEQL,'bqrs','decode',f'--format={fmt}',f'--output={decoded}']
   if fmt=='json': args+=['--entities=url,string']
   invoke(name+'-decode',args+[b]); return decoded
  files=query('extracted',ql/'ql/src/diagnostics/SuccessfullyExtractedFiles.ql','json')
  file_rows=json.loads(files.read_text())['#select']['tuples']; observed=collections.Counter(r[0]['url']['uri'] for r in file_rows)
  wanted=collections.Counter((source/'usr/share/ucode/controls'/n).resolve().as_uri() for n in names)
  if observed!=wanted: raise AssertionError('successful extraction file identity/multiplicity mismatch')
  dump(out/'assert-files.json',{'passed':True,'actual':dict(observed),'expected':dict(wanted)})
  errors=query('errors',ql/'ql/src/diagnostics/ExtractionErrors.ql','json'); err_rows=json.loads(errors.read_text())['#select']['tuples']
  check('errors',err_rows,[])
  def rows(path):
   with path.open(newline='') as f: return list(csv.reader(f))[1:]
  check('diagnostics',rows(query('diagnostics',ql/'ql/src/pkg6-diagnostics.ql')),[])
  got={n:rows(query(n,ql/'ql/src'/('pkg6-'+n+'.ql'))) for n in ('roots','scopes','ast','nodes','edges')}
  for n in ('roots','scopes','nodes','edges'): check(n,got[n],oracle[n])
  selected={tuple(r[:-1]) for r in oracle['ast_selected']}
  check('ast-selected',[r for r in got['ast'] if tuple(r[:-1]) in selected],oracle['ast_selected'])
  for name,digest in FIXTURES.items():
   if h(source/'usr/share/ucode/controls'/name)!=digest: raise AssertionError('staged source changed after extraction: '+name)
  dump(log/'result.json',{'status':'complete','finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commands':len(commands)})
 except BaseException as exc:
  dump(log/'result.json',{'status':'failed','error':repr(exc),'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commands':len(commands)})
  raise
if __name__=='__main__': run()
