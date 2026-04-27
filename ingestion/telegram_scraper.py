import requests
from bs4 import BeautifulSoup
import re

def scrape_telegram_preview(channel_name, limit=15):
    """
    Scrapes public Telegram channels via web preview (t.me/s/).
    Zero-budget, zero-API OPSEC.
    """
    url = f"https://t.me/s/{channel_name}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    print(f"Executing stealth extraction on: {channel_name}...")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to access {channel_name} (Status: {response.status_code})")
        return []

    # CRITICAL: Force UTF-8 encoding as required by our architecture analysis
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    extracted_data = []
    
    # Locate all message containers
    messages = soup.find_all('div', class_='tgme_widget_message', limit=limit)
    
    for msg in messages:
        text_div = msg.find('div', class_='tgme_widget_message_text')
        date_time = msg.find('time')
        
        if text_div:
            # Extract raw text, replacing <br> with newlines
            raw_text = text_div.get_text(separator='\n', strip=True)
            timestamp = date_time.get('datetime') if date_time else "Unknown"
            
            extracted_data.append({
                "channel": channel_name,
                "timestamp": timestamp,
                "raw_text": raw_text
            })

    return extracted_data

if __name__ == "__main__":
    # Test on a known public security channel (e.g., vxunderground or similar)
    # We will use 'vxunderground' just to test the connection and extraction
    results = scrape_telegram_preview("vxunderground", limit=3)
    for r in results:
        print(f"\n[{r['timestamp']}]\n{r['raw_text']}")