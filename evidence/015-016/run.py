#!/usr/bin/env python3
"""Index pinned upstream LuCI installed-source slice and test status query."""
import hashlib, json, os, shutil, subprocess, sys, time
from pathlib import Path
producer,luci,run=map(lambda x:Path(x).resolve(),sys.argv[1:]);run.mkdir(parents=True,exist_ok=False)
pack=producer/'extractor-pack'; rels={'usr/share/rpcd/ucode/luci':'modules/luci-base/root/usr/share/rpcd/ucode/luci','usr/share/ucode/luci/sys.uc':'modules/luci-base/ucode/sys.uc','usr/share/ucode/luci/zoneinfo.uc':'modules/luci-base/ucode/zoneinfo.uc'}
hashes={'usr/share/rpcd/ucode/luci':'6f9d972958d9cfb8a7ba421f38f0a5b03718ffeb0e30d460b64c9faf725fc54e','usr/share/ucode/luci/sys.uc':'0380fba5d843a8950bab0ef70982cb40ab8f475e8d267c873e4199a736b55656','usr/share/ucode/luci/zoneinfo.uc':'54162a073660ea65706aa920a10cfbd3ee4d345e1e4ab3bed8a8d56c9cab3863'}
for rel,src in rels.items():assert hashlib.sha256((luci/src).read_bytes()).hexdigest()==hashes[rel]
env=os.environ.copy();env.pop('CODEQL_UCODE_STAGED_ROOT',None); log=[]
def call(label,args,env_arg=None,out=None):
 stamp=time.monotonic(); timing=run/(label+'.time'); argv=['/usr/bin/time','-f','wall_s=%e user_s=%U sys_s=%S max_rss_kb=%M','-o',str(timing),*map(str,args)];p=subprocess.run(argv,cwd=producer,env=env_arg or env,capture_output=True);entry={'stage':label,'argv':argv[5:],'exit':p.returncode,'elapsed_s':round(time.monotonic()-stamp,3),'timing':timing.read_text(),'stdout':p.stdout.decode(errors='replace'),'stderr':p.stderr.decode(errors='replace')};log.append(entry);(run/'commands.json').write_text(json.dumps(log,indent=2)+'\n');assert p.returncode==0,(label,p.stderr.decode(errors='replace'));
 if out:out.write_bytes(p.stdout)
def stage(label,mutate=False):
 base=run/label;root=base/'root'
 for rel,source in rels.items():
  f=root/rel;f.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(luci/source,f)
 if mutate:
  f=root/'usr/share/rpcd/ucode/luci';s=f.read_text();a='return { result: conntrack_list() };';b='return { result: process_list() };';assert s.count(a)==s.count(b)==1;s=s.replace(a,'return { result: LEDGER_SWAP() };').replace(b,a).replace('return { result: LEDGER_SWAP() };',b);f.write_text(s)
 return root
def db_run(label,root):
 base=run/label;db=base/'db'; env2=env.copy();env2['CODEQL_UCODE_STAGED_ROOT']=str(root)
 call(label+'-init',['codeql','database','init',db,'--language=ucode',f'--search-path={pack}',f'--source-root={root}'])
 call(label+'-index',['codeql','database','index-files',db,'--language=ucode','--include=**/rpcd/ucode/luci','--include=**/*.uc',f'--working-dir={root}'],env2)
 shutil.copyfile(db/'trap/ucode/routing.json',base/'routing.json');receipt=json.loads((base/'routing.json').read_text());assert receipt['input_count']==receipt['plain_count']==3 and receipt['excluded_count']==0,receipt;assert {x['path'] for x in receipt['decisions']}=={str(root/r) for r in rels}
 call(label+'-finalize',['codeql','database','finalize',db])
 for name,q in [('extracted','diagnostics/SuccessfullyExtractedFiles.ql'),('errors','diagnostics/ExtractionErrors.ql'),('status','m4/LuciSysStatusExec.ql')]:
  b=base/(name+'.bqrs');call(label+'-'+name+'-query',['codeql','query','run',producer/'ql/src'/q,f'--database={db}',f'--search-path={pack}:{producer}/ql/lib:{producer}/ql/src',f'--output={b}','--threads=1','--ram=2048']);call(label+'-'+name+'-decode',['codeql','bqrs','decode','--format=json','--entities=url,string',b],out=base/(name+'.json'))
 get=lambda n:json.loads((base/(n+'.json')).read_text())['#select']['tuples']
 extracted=get('extracted');errors=get('errors');assert len(extracted)==3 and {r[0]['url']['uri'] for r in extracted}=={(root/r).as_uri() for r in rels};assert not errors,errors
 return get('status')
root=stage('positive'); negroot=stage('dispatch-swapped',True)
# Direct extractor confirms the same valid installed plugin reaches the outside-root guard.
outside=run/'outside/usr/share/rpcd/ucode/luci';outside.parent.mkdir(parents=True);shutil.copyfile(luci/rels['usr/share/rpcd/ucode/luci'],outside)
listing=run/'direct-inputs';listing.write_text(str(root/'usr/share/rpcd/ucode/luci')+'\n'+str(outside)+'\n')
call('direct-extractor',[pack/'tools/linux64/extractor','extract','--source-archive-dir',run/'direct-archive','--output-dir',run/'direct-trap','--file-list',listing,'--staged-root',root]);d=json.loads((run/'direct-trap/routing.json').read_text());assert d['plain_count']==1 and d['excluded_count']==1 and [x['reason'] for x in d['decisions']]==['rpcd_raw_mode_full_path','outside_staged_root'],d
positive=db_run('positive',root);negative=db_run('dispatch-swapped',negroot)
want={'getProcessList via process_list popen /bin/busybox top -bn1 at line 7','getConntrackList via conntrack_list popen /usr/sbin/conntrack -L -o extended at line 49'}
assert len(positive)==2 and {r[1] for r in positive}==want and all(r[0]['url']['uri']==(root/'usr/share/ucode/luci/sys.uc').as_uri() for r in positive),positive
assert not negative,negative
print('three actual sources extracted, outside-root guard and status query control verified')
