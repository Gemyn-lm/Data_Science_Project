import requests
import time
import pandas as pd

API_KEY = "RGAPI-7c165fce-adea-448b-8577-9d6b8ede81f1"
REGION = "eu"
HEADERS = {"X-Riot-Token": API_KEY}
CURRENT_ACT_ID = "0c9a4b79-46a0-4a2a-beb0-5b5690d9b742"

def get_content(region=REGION):
    url = f"https://{region}.api.riotgames.com/val/content/v1/contents"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

def get_leaderboard(act_id, region=REGION):
    url = f"https://{region}.api.riotgames.com/val/ranked/v1/leaderboards/by-act/{act_id}"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

def get_matchlists_by_puuid(puuid, region=REGION):
    url = f"https://{region}.api.riotgames.com/val/match/v1/matchlists/by-puuid/{puuid}"
    try:
        resp = requests.get(url, headers=HEADERS)
        resp.raise_for_status()
        print(f"OK !")
        return resp.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            print(f"⚠️ Accès interdit pour le joueur {puuid} (stats anonymisées)")
            return {"history": []} 
        else:
            raise

def get_match_details(match_id, region=REGION):
    url = f"https://{region}.api.riotgames.com/val/match/v1/matches/{match_id}"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

def collect_player_data(player_puuid, max_matches=50):
    matches = get_matchlists_by_puuid(player_puuid)
    data = []
    count = 0
    for entry in matches.get("history", []):
        match_id = entry.get("matchId")
        if count >= max_matches:
            break
        detail = get_match_details(match_id)
        players = detail.get("players")
        agent = "0"
        isWin = False

        for i in players:
            if i.puuid == player_puuid:
                agent = i.characterId
                isWin = i.get("teamId").get("won", False)

        data.append({"match_id": match_id, "map": detail.get("mapId"), "agent": agent, "IsWin" : isWin })
        count += 1
        time.sleep(1)
    return pd.DataFrame(data)

def get_current_act(region=REGION):
    url = f"https://{region}.api.riotgames.com/val/content/v1/contents"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    acts = [a for a in data["acts"] if a["isActive"]]
    return acts[1]["id"] if acts else None

act_id = get_current_act()
lb = get_leaderboard(act_id)

puuids = [p["puuid"] for p in lb["players"][:200]]
all_data = []
for puuid in puuids:
    df = collect_player_data(puuid, max_matches=100)
    all_data.append(df)
full_df = pd.concat(all_data, ignore_index=True)
print(df)