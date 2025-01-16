from datetime import datetime

import requests
from starlette.responses import JSONResponse

BASE_URL = "https://statsapi.mlb.com/api/v1"
LIVE_GAME_BASE_URL = "https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"


def fetch_schedule(season: int = None, game_type: str = "R", page: int = 1, page_size: int = 10):
    """
    Fetch the MLB schedule for a given season and game type with pagination and necessary filtering.
    """
    # Use the current year as default if season is not provided
    if season is None:
        season = datetime.now().year

    # use default game type 'R' for regular season
    if game_type is None:
        game_type = "R"

    # Fetch data from the API
    url = f"{BASE_URL}/schedule?sportId=1&season={season}&gameType={game_type}"
    response = requests.get(url)
    response.raise_for_status()
    raw_data = response.json()



    # Extract total games for pagination
    total_games = raw_data.get("totalGames", 0)
    dates = raw_data.get("dates", [])

    # Filter the games based on pagination
    games = []
    for date_info in dates:
        for game in date_info.get("games", []):
            games.append({
                "gameId": game["gamePk"],
                "gameDate": game["gameDate"],
                "status": game["status"]["detailedState"],
                "teams": {
                    "home": {
                        "teamId": game["teams"]["home"]["team"]["id"],
                        "name": game["teams"]["home"]["team"]["name"],
                    },
                    "away": {
                        "teamId": game["teams"]["away"]["team"]["id"],
                        "name": game["teams"]["away"]["team"]["name"],
                    },
                },
                "venue": {
                    "venueId": game["venue"]["id"],
                    "name": game["venue"]["name"],
                },
                "dayOrNight": game["dayNight"],
                "description": game["description"],
                "seriesDescription": game["seriesDescription"],
            })



    # Apply pagination
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_games = games[start_idx:end_idx]

    # Construct the response
    return JSONResponse(content={
        "season": season,
        "gameType": game_type,
        "totalGames": total_games,
        "page": page,
        "pageSize": page_size,
        "games": paginated_games,
    })


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
