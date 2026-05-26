from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from datetime import datetime, timezone
from app.core.database import Base

class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)
    # PostGIS Point geometry (Longitude, Latitude) using standard WGS84 (SRID 4326)
    geom = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    
    # We store lat/lng explicitly for fast JSON serialization to the mobile client
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)

class Edge(Base):
    __tablename__ = "edges"

    id = Column(Integer, primary_key=True, index=True)
    start_node_id = Column(Integer, ForeignKey("nodes.id"), nullable=False)
    end_node_id = Column(Integer, ForeignKey("nodes.id"), nullable=False)
    
    # The physical shape of the street
    geom = Column(Geometry(geometry_type='LINESTRING', srid=4326), nullable=False)
    
    # --- Standard Routing Metric ---
    base_distance_meters = Column(Float, nullable=False)
    
    # --- Shield Predictive Risk Parameters ---
    ambient_luminosity = Column(Float, default=1.0) # 0.0 (Pitch Black) to 1.0 (Daylight)
    pedestrian_density = Column(Float, default=0.5) # 0.0 (Deserted) to 1.0 (Crowded)
    
    # The final dynamic score calculated by our ML engine processing the 60 data streams
    dynamic_risk_score = Column(Float, default=0.0)

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    geom = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    severity = Column(Integer, nullable=False) # e.g., 1 (Suspicious) to 5 (Active Danger)
    report_type = Column(String, nullable=False) # e.g., "luminosity_drop", "harassment", "SOS"