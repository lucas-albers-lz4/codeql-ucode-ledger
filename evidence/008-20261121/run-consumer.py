#!/usr/bin/env python3
"""Fresh typed input through actual adapter in disposable copies; BASE TYPED SOURCE CSV RUN."""
import hashlib,json,os,subprocess,sys,time
from pathlib import Path
base,typed,source,csvfile,run=(Path(x).resolve() for x in sys.argv[1:]); run.mkdir(parents=True,exist_ok=False)
pin='33ff29f9f311fec078be8e2df04261529cba0e65'
paths=['reports/m4-block-device-exec.json','reports/handler_effects.json','policy/grants.json','policy/policy_decisions.json']; target='m4:effect:luci-setBlockDetect-system'; commands=[]
def h(b):return hashlib.sha256(b).hexdigest()
def call(label,argv,cwd,expected=0):
 argv=list(map(str,argv)); start=time.monotonic(); p=subprocess.run(['/usr/bin/time','-l',*argv],cwd=cwd,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','HOME':str(run.parent/'home')}); (run/(label+'.stdout')).write_text(p.stdout); (run/(label+'.stderr')).write_text(p.stderr); commands.append({'label':label,'cwd':str(cwd),'argv':argv,'exit':p.returncode,'wall_seconds':round(time.monotonic()-start,3),'stderr_and_time':label+'.stderr'}); (run/'commands.json').write_text(json.dumps(commands,indent=2)+'\n'); assert p.returncode==expected,(label,p.returncode,p.stderr); return p

def clone(name):
 d=run/name; call(name+'-clone',['git','clone','--quiet','--no-hardlinks','--local',base,d],run); call(name+'-checkout',['git','-C',d,'checkout','--detach',pin],run); return d
def snap(root):return {x:(root/x).read_bytes() for x in paths}
def hashes(s):return {k:h(v) for k,v in s.items()}
def invoke(label,root,flag,path,expect=0):return call(label,[sys.executable,'-B','-m','policy.setblock_table',flag,path,'--source-root',source],root,expect)
repo=clone('valid'); before=snap(repo); invoke('import',repo,'--typed-json',typed); after=snap(repo)
for path in paths[:2]:
 old=json.loads(before[path]); new=json.loads(after[path]); assert [x for x in old if x.get('record_id')!=target]==[x for x in new if x.get('record_id')!=target]
 row,=[x for x in new if x.get('record_id')==target]; assert row['analysis_revision']=='step3:setblock-typed-import-v1' and row['assessment']=='intended_access' and row['expectation_id']=='luci-mod-system-mounts'
 assert row['source_location']=={'path':'usr/share/rpcd/ucode/luci','start_line':532,'start_column':21,'end_line':532,'end_column':68}
 assert {'policy:grant:luci-mod-system-mounts:ubus_http:luci.setBlockDetect','policy:grant:root:ubus_http:luci.setBlockDetect'}<=set(row['evidence_refs'])
assert all(before[x]==after[x] for x in paths[2:]); invoke('reimport',repo,'--typed-json',typed); assert snap(repo)==after
p=invoke('downgrade',repo,'--csv',csvfile,1); assert 'typed-to-CSV downgrade is not supported' in p.stderr and snap(repo)==after
wrong=run/'policy-bearing.json'; rows=json.loads(typed.read_text()); rows[0]['assessment']='intended_access'; wrong.write_text(json.dumps(rows)+'\n')
negative=clone('invalid-policy'); negbefore=snap(negative); p=invoke('invalid-policy-import',negative,'--typed-json',wrong,1); assert 'typed setBlockDetect record does not match the supported family' in p.stderr and snap(negative)==negbefore
raw=typed.read_text(); token='"start_line": 532'; assert raw.count(token)==1
numeric=run/'integral-decimal.json'; numeric.write_text(raw.replace(token,'"start_line": 532.0'))
numrepo=clone('invalid-numeric'); numbefore=snap(numrepo); p=invoke('invalid-numeric-import',numrepo,'--typed-json',numeric,1); assert 'typed setBlockDetect record does not match the supported family' in p.stderr and snap(numrepo)==numbefore
summary={'consumer_commit':pin,'input_sha256':h(typed.read_bytes()),'before':hashes(before),'after':hashes(after),'reimport_identical':True,'csv_downgrade':{'exit':1,'unchanged':True},'policy_field_control':{'exit':1,'unchanged':True},'integral_decimal_control':{'exit':1,'unchanged':True,'token':'start_line: 532.0'}}
(run/'summary.json').write_text(json.dumps(summary,indent=2)+'\n'); print('typed import, idempotence, downgrade, policy and numeric rejection verified')
