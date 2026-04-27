import sqlite3
import uuid
import datetime
from telegram_scraper import scrape_telegram_preview
from translator import translate_local
from parser import parse_telemetry_to_schema

DB_PATH = 'database/fraud_events.db'
TARGET_CHANNELS = [
    # Core CTI & OSINT Aggregators
    "vxunderground",       # Malware samples and exploit documentation
    "threatintel",         # General CTI aggregation
    "DailyDarkWeb",        # Dark web breach announcements and leak tracking
    "FalconFeedsio",       # Automated threat intelligence alerts
    "DataLeakMonitor",     # Centralized credential and database leak indexing
    
    # Vulnerability & Operational Security
    "cybersec_feed",       # Vulnerability and exploit disclosures
    "ransomware_news",     # Dedicated ransomware negotiation and DLS tracking
    "cert_ee"              # State-level threat advisories (CERT Estonia)
]

def process_and_store_telemetry():
    """Extracts, translates, parses, and stages OSINT telemetry."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    today_str = datetime.date.today().strftime("%Y-%m-%d")

    for channel in TARGET_CHANNELS:
        print(f"[*] Initiating pipeline for: {channel}")
        raw_data = scrape_telegram_preview(channel, limit=5)
        
        for item in raw_data:
            translated_text = translate_local(item['raw_text'], from_lang="ru")
            
            parsed_data = parse_telemetry_to_schema(translated_text)
            
            event_id = f"EVT-AUTO-{str(uuid.uuid4())[:6]}"
            
            try:
                cursor.execute('''
                    INSERT INTO fraud_events (
                        event_id, occurrence_date, disclosure_date, entry_date, fraud_category, 
                        fraud_subcategory, attack_vector, ttp_mitre, victim_sector, victim_geo, 
                        financial_impact, commoditization_stage, cross_sector_link, regulatory_nexus, 
                        confidence_overall, source_url, exec_summary, management_impact
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    event_id, today_str, today_str, today_str, 
                    parsed_data["fraud_category"], parsed_data["fraud_subcategory"], 
                    parsed_data["attack_vector"], parsed_data["ttp_mitre"], 
                    parsed_data["victim_sector"], parsed_data["victim_geo"],
                    parsed_data["financial_impact"], parsed_data["commoditization_stage"], 
                    "None", "None", parsed_data["confidence_overall"], 
                    f"https://t.me/s/{channel}", translated_text, parsed_data["management_impact"]
                ))
            except sqlite3.Error as e:
                print(f"Database insertion failed: {e}")

    conn.commit()
    conn.close()
    print("[+] Pipeline execution complete. Parsed telemetry staged.")

if __name__ == "__main__":
    process_and_store_telemetry()