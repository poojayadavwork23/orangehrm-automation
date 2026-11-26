
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.automation.driver import run_automation


router = APIRouter(
    prefix="/api/automation",
    tags=["Automation"]
)


class EmployeeRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    employee_id: str = Field(..., min_length=1)


@router.get("/test")
def test_automation():

    return {
        "status": "success",
        "message": "Automation API is working!"
    }


@router.post("/start")
def start_automation(data: EmployeeRequest):

    try:
        result = run_automation(
            username=data.username,
            password=data.password,
            first_name=data.first_name,
            last_name=data.last_name,
            employee_id=data.employee_id
        )

        # Check automation result
        if result.get("status") == "failed":
            raise HTTPException(
                status_code=500,
                detail=result.get("message", "Automation failed.")
            )

        return result

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        ) from error
