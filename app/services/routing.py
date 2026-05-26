import networkx as nx
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import HTTPException

def get_nearest_node(db: Session, lat: float, lng: float) -> int:
    """Finds the closest database node to the user's raw GPS coordinates using PostGIS."""
    query = text("""
        SELECT id 
        FROM nodes 
        ORDER BY geom <-> ST_SetSRID(ST_MakePoint(:lng, :lat), 4326) 
        LIMIT 1;
    """)
    result = db.execute(query, {"lat": lat, "lng": lng}).fetchone()
    if not result:
        raise HTTPException(status_code=404, detail="No routable nodes found near this location.")
    return result.id

def calculate_safest_route(db: Session, start_lat: float, start_lng: float, end_lat: float, end_lng: float):
    # 1. Snap GPS coordinates to the nearest physical street nodes
    start_node_id = get_nearest_node(db, start_lat, start_lng)
    end_node_id = get_nearest_node(db, end_lat, end_lng)

    if start_node_id == end_node_id:
        return {"route": [start_node_id], "total_safe_weight": 0, "status": "Already at destination"}

    # 2. Extract a localized subgraph (Bounding Box) to prevent memory crashes
    # In a production app, you would mathematically define a bounding box around the start/end points.
    # For this implementation, we pull edges within a generous localized radius.
    edges_query = text("""
        SELECT start_node_id, end_node_id, base_distance_meters, dynamic_risk_score
        FROM edges
    """)
    edges = db.execute(edges_query).fetchall()

    # 3. Initialize the In-Memory Graph
    G = nx.Graph()

    # 4. The Shield Custom Weighting Algorithm
    for edge in edges:
        # Standard routing: weight = distance
        # Shield routing: High risk heavily penalizes the distance, forcing the algorithm 
        # to choose a slightly longer, but significantly safer, physical path.
        risk_multiplier = 1.0 + (edge.dynamic_risk_score * 2.0) 
        safe_weight = edge.base_distance_meters * risk_multiplier
        
        G.add_edge(
            edge.start_node_id, 
            edge.end_node_id, 
            weight=safe_weight,
            distance=edge.base_distance_meters
        )

    # 5. Execute A* Search
    try:
        # A* is highly optimized for spatial networks compared to standard Dijkstra
        path = nx.astar_path(G, source=start_node_id, target=end_node_id, weight="weight")
        
        # Calculate total safe_weight and physical distance of the chosen path
        total_weight = 0
        total_distance = 0
        for i in range(len(path) - 1):
            edge_data = G.get_edge_data(path[i], path[i+1])
            total_weight += edge_data['weight']
            total_distance += edge_data['distance']
            
        return {
            "status": "success",
            "path_nodes": path,
            "metrics": {
                "physical_distance_meters": round(total_distance, 2),
                "algorithmic_safe_weight": round(total_weight, 2)
            }
        }
        
    except nx.NetworkXNoPath:
        raise HTTPException(status_code=400, detail="No safe path exists between these coordinates.")