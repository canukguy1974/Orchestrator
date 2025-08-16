import argparse, os, sys, uuid
from pathlib import Path
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
THIS_DIR=Path(__file__).resolve().parent; SERVER_DIR=THIS_DIR.parent
if str(SERVER_DIR) not in sys.path: sys.path.insert(0, str(SERVER_DIR))
from server import config
from server.embedding import embed_text

def ensure_collection(client):
    try:
        client.recreate_collection(collection_name=config.COLLECTION_NAME, vectors_config=VectorParams(size=config.EMBED_DIM, distance=Distance.COSINE))
    except Exception: pass

def chunk_text(text,max_len=650):
    words=text.split(); buf=[]; size=0
    for w in words:
        buf.append(w); size+=len(w)+1
        if size>=max_len: yield ' '.join(buf); buf=[]; size=0
    if buf: yield ' '.join(buf)

def files_from_src(src:str):
    p=Path(src)
    if p.is_dir():
        for ext in ('**/*.md','**/*.txt'):
            for f in p.glob(ext): yield f
    else: yield p

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--ns', required=True); ap.add_argument('--src', required=True); args=ap.parse_args()
    client=QdrantClient(url=config.QDRANT_URL); ensure_collection(client)
    points=[]; count=0
    for fp in files_from_src(args.src):
        text=Path(fp).read_text(encoding='utf-8')
        for chunk in chunk_text(text):
            vec=embed_text(chunk); pid=str(uuid.uuid4())
            points.append(PointStruct(id=pid, vector=vec, payload={'text':chunk,'source':str(fp),'namespace':args.ns})); count+=1
    if points: client.upsert(collection_name=config.COLLECTION_NAME, points=points)
    print({'upserted': count, 'namespace': args.ns, 'collection': config.COLLECTION_NAME})
if __name__=='__main__': main()
