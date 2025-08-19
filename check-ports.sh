#!/bin/bash

echo "=== PORT CHECKER SCRIPT ==="
echo "Checking common development ports..."
echo

# Function to check if port is in use
check_port() {
    local port=$1
    local service=$2
    if lsof -i :$port > /dev/null 2>&1; then
        echo "✅ Port $port ($service): RUNNING"
        lsof -i :$port | grep LISTEN | head -1
    else
        echo "❌ Port $port ($service): FREE"
    fi
    echo
}

# Check common ports
check_port 3000 "Next.js (default)"
check_port 3001 "Next.js (alt)"
check_port 3002 "Next.js (alt)"
check_port 8000 "FastAPI (Orchestrator)"
check_port 8001 "FastAPI (Project 2)"
check_port 8002 "FastAPI (Project 3)"
check_port 6333 "Qdrant"
check_port 6379 "Redis"
check_port 27017 "MongoDB"

echo "=== DOCKER CONTAINERS ==="
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "Docker not running or accessible"

echo
echo "=== QUICK COMMANDS ==="
echo "Kill a port: lsof -ti:8000 | xargs kill -9"
echo "Start Orchestrator: docker compose up"
echo "Start Next.js: cd apps/web && npm run dev"
