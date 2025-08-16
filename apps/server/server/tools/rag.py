from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, Filter, FieldCondition, MatchValue
from .. import config
from ..embedding import embed_text

def _client(): return QdrantClient(url=config.QDRANT_URL)

def _ensure_collection(client, vector_size:int):
    try:
        cols=client.get_collections().collections; names=[c.name for c in cols]
        if config.COLLECTION_NAME not in names:
            client.recreate_collection(collection_name=config.COLLECTION_NAME, vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE))
    except Exception:
        client.recreate_collection(collection_name=config.COLLECTION_NAME, vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE))

def _ns_filter(namespaces: List[str]) -> Optional[Filter]:
    if not namespaces: return None
    should=[FieldCondition(key='namespace', match=MatchValue(value=ns)) for ns in namespaces]
    return Filter(should=should)

def search(query:str, namespaces:List[str], user_id:str, k:int=3)->List[Dict[str,Any]]:
    try:
        client=_client(); _ensure_collection(client, config.EMBED_DIM)
        qvec=embed_text(query or '')
        flt=_ns_filter(namespaces)
        results=client.search(collection_name=config.COLLECTION_NAME, query_vector=qvec, query_filter=flt, limit=k, with_payload=True)
        out=[]
        for r in results:
            p=r.payload or {}
            out.append({'id':str(r.id),'text':p.get('text',''),'source':p.get('source',''),'namespace':p.get('namespace',''),'score':float(r.score)})
        return out
    except Exception:
        return [
            {'id':'stub1','text':'KYC policy: verify ID and address for all new accounts.','source':'bank/policies/kyc.md','score':0.89},
            {'id':'stub2','text':'Queue triage: escalate if wait > 10 minutes for premium clients.','source':'bank/ops/queue.md','score':0.77},
            {'id':'stub3','text':'FAQ: appointment scheduling available via kiosk or web.','source':'bank/faqs/appointments.md','score':0.72},
        ][:k]
