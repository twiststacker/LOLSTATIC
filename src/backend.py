import requests
import time
from .config import load_config

cfg = load_config()

class Backend:
    def __init__(self):
        self.riot_key = cfg["RIOT_KEY"]
        self.ollama_url = cfg["OLLAMA_URL"]
        self.ollama_model = cfg["OLLAMA_MODEL"]
        self.ollama_key = cfg["OLLAMA_KEY"]
        self.headers = {"X-Riot-Token": self.riot_key.strip()}

    def get_routing(self, region):
        """Maps region code (EUW1) to routing region (europe)."""
        routing_map = {
            "NA1": "americas", "BR1": "americas", "LA1": "americas", "LA2": "americas",
            "EUW1": "europe", "EUN1": "europe", "TR1": "europe", "RU": "europe",
            "KR": "asia", "JP1": "asia",
            "OC1": "sea"
        }
        return routing_map.get(region, "europe")

    def get_player_puuid(self, name, tag, region):
        routing = self.get_routing(region)
        url = f"https://{routing}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}"
        try:
            r = requests.get(url, headers=self.headers)
            if r.status_code == 200:
                return r.json()['puuid']
        except: pass
        return None

    def get_recent_matches(self, puuid, region, count=3):
        routing = self.get_routing(region)
        url = f"https://{routing}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}"
        try:
            r = requests.get(url, headers=self.headers)
            if r.ok:
                return r.json()
        except: pass
        return []

    def analyze_match(self, match_id, puuid, region):
        routing = self.get_routing(region)
        url = f"https://{routing}.api.riotgames.com/lol/match/v5/matches/{match_id}"
        try:
            r = requests.get(url, headers=self.headers)
            if not r.ok: return None
            
            data = r.json()
            for p in data['info']['participants']:
                if p['puuid'] == puuid:
                    k, d, a = p['kills'], p['deaths'], p['assists']
                    cs = p['totalMinionsKilled'] + p['neutralMinionsKilled']
                    champion = p['championName']
                    return f"Champ: {champion} | KDA: {k}/{d}/{a} | CS: {cs}"
        except: pass
        return None

    def ask_ai(self, prompt, callback):
        """Sends prompt to Ollama and runs callback(text) when done."""
        try:
            payload = {"model": self.ollama_model, "prompt": prompt, "stream": False}
            headers = {}
            if self.ollama_key: headers["Authorization"] = f"Bearer {self.ollama_key}"
            
            resp = requests.post(self.ollama_url, json=payload, headers=headers)
            if resp.ok:
                callback(resp.json()['response'])
            else:
                callback(f"❌ AI Error: {resp.status_code}")
        except Exception as e:
            callback(f"❌ AI Connection Failed: {e}")

    def get_patch_version(self):
        try:
            r = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
            if r.ok: return r.json()[0]
        except: pass
        return "Latest"
    
    def get_champions(self, patch):
        try:
            url = f"https://ddragon.leagueoflegends.com/cdn/{patch}/data/en_US/champion.json"
            return list(requests.get(url).json()['data'].keys())
        except: return []
def get_patch_data(self, patch):
    # This fetches the core changes for the current patch
    url = f"https://ddragon.leagueoflegends.com/cdn/{patch}/data/en_US/champion.json"
    return requests.get(url).json()