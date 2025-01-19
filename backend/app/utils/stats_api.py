from datetime import datetime

import requests
from fastapi.responses import JSONResponse
import json



BASE_URL = "https://statsapi.mlb.com/api/v1"
LIVE_GAME_BASE_URL = "https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"
CONTENT_FETCH_URL = "https://statsapi.mlb.com/api/v1/game/{game_pk}/content"


def fetch_schedule(season: int = None, game_type: str = "R", page: int = 1, page_size: int = 12):
    """
    Fetch the MLB schedule for a given season and game type with pagination and necessary filtering.
    """
    # Use the current year as default if season is not provided
    if season is None:
        season = datetime.now().year

        # Use default game type 'R' for regular season
    if not game_type:
        game_type = "R"

        # Fetch data from the API
    url = f"{BASE_URL}/schedule?sportId=1&season={season}&gameType={game_type}"
    response = requests.get(url)
    response.raise_for_status()
    raw_data = response.json()

    # Save raw data to a text file
    with open("schedule_data.txt", "w") as file:
        json.dump(raw_data, file, indent=4)

    # Extract total games for pagination
    total_games = raw_data.get("totalGames", 0)
    dates = raw_data.get("dates", [])
    games = []

    # Parse game data
    for date_info in dates:
        for game in date_info.get("games", []):
            games.append({
                "gameId": game.get("gamePk"),
                "gameDate": game.get("gameDate"),
                "status": game.get("status", {}).get("detailedState"),
                "teams": {
                    "home": {
                        "teamId": game.get("teams", {}).get("home", {}).get("team", {}).get("id"),
                        "name": game.get("teams", {}).get("home", {}).get("team", {}).get("name"),
                        "wins": game.get("teams", {}).get("home", {}).get("leagueRecord", {}).get("wins", 0),
                        "losses": game.get("teams", {}).get("home", {}).get("leagueRecord", {}).get("losses", 0),
                    },
                    "away": {
                        "teamId": game.get("teams", {}).get("away", {}).get("team", {}).get("id"),
                        "name": game.get("teams", {}).get("away", {}).get("team", {}).get("name"),
                         "wins": game.get("teams", {}).get("away", {}).get("leagueRecord", {}).get("wins", 0),
                        "losses": game.get("teams", {}).get("away", {}).get("leagueRecord", {}).get("losses", 0),
                    },
                },
                "venue": {
                    "venueId": game.get("venue", {}).get("id"),
                    "name": game.get("venue", {}).get("name"),
                },

                "content":{
                    "link": game.get("content", {}).get("link"),
                },

                "dayOrNight": game.get("dayNight"),
                "description": game.get("description"),
                "seriesDescription": game.get("seriesDescription"),
            })



    # Apply pagination
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    #print(games)
    paginated_games = games[start_idx:end_idx]

    # Construct and return the response
    response_data = {
        "season": season,
        "gameType": game_type,
        "totalGames": total_games,
        "page": page,
        "pageSize": page_size,
        "games": paginated_games,
    }

    return response_data

