from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, tasks

app = FastAPI(title="Pro Task Manager")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def root():
    return {"message": "DGTU Backend Pro is running"}

app.include_router(auth.router)
app.include_router(tasks.router)