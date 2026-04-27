from fastapi import FastAPI, HTTPException, Query
import sqlite3
import os

app = FastAPI(title="CTI Fraud Dissemination API", version="1.0")
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'fraud_events.db'))

def get_db_connection():
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=500, detail="Database inaccessible.")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/api/v1/events/recent")
def get_recent_events(limit: int = Query(10, ge=1, le=100)):
    """Extracts the most recent threat telemetry."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fraud_events ORDER BY occurrence_date DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return {"data": [dict(row) for row in rows]}

@app.get("/api/v1/events/vector/{vector}")
def get_events_by_vector(vector: str):
    """Extracts telemetry filtered by attack vector (e.g., Phishing, Voice Cloning)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fraud_events WHERE attack_vector LIKE ?", (f"%{vector}%",))
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        raise HTTPException(status_code=404, detail="No events found for specified vector.")
        
    return {"data": [dict(row) for row in rows]}