def fetch_game_content(game_pk):
    """
    Fetch the content for a specific game.
    """
    url = f"{CONTENT_FETCH_URL.format(game_pk=game_pk)}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    recap = data.get('editorial', {}).get('recap', {}).get('mlb', {})

    headline = recap.get('headline')
    seo_title = recap.get('seoTitle')
    slug = recap.get('slug')
    blurb = recap.get('blurb')
    date = recap.get('date')

    # Keywords and Image
    keywords = recap.get('keywordsAll', [])
    image_details = recap.get('image', {})
    image_title = image_details.get('title')
    image_url = image_details.get('templateUrl')
    image_full_url = None

    # Extracting the highest-resolution image (if available)
    if 'cuts' in image_details:
        image_cuts = image_details['cuts']
        if image_cuts:
            image_full_url = image_cuts[0].get('src')  # Picking the first cut as an example

    keywords_all = data.get('editorial', {}).get('recap', {}).get('mlb', {}).get('keywordsAll', [])
    team = {}
    game = {}
    player = {}
    result = {
        "images": [],
        "videos": [],
        "highlights": []
    }

    # Iterating through keywordsAll and filtering by type
    for keyword in keywords_all:
        if keyword.get('type') == 'game':
            if keyword.get('value').startswith('gamepk'):
                game = {
                    'type': 'game',
                    'value': keyword.get('value'),
                    'displayName': f"Game {keyword.get('value').split('-')[1]}"
                    # You can customize the display name as needed
                }
        elif keyword.get('type') == 'team':
            team = {
                'type': 'team',
                'value': keyword.get('value'),
                'displayName': keyword.get('displayName', 'Unknown Team')  # Use 'Unknown Team' as a fallback
            }
        elif keyword.get('type') == 'player_id':
            player = {
                'type': 'player_id',
                'value': keyword.get('value'),
                'displayName': f"{keyword.get('displayName')}"  # Customize the display name
            }

    result = {
        "images": [],
        "videos": [],
        "highlights": {
            "images": [],
            "videos": []
        }
    }

    # Process `epgAlternate` for specific images and videos
    epg_alternate = data.get("media", {}).get("epgAlternate", [])

    # Process `epgAlternate` for specific images and videos
    # Process `epgAlternate` for specific images and videos
    for section in epg_alternate:
        items = section.get("items", [])
        for item in items:
            # Extract videos with specific playback names
            if item.get("type") == "video":
                filtered_playbacks = [
                    playback for playback in item.get("playbacks", [])
                    if playback.get("name") in ["mp4Avc", "highBit"]
                ]
                if filtered_playbacks:
                    video_data = {
                        "title": item.get("title"),
                        "description": item.get("description"),
                        "duration": item.get("duration"),
                        "playbacks": filtered_playbacks
                    }

                    # Check if the title contains "Highlights" to classify as a highlight video
                    if "Highlights" in item.get("title", ""):
                        result["highlights"]["videos"].append(video_data)
                    else:
                        result["videos"].append(video_data)

            # Extract specific image sizes
            image_cuts = item.get("image", {}).get("cuts", [])
            filtered_images = [
                {
                    "title": item.get("image", {}).get("title", ""),
                    "width": cut.get("width"),
                    "height": cut.get("height"),
                    "src": cut.get("src")
                }
                for cut in image_cuts if
                (cut.get("width"), cut.get("height")) in [(1920, 1080), (1280, 720), (496, 279)]
            ]

            # Check if the title contains "Highlights" to classify as highlight images
            if "Highlights" in item.get("image", {}).get("title", ""):
                result["highlights"]["images"].extend(filtered_images)
            else:
                result["images"].extend(filtered_images)

    # Process `previewStory` for additional highlights
    preview_story = data.get("media", {}).get("previewStory", {}).get("items", [])
    for item in preview_story:
        # Extract highlight images
        highlight_images = [
            {
                "title": item.get("image", {}).get("title", ""),
                "width": cut.get("width"),
                "height": cut.get("height"),
                "src": cut.get("src")
            }
            for cut in item.get("image", {}).get("cuts", [])
            if cut.get("width") in [1440, 1280, 684]
        ]
        if "Highlights" in item.get("image", {}).get("title", ""):
            result["highlights"]["images"].extend(highlight_images)
        else:
            result["images"].extend(highlight_images)

        # Extract highlight videos
        highlight_videos = [
            playback for playback in item.get("playbacks", [])
            if playback.get("name") in ["mp4Avc", "highBit"]
        ]
        if highlight_videos:
            video_data = {
                "title": item.get("title"),
                "playbacks": highlight_videos
            }
            if "Highlights" in item.get("title", ""):
                result["highlights"]["videos"].append(video_data)
            else:
                result["videos"].append(video_data)

    response_data = {
        "headline": headline,
        "seoTitle": seo_title,
        "slug": slug,
        "blurb": blurb,
        "date": date,
        "gameID" : game,
        "team": team,
        "players": player,
        "image": {
            "title": image_title,
            "templateUrl": image_url,
            "fullUrl": image_full_url,
        },
        'content': result,

    }
    return response_data


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
