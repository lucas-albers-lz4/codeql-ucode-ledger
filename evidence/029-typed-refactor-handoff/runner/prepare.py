#!/usr/bin/env python3
"""Prepare unique run after fresh pin/issue review; no CodeQL execution."""
import hashlib,json,os,pathlib,shutil,subprocess,sys,time
P=pathlib.Path(__file__).resolve().parent; ROOT=P.parents[1]; WORK=ROOT/'work'; PS=WORK/'pkg1-codeql-ucode'; CS=WORK/'pkg1-codeql-openwrt'; OLD=WORK/'cfg-trim-oracle/run-20261122-a'; BUILT=WORK/'wave10-ast-run'; TOOL=ROOT.parent/'.tools/codeql-2.27.4/codeql/codeql'; PP='6010ff2c0f101f7629c6fe117a421f671c311a2b'; CP='48c6a65b7578234644c6b06780fc82ccf6d61a8b'
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def tree(p): return {str(x.relative_to(p)):h(x) for x in sorted(p.rglob('*')) if x.is_file() and not x.is_symlink()}
def run():
 if len(sys.argv)!=2: raise RuntimeError('argument: unique path under work/')
 r=pathlib.Path(sys.argv[1]).resolve()
 if not r.is_relative_to(WORK.resolve()) or r.exists(): raise RuntimeError('run must be new and under work/')
 r.mkdir(); (r/'preflight').mkdir(); log=[]
 def call(label,args,cwd=r):
  t=time.monotonic(); p=subprocess.run(list(map(str,args)),cwd=cwd,capture_output=True); (r/'preflight'/f'{label}.stdout').write_bytes(p.stdout); (r/'preflight'/f'{label}.stderr').write_bytes(p.stderr); log.append({'label':label,'argv':list(map(str,args)),'cwd':str(cwd),'exit':p.returncode,'seconds':time.monotonic()-t}); (r/'preflight/commands.json').write_text(json.dumps(log,indent=2)+'\n');
  if p.returncode: raise RuntimeError(label+' failed')
  return p.stdout.decode().strip()
 def pin(repo,expected,label):
  if call(label+'-pin',['git','-C',repo,'rev-parse','HEAD'])!=expected or call(label+'-clean',['git','-C',repo,'status','--porcelain=v1']): raise RuntimeError(label+' not clean at pin')
 try:
  ps=call('processes',['ps','-ax','-o','pid=,etime=,command=']); active=[x for x in ps.splitlines() if ('/codeql/codeql ' in x or 'com.semmle.cli2.CodeQL' in x) and 'ps -ax' not in x]
  if active: raise RuntimeError('CodeQL process active')
  pin(PS,PP,'producer-source'); pin(CS,CP,'consumer-source')
  delta=call('pack-source-delta',['git','-C',PS,'diff','--name-only','8375887ed14825dd59addbfd0df43616d9e684fb',PP,'--','extractor','extractor-pack','Cargo.toml','Cargo.lock','codeql-extractor.yml','.codeqlmanifest.json','ql/src/qlpack.yml','ql/src/codeql-pack.lock.yml','ql/lib/qlpack.yml','ql/lib/codeql-pack.lock.yml','scripts/create-extractor-pack.sh','scripts/clone-grammar.sh','ql/lib/ucode.dbscheme','ql/lib/ucode.dbscheme.stats','ql/lib/codeql/ucode/ast/internal/TreeSitter.qll','tools','downgrades'])
  if delta: raise RuntimeError('relevant pack-source delta')
  original=json.loads((BUILT/'preparation-manifest.json').read_text()); pack=OLD/'pack/ucode-extractor-pack'; expected={x['path']:x['sha256'] for x in original['source_pack_files'] if x.get('sha256')}
  if tree(pack)!=expected or tree(OLD/'common-cache/packages')!=tree(BUILT/'home/.codeql/packages'): raise RuntimeError('pack/dependency mismatch')
  prev=json.loads((OLD/'preparation.json').read_text()); locks={x:h(PS/x) for x in ('ql/lib/codeql-pack.lock.yml','ql/src/codeql-pack.lock.yml')}
  if locks!=prev['lock_digests'] or h(TOOL)!=prev['codeql_sha256']: raise RuntimeError('tool or lock mismatch')
  grammar=WORK/'typed-20261121/producer/extractor/tree-sitter'; g=call('grammar-pin',['git','-C',grammar,'rev-parse','HEAD']); gs=call('grammar-clean',['git','-C',grammar,'status','--porcelain=v1']); gd=call('grammar-diff',['git','-C',grammar,'diff','--','Cargo.toml'])
  if g!='4a243af329fae2f4ff01e0fc80133cbab8314600' or gs!='M Cargo.toml' or '-tree-sitter = "0.27.1"' not in gd or '+tree-sitter = "=0.26.8"' not in gd: raise RuntimeError('grammar mismatch')
  version=call('codeql-version',[TOOL,'version'])
  if '2.27.4' not in version: raise RuntimeError('CodeQL version mismatch')
  buildlog=WORK/'typed-20261121/build-offline.log'
  if 'Finished `release`' not in buildlog.read_text(): raise RuntimeError('no retained completed build')
  for label,source,pinval in [('producer',PS,PP),('consumer',CS,CP)]:
   dst=r/label; call(label+'-clone',['git','clone','--no-hardlinks','--no-checkout',source,dst]); call(label+'-checkout',['git','-C',dst,'checkout','--detach',pinval]); pin(dst,pinval,label+'-copy')
  for origin,dest in ((pack,r/'producer/extractor-pack'),(OLD/'common-cache',r/'common-cache')):
   shutil.copytree(origin,dest,symlinks=True)
   if tree(origin)!=tree(dest): raise RuntimeError('copied tree differs')
  for n in ('tmp','cache/compilation'): (r/n).mkdir(parents=True)
  (r/'preflight/provenance.json').write_text(json.dumps({'producer':PP,'consumer':CP,'grammar':g,'grammar_dirty':gs,'grammar_diff_sha256':hashlib.sha256(gd.encode()).hexdigest(),'build_log_sha256':h(buildlog),'build_provenance':'claim 008 release build, Cargo 1.100.0; build-time rustc not separately logged; target metadata reports 1.100.0','pack_build_revision':'8375887ed14825dd59addbfd0df43616d9e684fb','pack_manifest':tree(pack),'copied_pack_manifest':tree(r/'producer/extractor-pack'),'dependencies':tree(r/'common-cache/packages'),'locks':locks,'consumer_lock':h(r/'consumer/corpus/lock.json'),'codeql_path':str(TOOL),'codeql_sha256':h(TOOL),'free_disk_bytes':shutil.disk_usage(r).free,'cpu_count':os.cpu_count(),'HOME_inherited':True,'cache_note':'Explicit cache paths do not prove all writes are isolated','python_executable':sys.executable,'python_version':sys.version,'producer_runner_sha256':h(P/'run-producer.py'),'consumer_runner_sha256':h(P/'run-consumer.py')},indent=2)+'\n')
  (r/'preflight/result.json').write_text('{"status":"prepared"}\n')
 except BaseException as e:
  (r/'preflight/result.json').write_text(json.dumps({'status':'failed','error':repr(e)})+'\n'); raise
if __name__=='__main__': run()
