from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db
from app.utils.s3 import s3_client

router = APIRouter(tags=["system"])

@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        db_status = "ok"
    except:
        db_status = "error"

    try:
        await s3_client.check_connection()
        s3_status = "ok"
    except:
        s3_status = "error"

    return {
        "status": "ok" if db_status == "ok" and s3_status == "ok" else "error",
        "components": {
            "database": db_status,
            "storage": s3_status
        }
    }

@router.get("/info")
async def get_info():
    return {
        "version": "1.0.0",
        "environment": "development",
        "framework": "FastAPI"
    }