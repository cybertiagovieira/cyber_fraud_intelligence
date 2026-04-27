import base64
import hashlib
import hmac
import urllib.request
import urllib.parse
import json
import os
from dotenv import load_dotenv

load_dotenv()

SILOBREAKER_API_URL = "https://api.silobreaker.com/v2"

def execute_silobreaker_request(endpoint_path, api_key, shared_key):
    """
    Constructs HMAC-SHA512 signature and executes GET request.
    """
    if not api_key or not shared_key:
        return {"error": "Silobreaker credentials missing."}

    url = urllib.parse.quote(f"{SILOBREAKER_API_URL}{endpoint_path}", safe=":/?&=")
    message = f"GET {url}"
    
    hmac_sha512 = hmac.new(
        shared_key.encode('utf-8'), 
        message.encode('utf-8'), 
        digestmod=hashlib.sha512
    )
    digest = base64.b64encode(hmac_sha512.digest()).decode('utf-8')
    
    sep = '&' if '?' in url else '?'
    final_url = f"{url}{sep}apiKey={api_key}&digest={urllib.parse.quote(digest)}"
    
    req = urllib.request.Request(final_url)
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        return {"error": str(e)}

def pivot_ioc_to_entities(ioc_value, api_key, shared_key):
    """
    Pivot: Raw IOC -> Correlated Threat Actors and Malware.
    Utilizes v2/infocus endpoint.
    """
    print(f"[+] Executing Silobreaker entity pivot for: {ioc_value}")
    
    encoded_ioc = urllib.parse.quote(ioc_value)
    path = f"/infocus/?q={encoded_ioc}&entitytypes=threatactor,malware&format=json"
    
    return execute_silobreaker_request(path, api_key, shared_key)

def extract_ioc_context(ioc_value, api_key, shared_key):
    """
    Pivot: Raw IOC -> Recent Contextual Documents.
    Utilizes v2/documents/search endpoint.
    """
    print(f"[+] Executing Silobreaker document extraction for: {ioc_value}")
    
    encoded_ioc = urllib.parse.quote(f'"{ioc_value}" fromdate:-30d')
    path = f"/documents/search?query={encoded_ioc}&pageSize=5"
    
    return execute_silobreaker_request(path, api_key, shared_key)

if __name__ == "__main__":
    # Execution Test. Replace 'None' with os.getenv() calls in production.
    TEST_API_KEY = os.getenv("SILOBREAKER_API_KEY")
    TEST_SHARED_KEY = os.getenv("SILOBREAKER_SHARED_KEY")
    TEST_IOC = "LockBit" 
    
    # Test execution flow (will return HTTP 401 Unauthorized without valid keys)
    print("Entity Pivot Result:")
    print(pivot_ioc_to_entities(TEST_IOC, TEST_API_KEY, TEST_SHARED_KEY))