CONSTRAINTS = (
    "CREATE CONSTRAINT incident_id IF NOT EXISTS FOR (n:Incident) REQUIRE n.id IS UNIQUE",
    "CREATE CONSTRAINT zone_id IF NOT EXISTS FOR (n:DisasterZone) REQUIRE n.id IS UNIQUE",
    "CREATE CONSTRAINT shelter_id IF NOT EXISTS FOR (n:Shelter) REQUIRE n.id IS UNIQUE",
    "CREATE CONSTRAINT road_id IF NOT EXISTS FOR (n:Road) REQUIRE n.id IS UNIQUE",
    "CREATE CONSTRAINT resource_id IF NOT EXISTS FOR (n:Resource) REQUIRE n.id IS UNIQUE",
)

PROJECT_FLOOD = """
UNWIND $zones AS zone
MERGE (z:DisasterZone {id: zone.id})
SET z.name = zone.name, z.risk_level = zone.risk_level, z.population = zone.population
WITH z
MATCH (i:Incident {id: $incident_id})
MERGE (i)-[:AFFECTS]->(z)
WITH i
UNWIND $shelters AS shelter
MERGE (s:Shelter {id: shelter.id})
SET s.name = shelter.name, s.capacity = shelter.capacity, s.available = shelter.available
WITH i, s
MERGE (s)-[:SERVES]->(i)
RETURN i.id AS incident_id, count(s) AS shelter_count
"""

INCIDENT_CONTEXT = """
MATCH (i:Incident {id: $incident_id})
OPTIONAL MATCH (i)-[:AFFECTS]->(zone:DisasterZone)
OPTIONAL MATCH (zone)<-[:SERVES]-(shelter:Shelter)
RETURN i.id AS incident_id,
       collect(DISTINCT {id: zone.id, name: zone.name, risk_level: zone.risk_level, population: zone.population}) AS zones,
       collect(DISTINCT {id: shelter.id, name: shelter.name, capacity: shelter.capacity, available: shelter.available}) AS shelters
"""
