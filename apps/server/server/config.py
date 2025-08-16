import os
from dotenv import load_dotenv
load_dotenv()
MONGO_URI=os.getenv('MONGO_URI','mongodb://localhost:27017/agent_mvp')
REDIS_URL=os.getenv('REDIS_URL','redis://localhost:6379/0')
QDRANT_URL=os.getenv('QDRANT_URL','http://localhost:6333')
EMBED_PROVIDER=os.getenv('EMBED_PROVIDER','hash')
EMBED_DIM=int(os.getenv('EMBED_DIM','512'))
EMBEDDING_MODEL=os.getenv('EMBEDDING_MODEL','text-embedding-3-small')
OPENROUTER_API_KEY=os.getenv('OPENROUTER_API_KEY','')
OPENAI_API_KEY=os.getenv('OPENAI_API_KEY','')
LOG_LEVEL=os.getenv('LOG_LEVEL','INFO')
COLLECTION_NAME=os.getenv('COLLECTION_NAME','docs')
