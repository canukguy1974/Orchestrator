"""
FastAPI Router for Employee Onboarding System
Provides endpoints for managing employee onboarding workflows
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from server.tools.onboarding import OnboardingGenerator

router = APIRouter(prefix="/onboarding", tags=["onboarding"])

# Initialize the onboarding generator
onboarding_generator = OnboardingGenerator()

# Pydantic models for request/response
class CreateEmployeeRequest(BaseModel):
    name: str
    email: str
    role: str
    department: str
    manager: str

class CompleteTaskRequest(BaseModel):
    task_id: str

@router.get("/employees")
async def get_employees():
    """Get all employees with their onboarding progress summary"""
    try:
        employees = onboarding_generator.get_all_employees()
        
        # Create summary with progress for each employee
        employee_summaries = []
        for emp in employees:
            program = onboarding_generator.get_employee_onboarding(emp.id)
            completed_tasks = sum(1 for task in program.program.tasks if task.completed)
            total_tasks = len(program.program.tasks)
            
            employee_summaries.append({
                "employee": emp.__dict__,
                "progress": program.program.progress_percentage,
                "completed_tasks": completed_tasks,
                "total_tasks": total_tasks
            })
        
        return {"employees": employee_summaries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/employees")
async def create_employee(request: CreateEmployeeRequest):
    """Create a new employee with onboarding program"""
    try:
        employee = onboarding_generator.create_employee(
            name=request.name,
            email=request.email,
            role=request.role,
            department=request.department,
            manager=request.manager
        )
        
        onboarding_data = onboarding_generator.get_employee_onboarding(employee.id)
        
        return {
            "employee": employee.__dict__,
            "program": onboarding_data.program.__dict__
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/employees/{employee_id}")
async def get_employee_details(employee_id: str):
    """Get detailed employee information with full onboarding program"""
    try:
        onboarding_data = onboarding_generator.get_employee_onboarding(employee_id)
        
        if not onboarding_data:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        # Convert to dict for JSON serialization
        return {
            "employee": onboarding_data.employee.__dict__,
            "program": {
                **onboarding_data.program.__dict__,
                "tasks": [task.__dict__ for task in onboarding_data.program.tasks]
            }
        }
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/employees/{employee_id}/complete-task")
async def complete_task(employee_id: str, request: CompleteTaskRequest):
    """Mark a task as completed for an employee"""
    try:
        result = onboarding_generator.complete_task(employee_id, request.task_id)
        
        if not result:
            raise HTTPException(status_code=404, detail="Employee or task not found")
        
        # Get updated onboarding data
        onboarding_data = onboarding_generator.get_employee_onboarding(employee_id)
        
        return {
            "success": True,
            "message": "Task completed successfully",
            "updated_progress": onboarding_data.program.progress_percentage
        }
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics")
async def get_analytics():
    """Get onboarding analytics and metrics"""
    try:
        analytics = onboarding_generator.get_onboarding_analytics()
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/demo-data")
async def create_demo_data():
    """Create demo employees for testing purposes"""
    try:
        # Create demo employees with different roles
        demo_employees = [
            {"name": "Sarah Johnson", "email": "sarah.johnson@bank.com", "role": "Teller", "department": "Branch Operations", "manager": "Mike Chen"},
            {"name": "David Rodriguez", "email": "david.rodriguez@bank.com", "role": "Personal Banker", "department": "Retail Banking", "manager": "Lisa Park"},
            {"name": "Emily Chen", "email": "emily.chen@bank.com", "role": "Business Banking Specialist", "department": "Commercial Banking", "manager": "Robert Smith"},
            {"name": "Michael Thompson", "email": "michael.thompson@bank.com", "role": "Teller", "department": "Branch Operations", "manager": "Mike Chen"},
            {"name": "Jessica Liu", "email": "jessica.liu@bank.com", "role": "Personal Banker", "department": "Retail Banking", "manager": "Lisa Park"}
        ]
        
        # Clear existing data for demo
        onboarding_generator.employees.clear()
        onboarding_generator.programs.clear()
        
        created_employees = []
        for emp_data in demo_employees:
            employee = onboarding_generator.create_employee(**emp_data)
            created_employees.append(employee)
            
            # Simulate some progress by completing a few tasks
            onboarding_data = onboarding_generator.get_employee_onboarding(employee.id)
            if onboarding_data.program.tasks:
                # Complete first task for demonstration
                onboarding_generator.complete_task(employee.id, onboarding_data.program.tasks[0].id)
        
        # Get analytics for the created data
        analytics = onboarding_generator.get_onboarding_analytics()
        
        return {
            "message": f"Created {len(created_employees)} demo employees",
            "employees": [emp.__dict__ for emp in created_employees],
            "analytics": analytics
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/programs")
async def get_available_programs():
    """Get all available onboarding programs"""
    try:
        programs = []
        for key, program in onboarding_generator.programs.items():
            programs.append({
                "role": program.role,
                "department": program.department,
                "duration_days": program.duration_days,
                "task_count": len(program.tasks),
                "tasks": [{"title": task.title, "category": task.category, "priority": task.priority} for task in program.tasks]
            })
        
        return {"programs": programs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
