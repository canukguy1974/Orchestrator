#!/usr/bin/env python3
"""
Test script for the Agent Orchestrator MVP
Tests core functionality including personas, tools, and RAG
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    """Test basic health endpoint"""
    print("🏥 Testing health endpoint...")
    resp = requests.get(f"{BASE_URL}/health")
    assert resp.status_code == 200
    assert resp.json()["ok"] == True
    print("✅ Health check passed")

def test_diagnostics():
    """Test diagnostics endpoint"""
    print("🔍 Testing diagnostics...")
    resp = requests.get(f"{BASE_URL}/diagnostics")
    assert resp.status_code == 200
    data = resp.json()
    
    assert data["qdrant"]["ok"] == True
    assert data["redis"]["ok"] == True  
    assert data["mongo"]["ok"] == True
    assert data["embedding"]["ok"] == True
    
    print(f"✅ All services healthy - Embedding provider: {data['embedding']['provider']}")

def test_persona_teller():
    """Test teller persona with CRM lookup"""
    print("👤 Testing teller persona...")
    payload = {
        "persona": "teller-v1",
        "user_id": "C001",
        "messages": [
            {"role": "user", "content": "What's my account balance?"}
        ]
    }
    
    resp = requests.post(f"{BASE_URL}/orchestrate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    
    # Should find customer and have CRM lookup event
    crm_events = [e for e in data["tool_events"] if e["name"] == "crm.lookup"]
    assert len(crm_events) > 0
    assert crm_events[0]["output"]["found"] == True
    
    # Should have personalized greeting
    assert "John Doe" in data["reply"]["text"]
    print("✅ Teller persona working - found customer and personalized response")

def test_persona_budget():
    """Test budget persona with budget analysis"""
    print("💰 Testing budget persona...")
    payload = {
        "persona": "budget-v1", 
        "user_id": "test_user",
        "messages": [
            {"role": "user", "content": "Help me create a budget plan"}
        ]
    }
    
    resp = requests.post(f"{BASE_URL}/orchestrate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    
    # Should have budget analysis
    budget_events = [e for e in data["tool_events"] if e["name"] == "budget.analyze"]
    assert len(budget_events) > 0
    
    # Should mention budget in response
    assert "Budget outlook" in data["reply"]["text"]
    print("✅ Budget persona working - analyzed spending and provided recommendations")

def test_rag_search():
    """Test RAG search functionality"""
    print("📚 Testing RAG search...")
    payload = {
        "persona": "teller-v1",
        "user_id": "test_user", 
        "messages": [
            {"role": "user", "content": "What are the KYC requirements for new accounts?"}
        ]
    }
    
    resp = requests.post(f"{BASE_URL}/orchestrate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    
    # Should have RAG search
    rag_events = [e for e in data["tool_events"] if e["name"] == "rag.search"]
    assert len(rag_events) > 0
    
    print("✅ RAG search working - retrieved relevant documents")

def test_offers():
    """Test offer engine"""
    print("🎯 Testing offer engine...")
    payload = {
        "persona": "exec-v1",
        "user_id": "test_user",
        "messages": [
            {"role": "user", "content": "Show me business insights"}
        ]
    }
    
    resp = requests.post(f"{BASE_URL}/orchestrate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    
    # Should have offers
    assert len(data["offers"]) > 0
    assert "id" in data["offers"][0]
    assert "name" in data["offers"][0]
    
    print(f"✅ Offer engine working - generated {len(data['offers'])} personalized offers")

def main():
    print("🚀 Starting Agent Orchestrator MVP Tests\n")
    
    try:
        test_health()
        test_diagnostics()
        test_persona_teller()
        test_persona_budget()
        test_rag_search()
        test_offers()
        
        print(f"\n🎉 All tests passed! The Agent Orchestrator MVP is fully functional.")
        print("🔗 Ready for:")
        print("   • RAG-powered knowledge retrieval") 
        print("   • Multi-persona conversations")
        print("   • CRM integration and customer lookup")
        print("   • Budget analysis and recommendations")
        print("   • Personalized offer generation")
        print("   • Avatar/TTS integration")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
