from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.core.database import get_db
from app.services.routing import calculate_safest_route

router = APIRouter()

class RouteRequest(BaseModel):
    start_lat: float = Field(..., ge=-90.0, le=90.0)
    start_lng: float = Field(..., ge=-180.0, le=180.0)
    end_lat: float = Field(..., ge=-90.0, le=90.0)
    end_lng: float = Field(..., ge=-180.0, le=180.0)

@router.post("/calculate")
def get_safe_route(payload: RouteRequest, db: Session = Depends(get_db)):
    """
    Computes the safest pedestrian path by weighting historical incidents 
    and ambient luminosity over standard physical distance.
    """
    route_data = calculate_safest_route(
        db=db,
        start_lat=payload.start_lat,
        start_lng=payload.start_lng,
        end_lat=payload.end_lat,
        end_lng=payload.end_lng
    )
    return route_data