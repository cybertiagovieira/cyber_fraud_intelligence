import sqlite3
import os

DB_PATH = 'database/fraud_events.db'

def initialize_schema():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Core Threat Telemetry Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fraud_events (
        event_id TEXT PRIMARY KEY,
        occurrence_date DATE,
        disclosure_date DATE,
        entry_date DATE,
        fraud_category TEXT,
        fraud_subcategory TEXT,
        attack_vector TEXT,
        ttp_mitre TEXT,
        victim_sector TEXT,
        victim_geo TEXT,
        financial_impact REAL,
        commoditization_stage TEXT,
        cross_sector_link TEXT,
        regulatory_nexus TEXT,
        confidence_overall TEXT,
        source_url TEXT,
        exec_summary TEXT,
        management_impact TEXT
    )
    ''')

    # Actionable Intelligence Output Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recommendations (
        rec_id TEXT PRIMARY KEY,
        event_id TEXT,
        rec_text TEXT,
        target_team TEXT,
        status TEXT,
        FOREIGN KEY(event_id) REFERENCES fraud_events(event_id)
    )
    ''')

    conn.commit()
    conn.close()
    print("Schema initialized.")

if __name__ == "__main__":
    if not os.path.exists('database'):
        os.makedirs('database')
    initialize_schema()