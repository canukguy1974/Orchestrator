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

class OnboardingResponse(BaseModel):
    employee: Dict[str, Any]
    program: Dict[str, Any]

class AnalyticsResponse(BaseModel):
    total_employees: int
    average_progress: float
    completion_rate: float
    by_role: Dict[str, Any]

@router.get("/employees", summary="Get all employees and their onboarding status")
async def get_all_employees():
    """
    Retrieve all employees with their onboarding progress.
    Useful for HR dashboard and manager oversight.
    """
    try:
        employees = onboarding_generator.get_all_employees()
        return {
            "employees": employees,
            "count": len(employees)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/employees", summary="Create a new employee with onboarding program")
async def create_employee(request: CreateEmployeeRequest):
    """
    Create a new employee and assign appropriate onboarding program.
    Automatically matches role to onboarding workflow.
    """
    try:
        employee = onboarding_generator.create_employee(
            name=request.name,
            email=request.email,
            role=request.role,
            department=request.department,
            manager=request.manager
        )
        
        # Get the full onboarding details
        onboarding_data = onboarding_generator.get_employee_onboarding(employee.id)
        
        return {
            "success": True,
            "employee": employee.__dict__,
            "onboarding": onboarding_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/employees/{employee_id}", summary="Get specific employee's onboarding details")
async def get_employee_onboarding(employee_id: str):
    """
    Get detailed onboarding information for a specific employee.
    Includes all tasks, progress, and completion status.
    """
    try:
        onboarding_data = onboarding_generator.get_employee_onboarding(employee_id)
        
        if "error" in onboarding_data:
            raise HTTPException(status_code=404, detail=onboarding_data["error"])
        
        return onboarding_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/employees/{employee_id}/complete-task", summary="Mark a task as completed")
async def complete_task(employee_id: str, request: CompleteTaskRequest):
    """
    Mark an onboarding task as completed for an employee.
    Updates progress tracking and completion timestamps.
    """
    try:
        result = onboarding_generator.complete_task(employee_id, request.task_id)
        
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analytics", summary="Get onboarding analytics and statistics")
async def get_onboarding_analytics():
    """
    Get comprehensive analytics about onboarding progress.
    Useful for HR reports and performance tracking.
    """
    try:
        analytics = onboarding_generator.get_onboarding_analytics()
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/demo-data", summary="Create demo employees for testing")
async def create_demo_data():
    """
    Create sample employees with various onboarding progress.
    Useful for demonstrations and testing.
    """
    try:
        # Create demo employees with different roles
        demo_employees_data = [
            {"name": "Sarah Johnson", "email": "sarah.johnson@bank.com", "role": "Teller", "department": "Branch Operations", "manager": "Mike Chen"},
            {"name": "David Rodriguez", "email": "david.rodriguez@bank.com", "role": "Personal Banker", "department": "Retail Banking", "manager": "Lisa Park"},
            {"name": "Emily Chen", "email": "emily.chen@bank.com", "role": "Business Banking Specialist", "department": "Commercial Banking", "manager": "Robert Smith"},
            {"name": "Michael Thompson", "email": "michael.thompson@bank.com", "role": "Teller", "department": "Branch Operations", "manager": "Mike Chen"},
            {"name": "Jessica Liu", "email": "jessica.liu@bank.com", "role": "Personal Banker", "department": "Retail Banking", "manager": "Lisa Park"}
        ]
        
        # Clear existing employees for demo (but keep programs)
        onboarding_generator.employees.clear()
        # Re-initialize programs to ensure they exist
        onboarding_generator._initialize_programs()
        
        created_employees = []
        for emp_data in demo_employees_data:
            employee = onboarding_generator.create_employee(**emp_data)
            created_employees.append(employee)
            
            # Simulate some progress by completing a few tasks
            onboarding_data = onboarding_generator.get_employee_onboarding(employee.id)
            if "program" in onboarding_data and onboarding_data["program"]["tasks"]:
                # Complete first task for demonstration
                onboarding_generator.complete_task(employee.id, onboarding_data["program"]["tasks"][0]["id"])
        
        return {
            "success": True,
            "message": f"Created {len(created_employees)} demo employees",
            "employees": [emp.__dict__ for emp in created_employees]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/demo-data", summary="Clear all demo data")
async def clear_demo_data():
    """
    Clear all employees and reset the onboarding system.
    Useful for resetting demonstrations.
    """
    try:
        onboarding_generator.employees.clear()
        return {"success": True, "message": "All demo data cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clear", summary="Clear all onboarding data")
async def clear_onboarding_data():
    """
    Clear all employees and reset programs.
    Useful for demos and testing.
    """
    try:
        # Clear existing employees
        onboarding_generator.employees.clear()
        # Re-initialize programs to ensure they exist
        onboarding_generator._initialize_programs()
        
        return {
            "success": True,
            "message": "All onboarding data cleared successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/programs", summary="Get available onboarding programs")
async def get_onboarding_programs():
    """
    Get all available onboarding programs and their details.
    Shows the different workflows for various roles.
    """
    try:
        programs = {}
        for key, program in onboarding_generator.programs.items():
            programs[key] = {
                "id": program.id,
                "role": program.role,
                "department": program.department,
                "duration_days": program.duration_days,
                "total_tasks": len(program.tasks),
                "task_categories": list(set(task.category for task in program.tasks)),
                "estimated_hours": sum(int(task.estimated_time) for task in program.tasks) / 60
            }
        
        return {
            "programs": programs,
            "total_programs": len(programs)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
