from fastapi import FastAPI
from api import tasks_router

app = FastAPI(title="Task management API")

@app.get("/")
async def root() -> dict:
    return {"message": "Task management API is running"}

app.include_router(tasks_router)
