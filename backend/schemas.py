from pydantic import BaseModel
from typing import List, Optional

class PreferenceCreate(BaseModel):
    user_id: int
    team_ids: List[int]  # IDs of teams the user wants to follow
    player_ids: List[int]  # IDs of players the user wants to follow

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    language: Optional[str] = "en"

    class Config:
        orm_mode = True
