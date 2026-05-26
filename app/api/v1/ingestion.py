from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.schemas.payload import IncidentReport, StreamPayload
from app.models.spatial import Incident, Edge

router = APIRouter()

def process_stream_data(payload: StreamPayload, db: Session):
    """
    Background task to update the street edge with new sensor data.
    This prevents the API from hanging while processing 60 streams.
    """
    edge = db.query(Edge).filter(Edge.id == payload.edge_id).first()
    if not edge:
        return # In a real system, we would log this anomaly
        
    if payload.ambient_luminosity is not None:
        edge.ambient_luminosity = payload.ambient_luminosity
    if payload.pedestrian_density is not None:
        edge.pedestrian_density = payload.pedestrian_density
        
    # Recalculate the dynamic risk score (simplified placeholder logic)
    # High density + low light = higher risk score
    risk_factor = (1.0 - edge.ambient_luminosity) + edge.pedestrian_density
    edge.dynamic_risk_score = min(risk_factor, 10.0) 
    
    db.commit()

@router.post("/environment-stream")
async def ingest_environmental_data(
    payload: StreamPayload, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    # We pass the heavy database update to a background task
    background_tasks.add_task(process_stream_data, payload, db)
    return {"status": "accepted", "message": f"Data from stream {payload.stream_id} queued for processing."}

@router.post("/incident")
async def report_incident(payload: IncidentReport, db: Session = Depends(get_db)):
    # Convert standard lat/lng into a PostGIS spatial point
    wkt_point = f"SRID=4326;POINT({payload.lng} {payload.lat})"
    
    new_incident = Incident(
        geom=text(f"ST_GeomFromEWKT('{wkt_point}')"),
        severity=payload.severity,
        report_type=payload.report_type,
        timestamp=payload.timestamp
    )
    
    db.add(new_incident)
    db.commit()
    return {"status": "success", "message": "Incident secured and logged."}