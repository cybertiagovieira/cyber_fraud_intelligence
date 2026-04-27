import re

def parse_telemetry_to_schema(text):
    """
    Heuristic extraction layer.
    Maps unstructured OSINT text to the CTI database schema.
    """
    text = text.lower()
    
    # Baseline default values
    data = {
        "fraud_category": "Unclassified",
        "fraud_subcategory": "Unknown",
        "attack_vector": "Unknown",
        "ttp_mitre": "Unknown",
        "victim_sector": "Unknown",
        "victim_geo": "Unknown",
        "financial_impact": 0.0,
        "commoditization_stage": "Unknown",
        "confidence_overall": "Medium",
        "management_impact": "Pending Analyst Review"
    }
    
    # Fraud Category Routing
    if any(k in text for k in ["app fraud", "authorized push payment", "transfer", "wire"]):
        data["fraud_category"] = "APP Fraud"
    elif any(k in text for k in ["takeover", "ato", "credential stuffing", "log", "combo"]):
        data["fraud_category"] = "Account Takeover"
    elif any(k in text for k in ["ransomware", "encrypt", "lock"]):
        data["fraud_category"] = "Ransomware"
        
    # Attack Vector & MITRE ATT&CK Mapping
    if any(k in text for k in ["voice", "clone", "deepfake"]):
        data["attack_vector"] = "Voice Cloning"
        data["ttp_mitre"] = "T1566.004"
    elif any(k in text for k in ["phish", "smish", "link"]):
        data["attack_vector"] = "Phishing"
        data["ttp_mitre"] = "T1566"
    elif any(k in text for k in ["proxy", "proxies", "botnet"]):
        data["attack_vector"] = "Residential Proxies"
        data["ttp_mitre"] = "T1090.002"
        
    # Victimology Sector Logic
    if any(k in text for k in ["bank", "financial", "credit"]):
        data["victim_sector"] = "Retail Banking"
    elif any(k in text for k in ["fintech", "crypto", "exchange"]):
        data["victim_sector"] = "Fintech"
        
    # Financial Impact Extraction via Regex
    impact_match = re.search(r'[\$€£](\d+[,\.]?\d*[kKmMbB]?)', text)
    if impact_match:
        val_str = impact_match.group(1).replace(',', '')
        multiplier = 1
        if 'k' in val_str.lower(): multiplier = 1000
        elif 'm' in val_str.lower(): multiplier = 1000000
        val_str = re.sub(r'[a-zA-Z]', '', val_str)
        try:
            data["financial_impact"] = float(val_str) * multiplier
        except ValueError:
            pass

    return data