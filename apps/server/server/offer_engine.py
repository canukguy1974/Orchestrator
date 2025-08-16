import json, os

def _base_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..'))
OFFERS=json.load(open(os.path.join(_base_dir(),'configs','offers','catalog.json'),'r',encoding='utf-8'))['items']

def evaluate(user, session):
    segs=set(user.get('segments', [])); balance=user.get('balance',0); out=[]
    for it in OFFERS:
        rules=it.get('rules',{}); ok=True
        req=set(rules.get('requireSegments', []))
        if req and not req.intersection(segs): ok=False
        if 'minBalance' in rules and balance<rules['minBalance']: ok=False
        if ok: out.append(it)
    return out[:2]
