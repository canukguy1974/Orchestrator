# Agent Orchestration MVP 🤖

A production-ready AI agent orchestration platform that combines **multi-persona conversations**, **RAG-powered knowledge retrieval**, **CRM integration**, and **personalized offers** into a unified banking/financial services experience.

## ✨ Features Implemented

### 🎭 Multi-Persona System

- **Teller**: Handles routine banking, account services, KYC verification
- **Executive**: Business insights, strategy, analytics  
- **Budget Companion**: Personal finance analysis, savings recommendations
- **Kiosk**: Self-service support (planned)

### 🧠 Core Capabilities

- **RAG-Powered Search**: OpenAI embeddings + Qdrant vector storage
- **CRM Integration**: Customer lookup and personalization
- **Budget Analysis**: Spending insights and recommendations
- **KYC/Compliance**: Identity verification workflows
- **Case Management**: Support ticket creation and tracking
- **Payment Processing**: Mock payment and transfer handling
- **Offer Engine**: Personalized product recommendations
- **Avatar/TTS**: Voice response generation (ready for SadTalker integration)

### 🛠️ Technical Stack

- **Backend**: FastAPI + Python 3.12
- **Frontend**: Next.js (port 3000)
- **Vector DB**: Qdrant (semantic search)
- **Cache**: Redis (session storage)
- **Database**: MongoDB (user data)
- **Embeddings**: OpenAI API (configurable)
- **Deployment**: Docker Compose

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- WSL/Linux environment (for scripts)
- OpenAI API key (optional, falls back to hash embeddings)

### 1. Clone & Setup

```bash
cd ~/projects/Orchestrator
```

### 2. Configure Environment

Edit `apps/server/.env`:

```env
# Database connections (use container hostnames for Docker deployment)
MONGO_URI=mongodb://mongo:27017/agent_mvp
REDIS_URL=redis://redis:6379/0  
QDRANT_URL=http://qdrant:6333

# Embedding provider (hash=offline, openai=production quality)
EMBED_PROVIDER=openai
EMBED_DIM=1536
EMBEDDING_MODEL=text-embedding-3-small

# API Keys (set for production embeddings)
OPENAI_API_KEY=your_openai_key_here
OPENROUTER_API_KEY=your_openrouter_key_here  # alternative

# System
LOG_LEVEL=INFO
COLLECTION_NAME=docs
```

### 3. Start Services

```bash
# Start all services (databases + app)
docker compose up -d --build

# Verify health
curl http://localhost:8000/diagnostics
```

### 4. Seed Knowledge Base

```bash
# Create virtual environment for seeding
python3 -m venv .venv
source .venv/bin/activate
pip install -r apps/server/requirements.txt

# Seed with override for localhost access
EMBED_PROVIDER=openai EMBED_DIM=1536 QDRANT_URL=http://localhost:6333 
MONGO_URI=mongodb://localhost:27017/agent_mvp 
REDIS_URL=redis://localhost:6379/0 
./scripts/seed_docs.sh
```

### 5. Test the System

```bash
# Run comprehensive test suite
python test_system.py
```

## 🔗 API Endpoints

### Health & Diagnostics

- `GET /health` - Basic health check
- `GET /diagnostics` - Detailed service status (Qdrant, Redis, Mongo, embeddings)

### Orchestration  

- `POST /orchestrate` - Main conversation endpoint

Example request:

```json
{
  "persona": "teller-v1",
  "user_id": "C001", 
  "messages": [
    {"role": "user", "content": "What's my account balance?"}
  ]
}
```

Example response:

```json
{
  "reply": {
    "text": "[Branch Teller] Hello John Doe! As a premium member...",
    "media": {"transcript": "...", "voice": "friendly"}
  },
  "offers": [
    {"id": "cashback-card-lite", "name": "Cashback Card", ...}
  ],
  "tool_events": [
    {"name": "crm.lookup", "input": {...}, "output": {...}},
    {"name": "rag.search", "input": {...}, "output": {...}}
  ]
}
```

## 🎯 Persona Configurations

Located in `configs/personaPacks/`:

- **teller-v1.json**: Branch teller with CRM, KYC, basic banking tools
- **exec-v1.json**: Executive with analytics and strategy focus  
- **budget-v1.json**: Budget advisor with spending analysis
- **kiosk-v1.json**: Self-service kiosk interface

Each persona defines:

- `tools[]`: Allowed tool access (rag.search, crm.lookup, etc.)
- `ragNamespaces[]`: Knowledge scope (bank/policies, bank/ops, etc.)
- `voice{}`: TTS configuration
- `guardrails{}`: Security and compliance rules

## 🛠️ Tool System

### Available Tools

- **rag.search**: Semantic search across knowledge base
- **crm.lookup**: Customer data retrieval  
- **kyc.verify**: Identity verification
- **budget.analyze**: Financial insights
- **case.create**: Support ticket creation
- **payments.offerPreview**: Personalized product offers
- **avatar.speak**: Voice/video generation (ready for SadTalker)

