import json, os

def _base_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..'))

def load_persona(persona_id: str):
    pdir=os.path.join(_base_dir(),'configs','personaPacks')
    fname=os.path.join(pdir,f"{persona_id}.json")
    if not os.path.exists(fname):
        for cand in os.listdir(pdir):
            if cand.startswith(persona_id): fname=os.path.join(pdir,cand); break
    return json.load(open(fname,'r',encoding='utf-8'))
