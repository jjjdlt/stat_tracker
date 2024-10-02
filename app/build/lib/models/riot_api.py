import os
import requests
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

RIOT_API_TOKEN = os.getenv("RIOT_API_TOKEN")
if not RIOT_API_TOKEN:
    raise ValueError("Riot Games API token is missing in environment variables")

class RiotAPI:
    def __init__(self):
        self.api_token = RIOT_API_TOKEN

    # func for getting puuid from riot
    def get_puuid(self, gameName: str, tagLine: str):
        url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}?api_key={self.api_token}"

        response = requests.get(url)

        if response.status_code != 200:
            print(f"Error fetching player info: {response.content}")
            raise HTTPException(status_code=response.status_code, detail="Error fetching player info")

        player_info = response.json()
        puuid = player_info['puuid']
        return puuid

    # func that takes puuid and returns id + other values
    def get_summoner_info(self, puuid: str):
        url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={self.api_token}"

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error fetching summoner info: {response.content}")
            raise HTTPException(status_code=response.status_code, detail="Error fetching summoner info")

        summoner_info = response.json()
        return {
            "id": summoner_info["id"],
            "accountId": summoner_info["accountId"],
            "profileIconId": summoner_info["profileIconId"],
            "summonerLevel": summoner_info["summonerLevel"]
        }

    # gets list of the last 20 matches from puuid
    def get_summoner_matches(self, puuid: str):
        url = f"https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key={self.api_token}"

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error fetching summoner info: {response.content}")
            raise HTTPException(status_code=response.status_code, detail="Error fetching summoner info")

        matches = response.json()
        return {"matches": matches}

    # gets stats of each individual match
    def get_summoner_match_stats(self, matchId: str):
        url = f"https://americas.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={self.api_token}"

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Error fetching summoner info: {response.content}")
            raise HTTPException(status_code=response.status_code, detail="Error fetching summoner info")

        match_stats = response.json()
        return {"match_stats": match_stats}

    # function trying to get match data with region and matchId
    def get_match_data(self, region: str, matchId: str):
        url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{matchId}?api_key={self.api_token}"

        response = requests.get(url)
        match_stats = response.json()
        return match_stats

    # func that goes through a match's data seeing if the participant (puuid) won
    def did_win(self, puuid: str, match_data: dict):
        part_index = match_data['metadata']['participants'].index(puuid)
        return match_data['info']['participants'][part_index]['win']
