import requests, json, os
from pathlib import Path

# Read token from .env
try:
    with open('C:\\bitcoin\\x-intel\\.env', 'r') as f:
        for line in f:
            if line.startswith('BLOCKHORIZON_TOKEN='):
                token = line.split('=', 1)[1].strip()
                break
except:
    print("ERROR: Token not found in .env")
    exit(1)

# Fetch data from BlockHorizon
try:
    r = requests.post(
        'https://zbvrubdalcojapjygbcz.supabase.co/rest/v1/rpc/get_metrics',
        headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
        json={},
        timeout=30
    )
    
    if r.status_code == 200:
        print("OK: Data received")
        data = {
            "generated_at": __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
            "metrics": r.json()[0] if isinstance(r.json(), list) else r.json()
        }
        Path('C:\\bitcoin\\data-v73\\data\\blockhorizon.json').parent.mkdir(parents=True, exist_ok=True)
        Path('C:\\bitcoin\\data-v73\\data\\blockhorizon.json').write_text(json.dumps(data, indent=2))
        print("Saved: C:\\bitcoin\\data-v73\\data\\blockhorizon.json")
    else:
        print(f"ERROR: HTTP {r.status_code}")
        exit(1)
except Exception as e:
    print(f"ERROR: {e}")
    exit(1)
