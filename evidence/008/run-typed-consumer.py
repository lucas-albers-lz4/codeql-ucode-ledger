#!/usr/bin/env python3
"""Test real setBlockDetect typed import and rejection in disposable clones."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
base,typed,source,csvfile,run=(Path(x).resolve() for x in sys.argv[1:]); run.mkdir(parents=True,exist_ok=False)
paths=['reports/m4-block-device-exec.json','reports/handler_effects.json','policy/grants.json','policy/policy_decisions.json']; target='m4:effect:luci-setBlockDetect-system'; commands=[]
def h(b):return hashlib.sha256(b).hexdigest()
def call(argv,cwd):
 p=subprocess.run(list(map(str,argv)),cwd=cwd,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}); commands.append({'cwd':str(cwd),'argv':list(map(str,argv)),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}); (run/'commands.json').write_text(json.dumps(commands,indent=2)+'\n');return p
def clone(name):
 d=run/name
 for cmd in (['git','clone','--quiet','--no-hardlinks','--local',base,d],['git','-C',d,'checkout','--detach','a8bdef3c22c8d5ba9999baa978052b59bd22907e']):
  p=call(cmd,run); assert p.returncode==0,p.stderr
 return d
def snap(root):return {x:(root/x).read_bytes() for x in paths}
def hashes(s):return {k:h(v) for k,v in s.items()}
def invoke(root,flag,path):return call([sys.executable,'-B','-m','policy.setblock_table',flag,path,'--source-root',source],root)
repo=clone('valid'); before=snap(repo); p=invoke(repo,'--typed-json',typed); assert p.returncode==0,p.stderr; after=snap(repo)
for path in paths[:2]:
 old=json.loads(before[path]); new=json.loads(after[path]); assert [x for x in old if x.get('record_id')!=target]==[x for x in new if x.get('record_id')!=target]
 row,=[x for x in new if x.get('record_id')==target]; assert row['analysis_revision']=='step3:setblock-typed-import-v1' and row['assessment']=='intended_access' and row['expectation_id']=='luci-mod-system-mounts'
 assert row['source_location']=={'path':'usr/share/rpcd/ucode/luci','start_line':532,'start_column':21,'end_line':532,'end_column':68}
 assert {'policy:grant:luci-mod-system-mounts:ubus_http:luci.setBlockDetect','policy:grant:root:ubus_http:luci.setBlockDetect'}<=set(row['evidence_refs'])
assert all(before[x]==after[x] for x in paths[2:]); p=invoke(repo,'--typed-json',typed); assert p.returncode==0,p.stderr; assert snap(repo)==after
p=invoke(repo,'--csv',csvfile); assert p.returncode!=0 and snap(repo)==after; downgrade=p.stderr.strip().splitlines()[-1]; downgrade_exit=p.returncode
wrong=run/'wrong.json'; rows=json.loads(typed.read_text()); rows[0]['assessment']='intended_access'; wrong.write_text(json.dumps(rows)+'\n'); negative=clone('invalid'); negbefore=snap(negative); p=invoke(negative,'--typed-json',wrong); assert p.returncode!=0 and snap(negative)==negbefore
summary={'input_sha256':h(typed.read_bytes()),'before':hashes(before),'after':hashes(after),'reimport_identical':True,'csv_downgrade':{'exit':downgrade_exit,'unchanged':True,'error':downgrade},'policy_field_control':{'exit':p.returncode,'unchanged':True,'error':p.stderr.strip().splitlines()[-1]}}
(run/'summary.json').write_text(json.dumps(summary,indent=2)+'\n'); print('typed import, reimport and two rejection controls passed')
