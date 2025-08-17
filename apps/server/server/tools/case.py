from typing import Dict, Any, List
import uuid

def create(user_id: str, case_type: str, description: str, priority: str = "medium") -> Dict[str, Any]:
    """Create a new support case"""
    case_id = f"CASE-{uuid.uuid4().hex[:8].upper()}"
    
    return {
        "case_id": case_id,
        "user_id": user_id,
        "type": case_type,
        "description": description,
        "priority": priority,
        "status": "open",
        "created_at": "2025-08-17T15:30:00Z",
        "assigned_to": "support_team",
        "estimated_resolution": "24-48 hours" if priority == "high" else "3-5 business days"
    }

def get_status(case_id: str) -> Dict[str, Any]:
    """Get case status - mock implementation"""
    return {
        "case_id": case_id,
        "status": "in_progress",
        "last_updated": "2025-08-17T14:20:00Z",
        "updates": [
            {"timestamp": "2025-08-17T14:20:00Z", "note": "Case assigned to specialist"},
            {"timestamp": "2025-08-17T13:45:00Z", "note": "Initial review completed"}
        ]
    }

def escalate(case_id: str, reason: str) -> Dict[str, Any]:
    """Escalate a case to higher tier support"""
    return {
        "case_id": case_id,
        "action": "escalated",
        "reason": reason,
        "new_priority": "high",
        "escalated_to": "senior_support",
        "updated_at": "2025-08-17T15:35:00Z"
    }
