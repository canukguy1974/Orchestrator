from typing import Dict, Any, Optional

def lookup(identifier: str) -> Dict[str, Any]:
    """Mock CRM lookup - returns customer data based on identifier"""
    # This would integrate with actual CRM system
    mock_customers = {
        "john.doe@email.com": {
            "customer_id": "C001",
            "name": "John Doe", 
            "email": "john.doe@email.com",
            "phone": "+1-555-0123",
            "segment": "premium",
            "account_since": "2020-03-15",
            "primary_account": "CHK-001-789",
            "balance": 12500.50,
            "products": ["checking", "savings", "credit_card"],
            "last_contact": "2025-08-10",
            "satisfaction_score": 8.7
        },
        "C001": {
            "customer_id": "C001", 
            "name": "John Doe",
            "email": "john.doe@email.com",
            "phone": "+1-555-0123",
            "segment": "premium",
            "account_since": "2020-03-15",
            "primary_account": "CHK-001-789",
            "balance": 12500.50,
            "products": ["checking", "savings", "credit_card"],
            "last_contact": "2025-08-10",
            "satisfaction_score": 8.7
        }
    }
    
    customer = mock_customers.get(identifier)
    if customer:
        return {"found": True, "customer": customer}
    else:
        return {
            "found": False, 
            "customer": None,
            "suggested_actions": ["verify_identifier", "check_spelling", "search_by_phone"]
        }
