"""
Employee Onboarding System for Banking AI Assistant
Provides structured onboarding workflows for different bank roles
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import uuid
import json

@dataclass
class OnboardingTask:
    id: str
    title: str
    description: str
    category: str
    estimated_time: int  # minutes
    priority: str  # high, medium, low
    completed: bool = False
    completed_date: Optional[str] = None
    resources: List[str] = None
    
    def __post_init__(self):
        if self.resources is None:
            self.resources = []

@dataclass
class OnboardingProgram:
    id: str
    role: str
    department: str
    duration_days: int
    tasks: List[OnboardingTask]
    progress_percentage: float = 0.0
    
    def calculate_progress(self):
        if not self.tasks:
            return 0.0
        completed_tasks = sum(1 for task in self.tasks if task.completed)
        self.progress_percentage = (completed_tasks / len(self.tasks)) * 100
        return self.progress_percentage

@dataclass
class Employee:
    id: str
    name: str
    email: str
    role: str
    department: str
    start_date: str
    manager: str
    onboarding_program_id: str
    status: str = "active"  # active, completed, paused

class OnboardingGenerator:
    def __init__(self):
        self.programs = {}
        self.employees = {}
        self._initialize_programs()
    
    def _initialize_programs(self):
        """Initialize onboarding programs for different bank roles"""
        
        # Teller Onboarding Program
        teller_tasks = [
            OnboardingTask(
                id=str(uuid.uuid4()),
                title="Banking Systems Overview",
                description="Learn core banking systems: customer management, transaction processing, and security protocols",
                category="Systems Training",
                estimated_time=120,
                priority="high",
                resources=["Banking Systems Manual", "Video Tutorial: Core Banking", "Quiz: System Navigation"]
            ),
            OnboardingTask(
                id=str(uuid.uuid4()),
                title="Customer Service Excellence",
                description="Master customer interaction techniques, complaint handling, and service standards",
                category="Customer Service",
                estimated_time=90,
                priority="high",
                resources=["Customer Service Guide", "Role-play Scenarios", "Communication Standards"]
            ),
            OnboardingTask(
                id=str(uuid.uuid4()),
                title="Cash Handling Procedures",
                description="Learn proper cash handling, balancing procedures, and security protocols",
                category="Operations",
                estimated_time=150,
                priority="high",
                resources=["Cash Handling Manual", "Security Procedures", "Balancing Worksheets"]
            ),
            OnboardingTask(
                id=str(uuid.uuid4()),
                title="Product Knowledge: Basic Banking",
                description="Understand checking accounts, savings accounts, and basic banking products",
                category="Product Training",
                estimated_time=120,
                priority="medium",
                resources=["Product Catalog", "Features Comparison", "Pricing Guidelines"]
            ),
            OnboardingTask(
                id=str(uuid.uuid4()),
                title="Fraud Prevention & Detection",
                description="Identify suspicious activities, fraud indicators, and reporting procedures",
                category="Security",
                estimated_time=90,
                priority="high",
                resources=["Fraud Prevention Guide", "Case Studies", "Reporting Procedures"]
            ),
            OnboardingTask(
                id=str(uuid.uuid4()),
                title="Regulatory Compliance Basics",
                description="Understand BSA/AML requirements, privacy laws, and compliance procedures",
                category="Compliance",
                estimated_time=120,
                priority="high",
                resources=["Compliance Manual", "BSA/AML Training", "Privacy Guidelines"]
            )
        ]
        
        # Personal Banker Onboarding Program
        personal_banker_tasks = [
            OnboardingTask(
                id=str(uuid.uuid4()),
                title="Advanced Banking Systems",
                description="Master CRM systems, loan origination platforms, and analytics tools",
                category="Systems Training",
                estimated_time=180,
                priority="high",
                resources=["CRM User Guide", "Loan Systems Training", "Analytics Dashboard Tutorial"]
            ),
            OnboardingTask(
                id=str(uuid.uuid4()),
                title="Relationship Building Strategies",
                description="Develop skills for building long-term customer relationships and trust",
                category="Relationship Management",
                estimated_time=120,
                priority="high",
                resources=["Relationship Building Guide", "Customer Psychology", "Trust Building Techniques"]
            ),
            OnboardingTask(
                id=str(uuid.uuid4()),
                title="Investment Products Overview",
                description="Learn about investment options, risk assessment, and portfolio basics",
                category="Investment Training",
                estimated_time=240,
                priority="medium",
                resources=["Investment Product Guide", "Risk Assessment Tools", "Portfolio Examples"]
            ),
            OnboardingTask(
                id=str(uuid.uuid4()),
                title="Loan Products & Underwriting",
                description="Understand personal loans, lines of credit, and basic underwriting principles",
                category="Lending",
                estimated_time=180,
                priority="high",
                resources=["Lending Guidelines", "Underwriting Basics", "Credit Analysis"]
            ),
            OnboardingTask(
                id=str(uuid.uuid4()),
                title="Sales Techniques & Goal Setting",
                description="Master consultative selling, needs assessment, and goal achievement strategies",
                category="Sales Training",
                estimated_time=150,
                priority="medium",
                resources=["Sales Methodology", "Needs Assessment Tools", "Goal Setting Framework"]
            )
        ]
        
        # Business Banking Specialist Program
        business_banker_tasks = [
            OnboardingTask(
                id=str(uuid.uuid4()),
                title="Business Banking Systems",
                description="Learn commercial banking platforms, cash management systems, and business tools",
                category="Systems Training",
                estimated_time=240,
                priority="high",
                resources=["Commercial Banking Systems", "Cash Management Guide", "Business Tools Training"]
            ),
            OnboardingTask(
                id=str(uuid.uuid4()),
                title="Commercial Lending Fundamentals",
                description="Understand business loans, lines of credit, equipment financing, and credit analysis",
                category="Commercial Lending",
                estimated_time=300,
                priority="high",
                resources=["Commercial Lending Manual", "Financial Analysis", "Industry Guidelines"]
            ),
            OnboardingTask(
                id=str(uuid.uuid4()),
                title="Cash Management Solutions",
                description="Master treasury services, merchant services, and payment processing solutions",
                category="Treasury Services",
                estimated_time="180",
                priority="medium",
                resources=["Treasury Services Guide", "Payment Solutions", "Merchant Services Manual"]
            ),
            OnboardingTask(
                id=str(uuid.uuid4()),
                title="Business Development Skills",
                description="Learn prospecting techniques, proposal writing, and business relationship management",
                category="Business Development",
                estimated_time=200,
                priority="medium",
                resources=["Business Development Guide", "Proposal Templates", "Prospecting Strategies"]
            )
        ]
        
        self.programs = {
            "teller": OnboardingProgram(
                id="teller-program",
                role="Teller",
                department="Branch Operations",
                duration_days=10,
                tasks=teller_tasks
            ),
            "personal-banker": OnboardingProgram(
                id="personal-banker-program",
                role="Personal Banker",
                department="Retail Banking",
                duration_days=15,
                tasks=personal_banker_tasks
            ),
            "business-banker": OnboardingProgram(
                id="business-banker-program",
                role="Business Banking Specialist",
                department="Commercial Banking",
                duration_days=20,
                tasks=business_banker_tasks
            )
        }
    
    def create_employee(self, name: str, email: str, role: str, department: str, manager: str) -> Employee:
        """Create a new employee with appropriate onboarding program"""
        employee_id = str(uuid.uuid4())
        role_key = role.lower().replace(" ", "-")
        
        # Find matching onboarding program
        program_id = None
        if "teller" in role_key:
            program_id = "teller-program"
        elif "personal" in role_key and "banker" in role_key:
            program_id = "personal-banker-program"
        elif "business" in role_key:
            program_id = "business-banker-program"
        else:
            program_id = "teller-program"  # Default fallback
        
        employee = Employee(
            id=employee_id,
            name=name,
            email=email,
            role=role,
            department=department,
            start_date=datetime.now().strftime("%Y-%m-%d"),
            manager=manager,
            onboarding_program_id=program_id
        )
        
        self.employees[employee_id] = employee
        return employee
    
    def get_employee_onboarding(self, employee_id: str) -> Dict:
        """Get employee's onboarding progress and tasks"""
        if employee_id not in self.employees:
            return {"error": "Employee not found"}
        
        employee = self.employees[employee_id]
        program_key = employee.onboarding_program_id.replace("-program", "")
        
        if program_key not in self.programs:
            return {"error": "Onboarding program not found"}
        
        program = self.programs[program_key]
        program.calculate_progress()
        
        return {
            "employee": employee.__dict__,
            "program": {
                "id": program.id,
                "role": program.role,
                "department": program.department,
                "duration_days": program.duration_days,
                "progress_percentage": program.progress_percentage,
                "tasks": [task.__dict__ for task in program.tasks]
            }
        }
    
    def complete_task(self, employee_id: str, task_id: str) -> Dict:
        """Mark a task as completed for an employee"""
        if employee_id not in self.employees:
            return {"error": "Employee not found"}
        
        employee = self.employees[employee_id]
        program_key = employee.onboarding_program_id.replace("-program", "")
        
        if program_key not in self.programs:
            return {"error": "Onboarding program not found"}
        
        program = self.programs[program_key]
        
        for task in program.tasks:
            if task.id == task_id:
                task.completed = True
                task.completed_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                program.calculate_progress()
                return {"success": True, "task": task.__dict__, "progress": program.progress_percentage}
        
        return {"error": "Task not found"}
    
    def get_all_employees(self) -> List[Dict]:
        """Get all employees and their onboarding status"""
        result = []
        for employee_id, employee in self.employees.items():
            onboarding_data = self.get_employee_onboarding(employee_id)
            if "error" not in onboarding_data:
                result.append({
                    "employee": employee.__dict__,
                    "progress": onboarding_data["program"]["progress_percentage"],
                    "completed_tasks": sum(1 for task in onboarding_data["program"]["tasks"] if task["completed"]),
                    "total_tasks": len(onboarding_data["program"]["tasks"])
                })
        return result
    
    def get_onboarding_analytics(self) -> Dict:
        """Get analytics about onboarding progress across all employees"""
        if not self.employees:
            return {
                "total_employees": 0,
                "average_progress": 0,
                "completion_rate": 0,
                "by_role": {}
            }
        
        total_progress = 0
        completed_count = 0
        role_stats = {}
        
        for employee_id, employee in self.employees.items():
            onboarding_data = self.get_employee_onboarding(employee_id)
            if "error" not in onboarding_data:
                progress = onboarding_data["program"]["progress_percentage"]
                total_progress += progress
                
                if progress >= 100:
                    completed_count += 1
                
                role = employee.role
                if role not in role_stats:
                    role_stats[role] = {"count": 0, "total_progress": 0, "completed": 0}
                
                role_stats[role]["count"] += 1
                role_stats[role]["total_progress"] += progress
                if progress >= 100:
                    role_stats[role]["completed"] += 1
        
        # Calculate averages
        employee_count = len(self.employees)
        for role in role_stats:
            if role_stats[role]["count"] > 0:
                role_stats[role]["average_progress"] = role_stats[role]["total_progress"] / role_stats[role]["count"]
                role_stats[role]["completion_rate"] = (role_stats[role]["completed"] / role_stats[role]["count"]) * 100
        
        return {
            "total_employees": employee_count,
            "average_progress": total_progress / employee_count if employee_count > 0 else 0,
            "completion_rate": (completed_count / employee_count) * 100 if employee_count > 0 else 0,
            "by_role": role_stats
        }

