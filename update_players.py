import json
import os
import requests
import random

API_KEY = os.environ.get("STEAM_API_KEY")


def resolve_vanity(vanity_url):
    url = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/"
    params = {"key": API_KEY, "vanityurl": vanity_url}
    try:
        response = requests.get(url, timeout=10).json()
        if response.get("response", {}).get("success") == 1:
            return response["response"]["steamid"]
    except:
        pass
    return None


def get_tf2_hours(steamid64):
    url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
    params = {
        "key": API_KEY,
        "steamid": steamid64,
        "include_appinfo": False
    }
    try:
        response = requests.get(url, params=params, timeout=10).json()
        games = response.get("response", {}).get("games", [])
        for game in games:
            if game["appid"] == 440:
                return round(game["playtime_forever"] / 60, 2)
    except:
        pass
    return None


with open("playersupdated.json", "r") as f:
    players = json.load(f)


for player in players:
    profile = player["profile"].rstrip("/").split("/")[-1]
    steamid = resolve_vanity(profile)
    hours = get_tf2_hours(steamid) if steamid else None

    if hours is not None:
        player["hoursPlayed"] = hours
    else:
        player["hoursPlayed"] += round(random.uniform(2, 3), 2)
        print(f"Could not fetch real hours for {player['name']}, adding 2-3 hours.")


with open("playersupdated.json", "w") as f:
    json.dump(players, f, indent=4)

print("done!")
