from typing import Dict, Any, List

def offer_preview(user_id: str, product_id: str) -> Dict[str, Any]:
    """Generate personalized payment/product offer preview"""
    
    # Mock product catalog
    products = {
        "premium_checking": {
            "name": "Premium Checking Account",
            "type": "checking",
            "monthly_fee": 15.00,
            "benefits": ["No ATM fees", "Priority customer service", "Mobile check deposit"],
            "requirements": {"min_balance": 1000}
        },
        "auto_loan": {
            "name": "Auto Loan",
            "type": "loan", 
            "rate": 4.5,
            "terms": ["36 months", "48 months", "60 months"],
            "max_amount": 50000
        },
        "credit_card": {
            "name": "Rewards Credit Card",
            "type": "credit",
            "apr": 18.9,
            "credit_limit": 5000,
            "rewards": "2% cash back on groceries, 1% on everything else"
        }
    }
    
    product = products.get(product_id)
    if not product:
        return {"error": "Product not found", "available_products": list(products.keys())}
    
    # Mock personalization based on user
    personalized_offer = {
        "user_id": user_id,
        "product_id": product_id,
        "product": product,
        "personalized_terms": {
            "approved_amount": 45000 if product["type"] == "loan" else None,
            "approved_rate": 4.2 if product["type"] == "loan" else product.get("rate"),
            "special_promotion": "No fees for first 6 months" if product["type"] == "checking" else None,
            "credit_limit": 7500 if product["type"] == "credit" else None
        },
        "eligibility": {
            "status": "pre_approved",
            "confidence": 0.92,
            "factors": ["Good credit score", "Existing customer", "Stable income"]
        },
        "next_steps": [
            "Complete online application",
            "Provide income verification", 
            "Schedule appointment for final approval"
        ]
    }
    
    return personalized_offer

def process_payment(user_id: str, amount: float, from_account: str, to_account: str) -> Dict[str, Any]:
    """Process a payment between accounts - mock implementation"""
    transaction_id = f"TXN-{hash(f'{user_id}{amount}{from_account}{to_account}') % 1000000:06d}"
    
    return {
        "transaction_id": transaction_id,
        "user_id": user_id,
        "amount": amount,
        "from_account": from_account,
        "to_account": to_account,
        "status": "completed",
        "processed_at": "2025-08-17T15:40:00Z",
        "fee": 0.0,
        "confirmation": f"Payment of ${amount:.2f} successfully transferred"
    }
