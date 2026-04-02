from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, tasks, comments
from app.exceptions import AppException, app_exception_handler

app = FastAPI(title="Pro Task Manager v1")

app.add_exception_handler(AppException, app_exception_handler)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(comments.router)

@app.get("/")
async def root():
    return {"message": "Task Manager API v1 is running"}