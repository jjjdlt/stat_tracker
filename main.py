from fastapi import FastAPI, Depends
from riot_api import RiotAPI

app = FastAPI()

def get_riot_api() -> RiotAPI:
    return RiotAPI(api_token="your_riot_api_token")

# fetches puuid
@app.get("/puuid")
def player_info(gameName: str, tagLine: str, riot_api: RiotAPI = Depends(get_riot_api)):
    puuid = riot_api.get_puuid(gameName, tagLine)
    return {"puuid": puuid}

# fetches summoner info
@app.get("/summoner-info")
def summoner_info(puuid: str, riot_api: RiotAPI = Depends(get_riot_api)):
    summoner_info = riot_api.get_summoner_info(puuid)
    return summoner_info

# fetches match history
@app.get("/summoner-matches")
def summoner_matches(puuid: str, riot_api: RiotAPI = Depends(get_riot_api)):
    matches = riot_api.get_summoner_matches(puuid)
    return matches

# fetches individual match stats
@app.get("/summoner-match-stats")
def summoner_match_stats(matchId: str, riot_api: RiotAPI = Depends(get_riot_api)):
    match_stats = riot_api.get_summoner_match_stats(matchId)
    return match_stats

# same thing as ^, need to integrate region selection
@app.get("/match-data")
def match_data(region: str, matchId: str, riot_api: RiotAPI = Depends(get_riot_api)):
    match_stats = riot_api.get_match_data(region, matchId)
    return match_stats

# fetches w/l
@app.get("/did-win")
def check_did_win(puuid: str, region: str, matchId: str, riot_api: RiotAPI = Depends(get_riot_api)):
    match_data = riot_api.get_match_data(region, matchId)
    did_win = riot_api.did_win(puuid, match_data)
    return {"did_win": did_win}
