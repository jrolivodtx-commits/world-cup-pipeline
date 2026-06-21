import csv
import requests

# 1. Connect to the public ESPN API endpoint
URL = "https://espn.com"

print("Connecting to ESPN API...")
response = requests.get(URL)
data = response.json()

cleaned_matches = []

# 2. Safely unpack the games list
events = data.get('events', [])
print(f"Found {len(events)} events to process.")

for event in events:
    match_id = event.get('id')
    
    # Extract status name (e.g., STATUS_FINAL, STATUS_SCHEDULED)
    status = event.get('status', {}).get('type', {}).get('name', 'UNKNOWN')
    
    # Grab the competitions list block
    competitions = event.get('competitions', [])
    if not competitions:
        continue
    
    # Index 0 contains the current match details
    match_detail = competitions[0]
    stage = match_detail.get('note', 'Tournament Match')
    
    # Competitors list: Index 0 is Home Team, Index 1 is Away Team
    competitors = match_detail.get('competitors', [])
    if len(competitors) >= 2:
        home_team_data = competitors[0]
        away_team_data = competitors[1]
        
        home_name = home_team_data.get('team', {}).get('displayName', 'TBD')
        away_name = away_team_data.get('team', {}).get('displayName', 'TBD')
        
        # Pull scores safely (ESPN stores scores as strings, we convert to numbers)
        try:
            home_score = int(home_team_data.get('score', 0))
            away_score = int(away_team_data.get('score', 0))
        except (ValueError, TypeError):
            home_score = 0
            away_score = 0
            
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

print(f"Successfully cleaned data for {len(cleaned_matches)} matches!")

# 3. Save directly to a local CSV file inside your repository
csv_filename = "world_cup_matches.csv"
fields = ["match_id", "stage", "status", "home_team", "away_team", "home_score", "away_score"]

with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(cleaned_matches)

print(f"File {csv_filename} successfully created and written.")