# Global instance
onboarding_generator = OnboardingGenerator()

# Demo data - create some sample employees
def create_demo_employees():
    employees = [
        ("Sarah Johnson", "sarah.johnson@bank.com", "Teller", "Branch Operations", "Mike Chen"),
        ("David Rodriguez", "david.rodriguez@bank.com", "Personal Banker", "Retail Banking", "Lisa Wang"),
        ("Emma Thompson", "emma.thompson@bank.com", "Business Banking Specialist", "Commercial Banking", "Robert Kim"),
        ("Alex Chen", "alex.chen@bank.com", "Teller", "Branch Operations", "Mike Chen"),
        ("Maria Garcia", "maria.garcia@bank.com", "Personal Banker", "Retail Banking", "Lisa Wang")
    ]
    
    created_employees = []
    for name, email, role, dept, manager in employees:
        employee = onboarding_generator.create_employee(name, email, role, dept, manager)
        created_employees.append(employee)
        
        # Simulate some progress for demo purposes
        employee_data = onboarding_generator.get_employee_onboarding(employee.id)
        if "error" not in employee_data:
            tasks = employee_data["program"]["tasks"]
            # Complete 2-3 random tasks for demonstration
            import random
            completed_count = random.randint(1, min(3, len(tasks)))
            for i in range(completed_count):
                task_id = tasks[i]["id"]
                onboarding_generator.complete_task(employee.id, task_id)
    
    return created_employees

if __name__ == "__main__":
    # Create demo data
    demo_employees = create_demo_employees()
    
    print("=== Onboarding System Demo ===")
    print(f"Created {len(demo_employees)} demo employees")
    
    # Show analytics
    analytics = onboarding_generator.get_onboarding_analytics()
    print(f"\nOverall Progress: {analytics['average_progress']:.1f}%")
    print(f"Completion Rate: {analytics['completion_rate']:.1f}%")
    
    # Show employee details
    for employee in demo_employees:
        onboarding_data = onboarding_generator.get_employee_onboarding(employee.id)
        if "error" not in onboarding_data:
            progress = onboarding_data["program"]["progress_percentage"]
            print(f"{employee.name} ({employee.role}): {progress:.1f}% complete")
