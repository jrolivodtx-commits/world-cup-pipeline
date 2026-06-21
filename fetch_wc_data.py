import json
import requests

# 1. ESPN Public World Cup API Endpoint
URL = "https://espn.com"

print("Connecting to ESPN API...")
response = requests.get(URL)
data = response.json()

cleaned_matches = []

# 2. Loop through all matches found in the API response
for event in data.get('events', []):
    match_id = event.get('id')
    
    # Extract match status (e.g., "STATUS_FINAL", "STATUS_IN_PROGRESS")
    status = event.get('status', {}).get('type', {}).get('name')
    
    # Extract competition details (Stage Name like "Group A" or "Quarterfinals")
    competition = event.get('competitions', [{}])[0]
    stage = competition.get('note', 'Tournament Match') 
    
    # ESPN lists teams as "competitors". Usually index 0 is Home, index 1 is Away
    competitors = competition.get('competitors', [])
    if len(competitors) >= 2:
        home_team_data = competitors[0]
        away_team_data = competitors[1]
        
        home_name = home_team_data.get('team', {}).get('displayName')
        away_name = away_team_data.get('team', {}).get('displayName')
        
        # Extract scores (convert to integer, default to 0 if not played yet)
        home_score = int(home_team_data.get('score', 0))
        away_score = int(away_team_data.get('score', 0))
        
        # Save a clean record of this match
        match_record = {
            "match_id": match_id,
            "stage": stage,
            "status": status,
            "home_team": home_name,
            "away_team": away_name,
            "home_score": home_score,
            "away_score": away_score
        }
        cleaned_matches.append(match_record)

print(f"Successfully cleaned {len(cleaned_matches)} matches from ESPN!")

# Temporary print to prove it works in GitHub actions log
print(json.dumps(cleaned_matches[:2], indent=2))
