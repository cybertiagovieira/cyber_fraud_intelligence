import sqlite3
import uuid
import datetime

DB_PATH = 'database/fraud_events.db'

def insert_baseline_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    today = datetime.date.today()
    
    events = [
        (
            f"EVT-{str(uuid.uuid4())[:8]}", today.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"),
            "APP Fraud", "CEO Spoofing", "Voice Cloning", "T1566.004", "Retail Banking", "DE",
            250000.0, "Packaged", "None", "PSD3", "High", "https://t.me/s/fraud_channel", 
            "Voice cloning attack bypassed secondary verification.", "Elevated risk of APP fraud via synthetic voice prior to PSD3 implementation."
        ),
        (
            f"EVT-{str(uuid.uuid4())[:8]}", (today - datetime.timedelta(days=2)).strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d"),
            "Account Takeover", "Credential Stuffing", "Residential Proxies", "T1110.004", "Fintech", "UK",
            45000.0, "Saturated", "EVT-PREV-001", "None", "Medium", "https://t.me/s/log_shop", 
            "Credential stuffing utilizing distributed residential proxy network.", "Require immediate review of rate-limiting controls on customer portals."
        )
    ]

    cursor.executemany('''
        INSERT INTO fraud_events (
            event_id, occurrence_date, disclosure_date, entry_date, fraud_category, 
            fraud_subcategory, attack_vector, ttp_mitre, victim_sector, victim_geo, 
            financial_impact, commoditization_stage, cross_sector_link, regulatory_nexus, 
            confidence_overall, source_url, exec_summary, management_impact
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', events)

    conn.commit()
    conn.close()
    print("[+] Baseline telemetry injected.")

if __name__ == "__main__":
    insert_baseline_data()