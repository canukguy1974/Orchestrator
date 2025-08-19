# Project Configuration & Testing Guide

## 🏗️ Current Docker Setup

### Services Overview
Based on your `docker-compose.yml`, you have 4 services running:

| Service | Container Name | Host Port | Container Port | Purpose |
|---------|---------------|-----------|----------------|---------|
| **app** | orchestrator-app-1 | 8000 | 8000 | FastAPI Backend |
| **qdrant** | orchestrator-qdrant-1 | 6333, 6334 | 6333, 6334 | Vector Database |
| **redis** | orchestrator-redis-1 | 6379 | 6379 | Cache/Session Store |
| **mongo** | orchestrator-mongo-1 | 27017 | 27017 | Document Database |

### Frontend
- **Next.js**: Auto-assigns port (3000, 3001, 3002, etc.)
- **Environment**: `.env.local` with `NEXT_PUBLIC_BACKEND_URL=http://localhost:8000`

---

## 🧪 Step-by-Step Testing Plan

### Step 1: Verify Docker Container Status
```bash
# Check all containers are running
docker ps

# Check container logs if needed
docker logs orchestrator-app-1
docker logs orchestrator-redis-1
docker logs orchestrator-qdrant-1
docker logs orchestrator-mongo-1
```

### Step 2: Test Each Service Individually

#### 🔧 **Redis Testing**
```bash
# Test 1: Basic connection
redis-cli -h localhost -p 6379 ping
# Expected: PONG

# Test 2: Set and get a value
redis-cli -h localhost -p 6379 set test-key "hello-redis"
redis-cli -h localhost -p 6379 get test-key
# Expected: "hello-redis"

# Test 3: Check Redis info
redis-cli -h localhost -p 6379 info server
```

#### 🗄️ **MongoDB Testing**
```bash
# Test 1: Check if MongoDB is responding
curl -s http://localhost:27017
# Expected: "It looks like you are trying to access MongoDB over HTTP..."

# Test 2: Connect with mongo shell (if installed)
mongosh --host localhost --port 27017
# Then in mongo shell:
# show dbs
# exit
```

#### 🧠 **Qdrant Testing**
```bash
# Test 1: Check Qdrant health
curl http://localhost:6333/
# Expected: JSON response with version info

# Test 2: Check collections
curl http://localhost:6333/collections
# Expected: {"result": {...}}

# Test 3: Get cluster info
curl http://localhost:6333/cluster
```

#### 🚀 **FastAPI Backend Testing**
```bash
# Test 1: Health check
curl http://localhost:8000/
# Expected: JSON response (might be 404, that's ok)

# Test 2: Check docs (if available)
curl -I http://localhost:8000/docs
# Expected: 200 or 404 status

# Test 3: Test the orchestrate endpoint directly
curl -X POST http://localhost:8000/orchestrate \
  -H "Content-Type: application/json" \
  -d '{"persona":"teller-v1","user_id":"test","messages":[{"role":"user","content":"hello"}]}'
```

### Step 3: Test Full Stack Integration
```bash
# Test the Next.js API route (after starting npm run dev)
curl -X POST http://localhost:3002/api/orchestrate \
  -H "Content-Type: application/json" \
  -d '{"persona":"teller-v1","user_id":"test","messages":[{"role":"user","content":"hello"}]}'
```

---

## 🔍 Expected Results & Troubleshooting

### ✅ Success Indicators
- **Redis**: Returns `PONG` and can store/retrieve values
- **MongoDB**: Shows connection message or database list
- **Qdrant**: Returns JSON with version/collection info
- **FastAPI**: Returns proper JSON responses (not HTML error pages)
- **Next.js**: Successfully proxies requests to backend

### ❌ Common Issues & Fixes
- **Connection Refused**: Service isn't running → Check `docker ps`
- **404 Errors**: Wrong endpoint → Verify URL and HTTP method
- **JSON Parse Errors**: Wrong content-type → Add `-H "Content-Type: application/json"`
- **Port Conflicts**: Run `./check-ports.sh` to see what's using which ports

---

## 📝 Environment Variables Checklist

Before going live, verify these are set correctly:

### Backend (.env in apps/server/)
```bash
# Database connections
MONGODB_URL=mongodb://mongo:27017/orchestrator
REDIS_URL=redis://redis:6379
QDRANT_URL=http://qdrant:6333

# API Keys (set these for production)
OPENAI_API_KEY=your_openai_key_here
# Add other API keys as needed
```

### Frontend (.env.local in apps/web/)
```bash
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

---

## 🎯 Quick Commands Reference

```bash
# Start everything
docker compose up -d

# Check what's running
./check-ports.sh

# Start frontend
cd apps/web && npm run dev

# View logs
docker compose logs -f

# Restart a specific service
docker compose restart app

# Stop everything
docker compose down
```

---

## 🚦 Testing Status Tracker

- [ ] Docker containers all running
- [ ] Redis responding to ping
- [ ] MongoDB accessible
- [ ] Qdrant API responding
- [ ] FastAPI backend responding
- [ ] Next.js frontend connecting to backend
- [ ] Environment variables configured
- [ ] Ready for production testing
