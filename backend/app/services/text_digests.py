import requests
async def generate_text_digest(game_id: int) -> str:
    try:
        # Fetch game data from MLB API
        url = f"https://statsapi.mlb.com/api/v1.1/game/{game_id}/feed/live"
        response = requests.get(url)
        response.raise_for_status()
        game_data = response.json()

        # Summarize key highlights (adjust logic as needed)
        game_summary = game_data.get("gameData", {}).get("game", {}).get("type", "No summary available")
        return f"Game Highlights: {game_summary}"

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching game data: {e}")