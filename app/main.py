from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db, engine
from app.models import spatial

from app.api.v1 import ingestion
from app.api.v1 import routing # <-- New Import

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

spatial.Base.metadata.create_all(bind=engine)

app.include_router(ingestion.router, prefix="/api/v1/ingest", tags=["Data Ingestion"])
app.include_router(routing.router, prefix="/api/v1/routing", tags=["Spatial Routing Engine"]) # <-- New Route

@app.get("/")
def root():
    return {"message": "Shield API Gateway is online.", "status": "active"}

@app.get("/api/v1/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected", "version": settings.VERSION}
    except Exception as e:
        raise HTTPException(status_code=503, detail="Database connection failed")