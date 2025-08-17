from fastapi import APIRouter
from server import config
import requests
from qdrant_client import QdrantClient
import redis
from pymongo import MongoClient

router = APIRouter()


@router.get('/diagnostics')
def diagnostics():
    results = {}
    # Qdrant
    try:
        client = QdrantClient(url=config.QDRANT_URL)
        # simple ping: get collections (may raise on bad connection)
        names = []
        try:
            col_resp = client.get_collections()
            # qdrant-client returns an object with collections attr in newer versions
            names = col_resp.collections if hasattr(col_resp, 'collections') else []
        except Exception:
            # fallback: call http endpoint
            try:
                r = requests.get(config.QDRANT_URL + '/collections', timeout=5)
                r.raise_for_status()
                names = r.json().get('collections', [])
            except Exception:
                names = []
        results['qdrant'] = {'ok': True, 'collections_count': len(names)}
    except Exception as e:
        results['qdrant'] = {'ok': False, 'error': str(e)}

    # Redis
    try:
        r = redis.from_url(config.REDIS_URL)
        pong = r.ping()
        results['redis'] = {'ok': bool(pong)}
    except Exception as e:
        results['redis'] = {'ok': False, 'error': str(e)}

    # Mongo
    try:
        mc = MongoClient(config.MONGO_URI, serverSelectionTimeoutMS=3000)
        mc.server_info()
        results['mongo'] = {'ok': True}
    except Exception as e:
        results['mongo'] = {'ok': False, 'error': str(e)}

    # Embedding provider test (hash always OK; for openai/openrouter do a small call if keys present)
    try:
        prov = config.EMBED_PROVIDER
        if prov == 'hash':
            results['embedding'] = {'ok': True, 'provider': 'hash'}
        elif prov == 'openrouter':
            if not config.OPENROUTER_API_KEY:
                results['embedding'] = {'ok': False, 'error': 'OPENROUTER_API_KEY not set'}
            else:
                url = 'https://openrouter.ai/api/v1/embeddings'
                headers = {'Authorization': f'Bearer {config.OPENROUTER_API_KEY}'}
                payload = {'model': config.EMBEDDING_MODEL, 'input': 'ping'}
                r = requests.post(url, headers=headers, json=payload, timeout=10)
                r.raise_for_status()
                results['embedding'] = {'ok': True, 'provider': 'openrouter'}
        elif prov == 'openai':
            if not config.OPENAI_API_KEY:
                results['embedding'] = {'ok': False, 'error': 'OPENAI_API_KEY not set'}
            else:
                url = 'https://api.openai.com/v1/embeddings'
                headers = {'Authorization': f'Bearer {config.OPENAI_API_KEY}'}
                payload = {'model': config.EMBEDDING_MODEL, 'input': 'ping'}
                r = requests.post(url, headers=headers, json=payload, timeout=10)
                r.raise_for_status()
                results['embedding'] = {'ok': True, 'provider': 'openai'}
        else:
            results['embedding'] = {'ok': False, 'error': f'unknown provider: {prov}'}
    except Exception as e:
        results['embedding'] = {'ok': False, 'error': str(e)}

    return results