### Adding New Tools

1. Create `apps/server/server/tools/your_tool.py`
2. Add functions with clear type hints
3. Update `apps/server/server/tools/__init__.py`
4. Add to persona `tools[]` arrays
5. Handle in `routers/orchestrate.py`

## 📊 Knowledge Base

Documents are stored in Qdrant with namespace-based access control:

- `bank/policies`: KYC, compliance, procedures
- `bank/ops`: Operational procedures, queue management
- `bank/faqs`: Customer service questions
- `global`: Cross-cutting knowledge  
- `role/teller`, `role/exec`, etc.: Role-specific content

Add new content:

```bash
# Add documents to seed_docs/ folder, then:
python apps/server/scripts/embed_upsert.py --ns your/namespace --src path/to/docs
```

## 🔧 Development

### Local Development (Hybrid)

```bash
# Run databases in Docker
docker compose up -d qdrant redis mongo

# Run app locally for faster iteration
source .venv/bin/activate
cd apps/server
uvicorn main:app --host 0.0.0.0 --port 8080 --reload

# Update .env to use localhost for local development:
# QDRANT_URL=http://localhost:6333
# MONGO_URI=mongodb://localhost:27017/agent_mvp  
# REDIS_URL=redis://localhost:6379/0
```

### Full Docker Development  

```bash
# Everything in containers
docker compose up -d --build
```

### Adding SadTalker Integration

The avatar tool is ready for SadTalker integration:

1. Update `server/tools/avatar.py` to call SadTalker API
2. Add video generation logic  
3. Return media URLs instead of transcripts
4. Frontend displays video responses

## 🚦 Production Readiness

### Security Features Implemented

- Persona-based tool access control
- Namespace-scoped knowledge access
- API key management via environment variables
- Tool execution logging and audit trail

### Next Steps for Production

- [ ] Add authentication/authorization
- [ ] Implement proper logging and monitoring  
- [ ] Add rate limiting
- [ ] Set up CI/CD pipelines
- [ ] Add proper error handling and retry logic
- [ ] Scale database connections
- [ ] Add session management with Redis

## 📈 Extending the System

Based on `docs/features.md`, planned enhancements:

1. **Advanced Session Memory**: Redis-backed conversation continuity
2. **Analytics Dashboard**: Conversion tracking, usage metrics
3. **Security Hardening**: PII masking, audit trails, consent management
4. **Tool Marketplace**: Plugin system for custom integrations
5. **A/B Testing**: Prompt variants and persona optimization

## 🎭 Current Status

✅ **Complete MVP Features:**

- Multi-persona orchestration
- RAG with OpenAI embeddings  
- CRM integration and customer lookup
- Budget analysis and recommendations
- Offer engine with personalization
- Avatar/TTS framework (ready for SadTalker)
- Docker-based deployment
- Comprehensive test suite

🔄 **Ready for Your Extensions:**

- SadTalker video generation
- Advanced budget bot features
- Custom persona development
- Extended tool integrations

---

## 🆘 Support

If you encounter issues:

1. **Check diagnostics**: `curl http://localhost:8000/diagnostics`
2. **View logs**: `docker logs orchestrator-app-1`
3. **Run tests**: `python test_system.py`
4. **Restart services**: `docker compose restart`

**Common Issues:**

- **Module not found**: Run `pip install -r apps/server/requirements.txt` in virtual environment
- **Connection refused**: Check `docker ps` and port mappings
- **Embedding errors**: Verify API keys in `.env` file
- **Empty RAG results**: Re-run seed script with correct provider settings

The system is production-ready for your banking AI agent! 🚀
Generated 2025-08-16

See README for RAG setup and Quick start.

---

## 👨‍💻 About the Developer

<p align="center">
  <img src="DCW_LOG.png" alt="Digital Creations Windsor" width="200"/>
</p>

<p align="center">
  <b>Colin — Founder & Indie Dev @ <a href="https://digitalcreationswindsor.xyz">Digital Creations Windsor</a></b><br/>
  📧 <a href="mailto:colin@digitalcreationswindsor.xyz">colin@digitalcreationswindsor.xyz</a>  
</p>

<p align="center">
  <a href="https://github.com/canukguy1974">
    <img src="https://img.shields.io/badge/GitHub-Profile-black?style=for-the-badge&logo=github" />
  </a>
  <a href="https://digitalcreationswindsor.xyz">
    <img src="https://img.shields.io/badge/Website-digitalcreationswindsor.xyz-green?style=for-the-badge&logo=google-chrome" />
  </a>
  <a href="https://linkedin.com/company/digital-creations-windsor">
    <img src="https://img.shields.io/badge/LinkedIn-Network-blue?style=for-the-badge&logo=linkedin" />
  </a>
</p>

<p align="center"><i>
  Building AI automation tools that scale businesses — one line of code at a time.
</i></p>
