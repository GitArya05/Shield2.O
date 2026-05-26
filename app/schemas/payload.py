from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class IncidentReport(BaseModel):
    # We strictly bound coordinates to valid global limits
    lat: float = Field(..., ge=-90.0, le=90.0)
    lng: float = Field(..., ge=-180.0, le=180.0)
    severity: int = Field(..., ge=1, le=5, description="1 is suspicious, 5 is active danger")
    report_type: str = Field(..., example="luminosity_drop")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class StreamPayload(BaseModel):
    # This ensures we only accept data from authorized stream IDs (1 through 60)
    stream_id: str = Field(..., description="The unique ID of the heterogeneous stream")
    edge_id: int = Field(..., description="The database ID of the street segment")
    
    # Optional updates depending on what the specific stream monitors
    ambient_luminosity: Optional[float] = Field(None, ge=0.0, le=1.0)
    pedestrian_density: Optional[float] = Field(None, ge=0.0, le=1.0)