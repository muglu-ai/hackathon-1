from fastapi import APIRouter, HTTPException, Query

from app.utils.stats_api import (
    fetch_schedule,
    fetch_team_roster,
    fetch_team_info,
    fetch_player_info,
    fetch_live_game_data,
    fetch_game_timestamps,
    fetch_game_at_timecode,
    fetch_game_content,
)

router = APIRouter(prefix="/mlb", tags=["MLB Highlights"])


@router.get("/schedule/")
def get_schedule(season: int = Query(None, description="Season year (default: current year)"),
    game_type: str = Query("R", description="Game type (default: 'R')"),
    page: int = Query(1, description="Page number for pagination (default: 1)"),
    page_size: int = Query(10, description="Number of items per page (default: 10)"),
):
    """
    Get the MLB schedule for a given season and game type.
    """
    try:
        #print(season, game_type, page, page_size)
        return fetch_schedule(season, game_type, page, page_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/team/{team_id}/roster/{season}")
def get_team_roster(team_id: int, season: int):
    """
    Get the roster for a specific team and season.
    """
    try:
        return fetch_team_roster(team_id, season)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#fetch game content by game id
@router.get("/game/{game_pk}/content/")
def get_game_content(game_pk: int):
    """
    Get the content for a specific game.
    """
    try:
        return fetch_game_content(game_pk)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#get game highlights by game id

@router.get("/team/{team_id}/info/")
def get_team_info(team_id: int, season: int = None):
    """
    Get detailed information about a specific team.
    """
    try:
        return fetch_team_info(team_id, season)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/player/{player_id}/info/")
def get_player_info(player_id: int, season: int = None):
    """
    Get detailed information about a specific player.
    """
    try:
        return fetch_player_info(player_id, season)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/game/{game_pk}/live/")
def get_live_game_data(game_pk: int):
    """
    Get live game data for a specific game.
    """
    try:
        return fetch_live_game_data(game_pk)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/game/{game_pk}/timestamps/")
def get_game_timestamps(game_pk: int):
    """
    Get the list of update timestamps for a specific game.
    """
    try:
        return fetch_game_timestamps(game_pk)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/game/{game_pk}/timecode/")
def get_game_at_timecode(game_pk: int, timecode: str):
    """
    Get game data at a specific timecode.
    """
    try:
        return fetch_game_at_timecode(game_pk, timecode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
