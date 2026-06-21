import os
import requests

# 1. Safely read your hidden API key from GitHub Secrets
api_key = os.environ.get('FOOTBALL_API_KEY')

# 2. Configure the Football API (API-Football example)
url = "https://api-sports.io"
headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': api_key
}
params = {
    'league': '1',  # FIFA World Cup ID
    'season': '2026'
}

# 3. Fetch the live data
print("Fetching match data from the API...")
response = requests.get(url, headers=headers, params=PARAMS)
data = response.json()

# 4. Print match count to prove the script works in the cloud
match_count = len(data.get('response', []))
print(f"Successfully fetched {match_count} matches!")

# Next step will be adding code here to send this data to Google Sheets!
