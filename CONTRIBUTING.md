# Contributing to Agent Orchestrator

## Development Workflow

### Branch Strategy
- `main` - Production-ready code, protected branch
- `feature/*` - Feature development branches
- `hotfix/*` - Critical bug fixes for production

### Current Feature Branches
- `feature/sadtalker-integration` - Avatar video generation with SadTalker
- `feature/budget-bot-enhancement` - Advanced financial analysis features  
- `feature/advanced-capabilities` - General improvements and new tools

### Getting Started

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd Orchestrator
   cp .env.template apps/server/.env
   # Fill in your API keys in apps/server/.env
   ```

2. **Environment Setup**
   ```bash
   # Start services
   docker-compose up -d
   
   # Seed knowledge base
   cd apps/server && python scripts/embed_upsert.py
   
   # Run tests
   python test_system.py
   ```

3. **Development**
   ```bash
   # Create feature branch
   git checkout -b feature/your-feature-name
   
   # Make changes...
   
   # Test your changes
   python test_system.py
   
   # Commit and push
   git add .
   git commit -m "feat: description of your feature"
   git push origin feature/your-feature-name
   ```

### Environment Variables
- Copy `.env.template` to `apps/server/.env`
- Required: `OPENAI_API_KEY`, `OPENAI_ORG_ID`
- Service URLs are pre-configured for Docker Compose

### Testing
- Run `python test_system.py` before committing
- All tests must pass for merge approval
- Add tests for new features

### Code Standards
- Use meaningful commit messages
- Follow existing code structure
- Document new tools and endpoints
- Maintain security - never commit secrets

### Security
- `.env` files are gitignored - never commit API keys
- Use `.env.template` for documentation
- Sensitive config goes in environment variables only

### Architecture
- **Backend**: FastAPI with tool-based architecture
- **Frontend**: Next.js with real-time chat
- **Vector DB**: Qdrant for RAG search
- **Cache**: Redis for session management  
- **Database**: MongoDB for document storage
- **Deployment**: Docker Compose for all services

### Adding New Tools
1. Create tool file in `apps/server/server/tools/`
2. Implement tool contract (name, description, execute)
3. Add to `tools/__init__.py`
4. Update orchestrate.py tool execution
5. Add test cases to test_system.py

### Adding New Personas
1. Create persona config in `configs/personaPacks/`
2. Define tool access permissions
3. Set conversation style and context
4. Test with orchestrate endpoint

### Next Features
- SadTalker avatar integration
- Advanced budget analysis algorithms
- Real-time collaboration features
- Enhanced security and authentication
