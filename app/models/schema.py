from pydantic import BaseModel
from typing import List

# Model for a request with gameName and tagLine
class PlayerRequest(BaseModel):
    gameName: str
    tagLine: str

# Model for PUUID response
class PUUIDResponse(BaseModel):
    puuid: str

# Model for summoner info response
class SummonerInfoResponse(BaseModel):
    id: str
    accountId: str
    profileIconId: int
    summonerLevel: int

# Model for match history (list of match IDs)
class MatchHistoryResponse(BaseModel):
    matches: List[str]

# Model for match stats
class MatchStatsResponse(BaseModel):
    match_stats: dict  # You can adjust this to reflect the exact structure if you want more detail

# Model for win/loss check
class DidWinResponse(BaseModel):
    did_win: bool
