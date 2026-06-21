import csv
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
    
    # Extract match status
    status = event.get('status', {}).get('type', {}).get('name')
    
    # Extract competition details
    competitions = event.get('competitions', [{}])[0]
    stage = competitions.get('note', 'Tournament Match') 
    
    # ESPN lists teams as competitors. Index 0 is Home, Index 1 is Away
    competitors = competitions.get('competitors', [])
    if len(competitors) >= 2:
        home_team_data = competitors[0]
        away_team_data = competitors[1]
        
        home_name = home_team_data.get('team', {}).get('displayName')
        away_name = away_team_data.get('team', {}).get('displayName')
        
        # Extract scores
        home_score = int(home_team_data.get('score', 0))
        away_score = int(away_team_data.get('score', 0))
        
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

# 3. Save the data to a CSV file
csv_filename = "world_cup_matches.csv"
fields = ["match_id", "stage", "status", "home_team", "away_team", "home_score", "away_score"]

with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(cleaned_matches)

print(f"Saved data to {csv_filename}")
