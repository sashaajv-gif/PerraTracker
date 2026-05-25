import requests
from datetime import datetime, timezone

STEAM_API_KEY = "B4180024D26162FB22F88A674145EB91"
STEAM_ID = "76561198088072398"

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1508526265332924558/viZqhN-YgpXpzpzxlJfTUG_iAEcwKHuthQmDBPwRZfj633j5l52W2DtcsNaa2SodTw4k"


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

        return f"Perttu ollut offline {days_offline} päivää."

    return "Steam-profiili on online!!!."


message = get_steam_status()

requests.post(
    DISCORD_WEBHOOK,
    json={
        "content": message
    }
)
