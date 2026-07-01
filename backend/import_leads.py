# import json
# import requests
# import time
# from pathlib import Path

# BASE_DIR = Path(__file__).parent.parent          # dentist-website/
# SHARED_DIR = BASE_DIR / "shared_data"
# LEADS_FILE = SHARED_DIR / "enriched_leads.json"
# OUTPUT_FILE = SHARED_DIR / "demo_links.json"

# # Use environment variable for API URL, or fallback to local
# import os
# API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api/clients/register")

# def map_niche(niche):
#     if not niche:
#         return "restaurant"
#     if niche.endswith('s'):
#         return niche[:-1]
#     return niche

# def clean_address(addr):
#     if addr:
#         return addr.replace('\n', ' ').strip()
#     return None

# def main():
#     if not LEADS_FILE.exists():
#         print(f"❌ Leads file not found: {LEADS_FILE}")
#         return

#     with open(LEADS_FILE, 'r', encoding='utf-8') as f:
#         leads = json.load(f)

#     if not leads:
#         print("⚠️ No leads found.")
#         return

#     print(f"📥 Found {len(leads)} leads. Registering...")
#     mapping = {}

#     for lead in leads:
#         business_name = lead.get('name')
#         if not business_name:
#             continue

#         payload = {
#             "business_name": business_name.strip(),
#             "niche": map_niche(lead.get('niche')),
#             "phone": lead.get('phone'),
#             "address": clean_address(lead.get('address')),
#             "email": lead.get('email'),
#             "city": lead.get('city'),
#             "state": lead.get('state'),
#             "rating": lead.get('lead_stage'),
#             "google_maps_url": lead.get('maps_url'),
#             "facebook_url": lead.get('facebook_url'),
#             "instagram_url": lead.get('instagram_url'),
#             "lead_score": lead.get('lead_stage'),
#         }
#         payload = {k: v for k, v in payload.items() if v is not None}

#         try:
#             resp = requests.post(API_URL, json=payload)
#             if resp.status_code == 200:
#                 data = resp.json()
#                 mapping[business_name] = data.get('demo_url')
#                 print(f"✅ {business_name} → {data.get('demo_url')}")
#             else:
#                 print(f"❌ {business_name} failed: {resp.status_code} - {resp.text}")
#         except Exception as e:
#             print(f"⚠️ {business_name} error: {e}")

#         time.sleep(0.2)

#     SHARED_DIR.mkdir(parents=True, exist_ok=True)
#     with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
#         json.dump(mapping, f, indent=2, ensure_ascii=False)

#     print(f"✅ Saved {len(mapping)} links to {OUTPUT_FILE}")

# if __name__ == "__main__":
#     main()


import json
import requests
import time
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent          # dentist-website/
SHARED_DIR = BASE_DIR / "shared_data"
LEADS_FILE = SHARED_DIR / "enriched_leads.json"
OUTPUT_FILE = SHARED_DIR / "demo_links.json"

# Use environment variable for API URL, or fallback to local
import os
API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api/clients/register")

def map_niche(niche):
    if not niche:
        return "restaurant"
    if niche.endswith('s'):
        return niche[:-1]
    return niche

def clean_address(addr):
    if addr:
        return addr.replace('\n', ' ').strip()
    return None

def main():
    if not LEADS_FILE.exists():
        print(f"❌ Leads file not found: {LEADS_FILE}")
        return

    with open(LEADS_FILE, 'r', encoding='utf-8') as f:
        leads = json.load(f)

    if not leads:
        print("⚠️ No leads found.")
        return

    print(f"📥 Found {len(leads)} leads. Registering...")
    mapping = {}

    for lead in leads:
        business_name = lead.get('name')
        if not business_name:
            continue

        payload = {
            "business_name": business_name.strip(),
            "niche": map_niche(lead.get('niche')),
            "phone": lead.get('phone'),
            "address": clean_address(lead.get('address')),
            "email": lead.get('email'),
            "city": lead.get('city'),
            "state": lead.get('state'),
            "rating": lead.get('lead_stage'),
            "google_maps_url": lead.get('maps_url'),
            "facebook_url": lead.get('facebook_url'),
            "instagram_url": lead.get('instagram_url'),
            "lead_score": lead.get('lead_stage'),
            "latitude": lead.get('latitude'),
            "longitude": lead.get('longitude'),
        }
        payload = {k: v for k, v in payload.items() if v is not None}

        try:
            resp = requests.post(API_URL, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                mapping[business_name] = data.get('demo_url')
                print(f"✅ {business_name} → {data.get('demo_url')}")
            else:
                print(f"❌ {business_name} failed: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"⚠️ {business_name} error: {e}")

        time.sleep(0.2)

    SHARED_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {len(mapping)} links to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()