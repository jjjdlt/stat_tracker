from fastapi import APIRouter, Depends, Request
from app.models.riot_api import RiotAPI
from app.models.schema import PlayerRequest, PUUIDResponse, SummonerInfoResponse, MatchHistoryResponse, MatchStatsResponse, DidWinResponse

router = APIRouter()

def get_riot_api() -> RiotAPI:
    return RiotAPI()

# Route to fetch puuid and store it in the app state
@router.post("/puuid", response_model=PUUIDResponse)
def player_info(player: PlayerRequest, request: Request, riot_api: RiotAPI = Depends(get_riot_api)):
    # Fetch the PUUID
    puuid = riot_api.get_puuid(player.gameName, player.tagLine)

    # Store PUUID in the app state
    request.app.state.puuid = puuid
    return PUUIDResponse(puuid=puuid)

# Reusable dependency to get PUUID from app state
def get_puuid_from_state(request: Request):
    puuid = request.app.state.puuid
    if not puuid:
        raise HTTPException(status_code=404, detail="PUUID not found in state. Make a POST request to /puuid first.")
    return puuid

# Route to fetch summoner info using stored PUUID
@router.get("/summoner-info", response_model=SummonerInfoResponse)
def summoner_info(puuid: str = Depends(get_puuid_from_state), riot_api: RiotAPI = Depends(get_riot_api)):
    summoner_info = riot_api.get_summoner_info(puuid)
    return SummonerInfoResponse(
        id=summoner_info['id'],
        accountId=summoner_info['accountId'],
        profileIconId=summoner_info['profileIconId'],
        summonerLevel=summoner_info['summonerLevel']
    )

# Route to fetch match history using stored PUUID
@router.get("/summoner-matches", response_model=MatchHistoryResponse)
def summoner_matches(puuid: str = Depends(get_puuid_from_state), riot_api: RiotAPI = Depends(get_riot_api)):
    matches = riot_api.get_summoner_matches(puuid)
    return MatchHistoryResponse(matches=matches['matches'])

# Route to fetch individual match stats using stored PUUID
@router.get("/summoner-match-stats", response_model=MatchStatsResponse)
def summoner_match_stats(matchId: str, puuid: str = Depends(get_puuid_from_state), riot_api: RiotAPI = Depends(get_riot_api)):
    match_stats = riot_api.get_summoner_match_stats(matchId)
    return MatchStatsResponse(match_stats=match_stats)

# Route to fetch match data based on region and matchId using stored PUUID
@router.get("/match-data", response_model=MatchStatsResponse)
def match_data(region: str, matchId: str, puuid: str = Depends(get_puuid_from_state), riot_api: RiotAPI = Depends(get_riot_api)):
    match_stats = riot_api.get_match_data(region, matchId)
    return MatchStatsResponse(match_stats=match_stats)

# Route to check if player won using stored PUUID
@router.get("/did-win", response_model=DidWinResponse)
def check_did_win(region: str, matchId: str, puuid: str = Depends(get_puuid_from_state), riot_api: RiotAPI = Depends(get_riot_api)):
    match_data = riot_api.get_match_data(region, matchId)
    did_win = riot_api.did_win(puuid, match_data)
    return DidWinResponse(did_win=did_win)
