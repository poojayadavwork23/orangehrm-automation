
from fastapi import FastAPI

app = FastAPI(
    title="OrangeHRM Automation",
    description="Dashboard-driven employee automation",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "OrangeHRM Automation API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
