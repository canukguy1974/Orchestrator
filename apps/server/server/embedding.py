import hashlib, math, requests
from typing import List
from . import config
DIM=config.EMBED_DIM

def _hash_token(t:str)->int: return int(hashlib.sha256(t.encode('utf-8')).hexdigest(),16)

def _hash_embed(text:str, dim:int=DIM)->List[float]:
    vec=[0.0]*dim
    toks=text.lower().split()
    if not toks: return vec
    for tok in toks:
        h=_hash_token(tok); idx=h%dim; val=((h>>8)%1000)/1000.0
        vec[idx]+=val
    norm=math.sqrt(sum(v*v for v in vec)) or 1.0
    return [v/norm for v in vec]

def embed_text(text:str)->List[float]:
    prov=config.EMBED_PROVIDER
    if prov=='hash': return _hash_embed(text,DIM)
    if prov=='openrouter':
        import requests
        url='https://openrouter.ai/api/v1/embeddings'; headers={'Authorization':f'Bearer {config.OPENROUTER_API_KEY}'}; payload={'model':config.EMBEDDING_MODEL,'input':text}
        r=requests.post(url,headers=headers,json=payload,timeout=30); r.raise_for_status(); return r.json()['data'][0]['embedding']
    if prov=='openai':
        import requests
        url='https://api.openai.com/v1/embeddings'; headers={'Authorization':f'Bearer {config.OPENAI_API_KEY}'}; payload={'model':config.EMBEDDING_MODEL,'input':text}
        r=requests.post(url,headers=headers,json=payload,timeout=30); r.raise_for_status(); return r.json()['data'][0]['embedding']
    return _hash_embed(text,DIM)
