# My FastAPI Projects Quick Reference

## Project: Orchestrator (CURRENT)
- Location: ~/projects/Orchestrator
- Backend: http://localhost:8000 (Docker)
- Frontend: http://localhost:3000+ (Next.js auto-assigns)
- Start: `docker compose up` + `cd apps/web && npm run dev`
- Services: qdrant(6333), redis(6379), mongo(27017)

## Project 2: [Your Next Project]
- Location: ~/projects/[ProjectName]
- Backend: http://localhost:8001
- Frontend: http://localhost:3100
- Start: [commands here]

## Project 3: [Another Project]
- Location: ~/projects/[ProjectName] 
- Backend: http://localhost:8002
- Frontend: http://localhost:3200
- Start: [commands here]

## Quick Commands:
```bash
# See what's running on ports
lsof -i :8000-8010

# Check Docker containers
docker ps

# Kill a specific port
lsof -ti:8000 | xargs kill -9

# Check Next.js status
curl -I http://localhost:3000
```

## Environment Variables Checklist:
- [ ] .env.local has correct NEXT_PUBLIC_BACKEND_URL
- [ ] Docker ports match between compose and frontend
- [ ] No port conflicts between projects
