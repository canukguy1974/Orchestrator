"""
Transaction API Router
Handles transaction generation and retrieval endpoints
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

from server.tools.transactions import get_transactions, reset_generator

# Set up logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/transactions", tags=["transactions"])


class GenerateTransactionsRequest(BaseModel):
    start_date: str = "2025-05-01"
    months: int = 3
    initial_balance: Optional[float] = 2500.0


class TransactionResponse(BaseModel):
    transactions: List[Dict[str, Any]]
    count: int
    summary: Dict[str, Any]


@router.get("/", response_model=List[Dict[str, Any]])
async def list_transactions(
    start_date: str = "2025-05-01",
    months: int = 3
):
    """
    Get existing transactions or generate default set
    """
    try:
        transactions = get_transactions(start_date, months)
        logger.info(f"Retrieved {len(transactions)} transactions")
        return transactions
    except Exception as e:
        logger.error(f"Error retrieving transactions: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve transactions: {str(e)}")


@router.post("/generate", response_model=TransactionResponse)
async def generate_transactions(request: GenerateTransactionsRequest):
    """
    Generate new transaction data for testing/demo purposes
    """
    try:
        # Validate date format
        try:
            datetime.strptime(request.start_date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        
        # Validate months
        if request.months < 1 or request.months > 12:
            raise HTTPException(status_code=400, detail="Months must be between 1 and 12")
        
        # Reset generator with new initial balance if provided
        if request.initial_balance:
            reset_generator(request.initial_balance)
        
        # Generate transactions
        transactions = get_transactions(request.start_date, request.months)
        
        # Calculate summary statistics
        total_credits = sum(tx["amount"] for tx in transactions if tx["amount"] > 0)
        total_debits = sum(tx["amount"] for tx in transactions if tx["amount"] < 0)
        final_balance = transactions[-1]["running_balance"] if transactions else 0
        
        summary = {
            "total_transactions": len(transactions),
            "total_credits": round(total_credits, 2),
            "total_debits": round(total_debits, 2),
            "net_change": round(total_credits + total_debits, 2),
            "final_balance": round(final_balance, 2),
            "start_date": request.start_date,
            "months_generated": request.months
        }
        
        logger.info(f"Generated {len(transactions)} transactions from {request.start_date} for {request.months} months")
        
        return TransactionResponse(
            transactions=transactions,
            count=len(transactions),
            summary=summary
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating transactions: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate transactions: {str(e)}")


@router.get("/summary")
async def get_transaction_summary(
    start_date: str = "2025-05-01",
    months: int = 3
):
    """
    Get summary statistics for transactions
    """
    try:
        transactions = get_transactions(start_date, months)
        
        if not transactions:
            return {"message": "No transactions found"}
        
        total_credits = sum(tx["amount"] for tx in transactions if tx["amount"] > 0)
        total_debits = sum(tx["amount"] for tx in transactions if tx["amount"] < 0)
        
        # Category breakdown
        categories = {}
        for tx in transactions:
            cat = tx["category"]
            if cat not in categories:
                categories[cat] = {"count": 0, "total": 0}
            categories[cat]["count"] += 1
            categories[cat]["total"] += tx["amount"]
        
        return {
            "total_transactions": len(transactions),
            "total_credits": round(total_credits, 2),
            "total_debits": round(total_debits, 2),
            "net_change": round(total_credits + total_debits, 2),
            "categories": categories,
            "date_range": {
                "start": transactions[0]["date"],
                "end": transactions[-1]["date"]
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting transaction summary: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get summary: {str(e)}")


@router.delete("/")
async def clear_transactions():
    """
    Clear/reset transaction data
    """
    try:
        reset_generator()
        return {"message": "Transaction data cleared successfully"}
    except Exception as e:
        logger.error(f"Error clearing transactions: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to clear transactions: {str(e)}")
