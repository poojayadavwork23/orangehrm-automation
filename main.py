from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.routes.automation import router as automation_router

app = FastAPI(
    title="OrangeHRM Automation",
    description="Dashboard-driven employee automation",
    version="1.0.0"
)

app.include_router(automation_router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home():
    with open("app/templates/index.html", "r", encoding="utf-8") as file:
        return file.read()


@app.get("/health")
def health_check():
    return {"status": "healthy"}