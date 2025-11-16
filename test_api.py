import requests
import json

# The correct, public API endpoint used by the web application
api_url = 'https://api.polkamarkets.com/markets'

print(f"Attempting to connect to: {api_url} (via VPN)")

try:
    headers = {
        'User-Agent': 'MyMyriadBot/0.2'
    }
    
    # We filter for OPEN markets specifically from the MYRIAD platform.
    params = {
        'state': 'open',
        'slug': 'myriad' 
    }

    timeout_seconds = 15 # Increased timeout slightly just in case of VPN latency

    response = requests.get(api_url, headers=headers, params=params, timeout=timeout_seconds)

    print(f"Requesting URL: {response.url}")
    print(f"Response Status Code: {response.status_code}")

    response.raise_for_status()

    print("\n✅ Connection Successful! API Response:")
    markets_data = response.json()
    
    if markets_data:
        print("\nStructure of the first market found:")
        print(json.dumps(markets_data[0], indent=2))
    else:
        print("API returned an empty list of markets.")
            
except requests.exceptions.RequestException as e:
    print(f"\n❌ An error occurred during the request: {e}")