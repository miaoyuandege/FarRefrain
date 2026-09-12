"""Optional pure plain-file projection helper; no CLI, registry, mutation or daemon."""
import json, math
from pathlib import Path

STATUSES={'CAPTURED','PROPOSED','ADOPTED','CONTESTED','SUPERSEDED','OBSERVED'}
TYPES={'FACT','DECISION','CONSTRAINT','GOTCHA','FAILURE'}
TARGETS={0:(5,6000),1:(8,12000),2:(12,18000),3:(16,30000)}
FIELDS={'truth_status','knowledge_type','scope','primary','evidence','supersedes'}

def local(root,relative):
    root=Path(root).resolve(); candidate=root/relative
    if Path(relative).is_absolute() or candidate.is_symlink() or not candidate.resolve().is_relative_to(root) or not candidate.is_file():
        raise ValueError('missing or unsafe local reference')
    return candidate

def record(root,path,role):
    if role not in {'boot','current','planning','history'}:raise ValueError('unknown role')
    p=local(root,path); text=p.read_text(encoding='utf-8')
    explicit=text.startswith('---\n')
    if explicit:
        parts=text.split('---\n',2)
        if len(parts)!=3:raise ValueError('unclosed metadata')
        meta=json.loads(parts[1])
        if not isinstance(meta,dict) or set(meta)-FIELDS:raise ValueError('unknown metadata')
        if not {'truth_status','knowledge_type','scope','evidence'}<=set(meta):raise ValueError('incomplete metadata')
        if meta['truth_status'] not in STATUSES or meta['knowledge_type'] not in TYPES:raise ValueError('unknown semantics')
        if not isinstance(meta['scope'],list) or not meta['scope'] or not all(isinstance(s,str) and s.strip() for s in meta['scope']):raise ValueError('scope required')
        if not isinstance(meta['evidence'],list) or not all(isinstance(x,str) for x in meta['evidence']):raise ValueError('invalid evidence')
        if not isinstance(meta.get('primary',False),bool):raise ValueError('primary must be boolean')
        if meta['truth_status'] in {'ADOPTED','OBSERVED'} and not meta['evidence']:raise ValueError('evidence required')
        for rel in meta['evidence']+([meta['supersedes']] if meta.get('supersedes') else []):
            target=(p.parent/rel).relative_to(Path(root))
            local(root,target)
        if role in {'planning','history'} and meta['truth_status']=='ADOPTED':raise ValueError('role/status conflict; explicit adoption decision and location repair required')
    else:
        meta={'truth_status':{'current':'ADOPTED','planning':'PROPOSED','history':'SUPERSEDED','boot':'OBSERVED'}[role], 'knowledge_type':'FACT','scope':['global'],'primary':False,'evidence':[]}
    return {'path':path,'role':role,'explicit':explicit,**meta}

def promotion(root,path,*,authorized=False,unresolved_conflict=True,automatic=True):
    r=record(root,path,'current')
    if automatic or not authorized or unresolved_conflict:raise ValueError('promotion gate not satisfied')
    if not r['explicit'] or not r['evidence'] or not r['scope']:raise ValueError('explicit evidence and scope required')
    if r['truth_status'] not in {'PROPOSED','CONTESTED'}:raise ValueError('propose or resolve before adoption')
    return {'permitted':True,'writes_performed':False,'history_preservation_required':True}

def choose(records,tier,*,scopes=(),include_planning=False,evidence_paths=(),primary_paths=()):
    if tier not in TARGETS:raise ValueError('unknown tier')
    primary=set(primary_paths); wanted=set(scopes)
    selected=[]
    for r in records:
        status=r['truth_status']; typ=r['knowledge_type']; scope=set(r['scope']); role=r['role']
        is_primary=role=='current' and status=='ADOPTED' and (r.get('primary') or r['path'] in primary)
        take=role=='boot' or is_primary
        if tier>=1 and role=='current' and 'global' in scope and status in {'ADOPTED','CONTESTED'} and typ not in {'GOTCHA','FAILURE'}:take=True
        if tier>=2 and wanted&scope and status in {'ADOPTED','CONTESTED','OBSERVED'}:take=True
        if tier>=2 and include_planning and role=='planning':take=True
        if tier==3 and r['path'] in evidence_paths:take=True
        if status in {'CAPTURED','SUPERSEDED'} and r['path'] not in evidence_paths:take=False
        if take and r['path'] not in selected:selected.append(r['path'])
    if not any(r['path'] in selected and r['role']=='current' and r['truth_status']=='ADOPTED' and (r.get('primary') or r['path'] in primary) for r in records):
        raise ValueError('missing primary adopted current; follow explicit Current link')
    return selected

def account(root,paths,tier,*,target=None):
    rows=[]
    for path in paths:
        raw=local(root,path).read_bytes(); chars=len(raw.decode('utf-8'))
        rows.append({'path':path,'bytes':len(raw),'characters':chars,'estimated_tokens':math.ceil(chars/4)})
    files,chars=target or TARGETS[tier]
    total=sum(r['characters'] for r in rows)
    return {'reads':rows,'files':len(rows),'characters':total,'bytes':sum(r['bytes'] for r in rows),'estimated_tokens':sum(r['estimated_tokens'] for r in rows),'hops':max(0,len(rows)-1),'target_files':files,'target_characters':chars,'over_budget':len(rows)>files or total>chars,'fallback':'Report excess and follow named authority; never silently truncate','method':'sum ceil(Unicode characters/4) per read; not native tokenizer'}
