import schedule
import time
import subprocess
import os

def execute_ingestion():
    print("[*] Triggering automated ingestion cycle...")
    subprocess.run([os.sys.executable, "ingestion/orchestrator.py"])

def start_daemon():
    print("[+] CTI Pipeline Daemon Initialized.")
    print("[+] Ingestion interval: 4 hours.")
    
    # Run once immediately on startup
    execute_ingestion()
    
    # Schedule recurring execution
    schedule.every(4).hours.do(execute_ingestion)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    start_daemon()