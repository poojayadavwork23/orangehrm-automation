from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.automation.driver import run_automation

router = APIRouter(
    prefix="/api/automation",
    tags=["Automation"]
)


class EmployeeRequest(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    employee_id: str


@router.get("/test")
def test_automation():
    return {
        "status": "success",
        "message": "Automation API is working!"
    }


@router.post("/start")
def start_automation(data: EmployeeRequest):

    result = run_automation(
        username=data.username,
        password=data.password,
        first_name=data.first_name,
        last_name=data.last_name,
        employee_id=data.employee_id
    )

    return result