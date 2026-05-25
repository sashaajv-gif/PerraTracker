import os
import requests
from datetime import datetime, timezone
from datetime import datetime, timezone

STEAM_API_KEY = os.environ["STEAM_API_KEY"]
STEAM_ID = os.environ["STEAM_ID"]
DISCORD_WEBHOOK = os.environ["DISCORD_WEBHOOK"]

def get_steam_status():
    url = (
        "https://api.steampowered.com/"
        "ISteamUser/GetPlayerSummaries/v0002/"
    )

    params = {
        "key": STEAM_API_KEY,
        "steamids": STEAM_ID
    }

    r = requests.get(url, params=params)
    data = r.json()

    player = data["response"]["players"][0]

    persona_state = player.get("personastate", 0)
    last_logoff = player.get("lastlogoff", 0)

    offline = persona_state == 0

    if offline:
        last_online = datetime.fromtimestamp(
            last_logoff,
            tz=timezone.utc
        )

        now = datetime.now(timezone.utc)

        days_offline = (now - last_online).days

        return f"Perttu on ollut offline {days_offline} päivää."

    return "Perttu on online!!!."


message = get_steam_status()

requests.post(
    DISCORD_WEBHOOK,
    json={
        "content": message
    }
)
