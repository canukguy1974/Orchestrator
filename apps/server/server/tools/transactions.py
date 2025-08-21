"""
Transaction Generator for Banking Demo
Generates realistic transaction data for testing and development
"""

import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class Transaction:
    id: str
    date: str
    description: str
    amount: float
    category: str
    merchant: str = ""
    method: str = "card"
    currency: str = "CAD"
    running_balance: float = 0.0


class TransactionGenerator:
    def __init__(self, initial_balance: float = 2500.0):
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        
        # Transaction categories with typical amounts and frequency weights
        self.categories = {
            "Groceries": {
                "merchants": ["Metro", "Loblaws", "Sobeys", "FreshCo", "Farm Boy"],
                "amount_range": (25, 150),
                "frequency": 8,  # times per month
                "type": "debit"
            },
            "Gas": {
                "merchants": ["Petro-Canada", "Shell", "Esso", "Ultramar", "Canadian Tire Gas"],
                "amount_range": (45, 85),
                "frequency": 4,
                "type": "debit"
            },
            "Restaurants": {
                "merchants": ["Tim Hortons", "McDonald's", "Subway", "Pizza Pizza", "Local Bistro"],
                "amount_range": (8, 65),
                "frequency": 6,
                "type": "debit"
            },
            "Coffee": {
                "merchants": ["Tim Hortons", "Starbucks", "Second Cup", "Country Style"],
                "amount_range": (3, 12),
                "frequency": 15,
                "type": "debit"
            },
            "Utilities": {
                "merchants": ["Hydro One", "Enbridge Gas", "Bell Canada", "Rogers"],
                "amount_range": (75, 200),
                "frequency": 1,
                "type": "debit"
            },
            "Income": {
                "merchants": ["Payroll Deposit", "Direct Deposit", "Salary"],
                "amount_range": (2500, 3500),
                "frequency": 2,  # bi-weekly
                "type": "credit"
            },
            "Entertainment": {
                "merchants": ["Cineplex", "Netflix", "Spotify", "Steam", "Amazon Prime"],
                "amount_range": (10, 45),
                "frequency": 3,
                "type": "debit"
            },
            "Shopping": {
                "merchants": ["Amazon", "Walmart", "Canadian Tire", "Best Buy", "The Bay"],
                "amount_range": (20, 200),
                "frequency": 4,
                "type": "debit"
            },
            "Healthcare": {
                "merchants": ["Pharmacy", "Dental Clinic", "Medical Clinic", "Physio Clinic"],
                "amount_range": (25, 150),
                "frequency": 2,
                "type": "debit"
            },
            "Transfer": {
                "merchants": ["E-Transfer", "Bill Payment", "Internal Transfer"],
                "amount_range": (50, 500),
                "frequency": 3,
                "type": "debit"
            }
        }
        
        # Payment methods
        self.payment_methods = ["card", "debit", "credit", "etransfer", "bill_payment"]

    def generate_transaction(self, date: datetime, category: str = None) -> Transaction:
        """Generate a single realistic transaction"""
        
        if category is None:
            # Weighted random selection based on frequency
            weights = [cat["frequency"] for cat in self.categories.values()]
            category = random.choices(list(self.categories.keys()), weights=weights)[0]
        
        cat_info = self.categories[category]
        
        # Generate amount
        min_amt, max_amt = cat_info["amount_range"]
        amount = round(random.uniform(min_amt, max_amt), 2)
        
        # Make debits negative
        if cat_info["type"] == "debit":
            amount = -amount
            
        # Select merchant
        merchant = random.choice(cat_info["merchants"])
        
        # Create description
        if category == "Income":
            description = f"{merchant}"
        else:
            description = f"{merchant} - {category}"
            
        # Select payment method
        method = random.choice(self.payment_methods)
        
        # Update running balance
        self.current_balance += amount
        
        return Transaction(
            id=str(uuid.uuid4()),
            date=date.strftime("%Y-%m-%d"),
            description=description,
            amount=amount,
            category=category,
            merchant=merchant,
            method=method,
            currency="CAD",
            running_balance=round(self.current_balance, 2)
        )

    def generate_monthly_transactions(self, start_date: datetime) -> List[Transaction]:
        """Generate transactions for one month"""
        transactions = []
        current_date = start_date
        end_date = start_date + timedelta(days=30)
        
        while current_date < end_date:
            # Determine how many transactions for this day (0-3, weighted toward 1-2)
            daily_tx_count = random.choices([0, 1, 2, 3], weights=[20, 40, 30, 10])[0]
            
            for _ in range(daily_tx_count):
                # Add some random time to the date
                tx_time = current_date + timedelta(
                    hours=random.randint(6, 22),
                    minutes=random.randint(0, 59)
                )
                
                transaction = self.generate_transaction(tx_time)
                transactions.append(transaction)
            
            current_date += timedelta(days=1)
        
        return transactions

    def generate_transactions(self, start_date: str, months: int = 3) -> List[Dict[str, Any]]:
        """Generate transactions for multiple months"""
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        all_transactions = []
        
        for month in range(months):
            month_start = start_dt + timedelta(days=30 * month)
            monthly_transactions = self.generate_monthly_transactions(month_start)
            all_transactions.extend(monthly_transactions)
        
        # Sort by date (oldest first)
        all_transactions.sort(key=lambda x: x.date)
        
        # Convert to dictionaries
        return [asdict(transaction) for transaction in all_transactions]


# Global generator instance
transaction_generator = TransactionGenerator()


def reset_generator(initial_balance: float = 2500.0):
    """Reset the generator with a new initial balance"""
    global transaction_generator
    transaction_generator = TransactionGenerator(initial_balance)


def get_transactions(start_date: str = "2025-05-01", months: int = 3) -> List[Dict[str, Any]]:
    """Generate and return transactions"""
    reset_generator()  # Reset for consistent data
    return transaction_generator.generate_transactions(start_date, months)


if __name__ == "__main__":
    # Test the generator
    transactions = get_transactions("2025-05-01", 3)
    print(f"Generated {len(transactions)} transactions")
    
    # Show first few transactions
    for tx in transactions[:5]:
        print(f"{tx['date']} | {tx['description']} | ${tx['amount']:.2f} | Balance: ${tx['running_balance']:.2f}")
