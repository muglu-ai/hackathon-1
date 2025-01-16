from fastapi import APIRouter, HTTPException, Query

from utils.stats_api import (
    fetch_schedule,
    fetch_team_roster,
    fetch_team_info,
    fetch_player_info,
    fetch_live_game_data,
    fetch_game_timestamps,
    fetch_game_at_timecode,
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
