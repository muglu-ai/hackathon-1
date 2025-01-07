import requests

BASE_URL = "https://statsapi.mlb.com/api/v1"
LIVE_GAME_BASE_URL = "https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"


def fetch_schedule(season: int, game_type: str = "R"):
    """
    Fetch the MLB schedule for a given season and game type.
    """
    url = f"{BASE_URL}/schedule?sportId=1&season={season}&gameType={game_type}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def fetch_team_roster(team_id: int, season: int):
    """
    Fetch the roster for a specific team and season.
    """
    url = f"{BASE_URL}/teams/{team_id}/roster?season={season}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def fetch_team_info(team_id: int, season: int = None):
    """
    Fetch detailed information about a specific team.
    """
    url = f"{BASE_URL}/teams/{team_id}"
    if season:
        url += f"?season={season}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def fetch_player_info(player_id: int, season: int = None):
    """
    Fetch detailed information about a specific player.
    """
    url = f"{BASE_URL}/people/{player_id}"
    if season:
        url += f"?season={season}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def fetch_live_game_data(game_pk: int):
    """
    Fetch live game data for a specific game.
    """
    url = LIVE_GAME_BASE_URL.format(game_pk=game_pk)
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def fetch_game_timestamps(game_pk: int):
    """
    Fetch the list of update timestamps for a specific game.
    """
    url = f"{LIVE_GAME_BASE_URL.format(game_pk=game_pk)}/timestamps"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def fetch_game_at_timecode(game_pk: int, timecode: str):
    """
    Fetch game data at a specific timecode.
    """
    url = f"{LIVE_GAME_BASE_URL.format(game_pk=game_pk)}?timecode={timecode}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
