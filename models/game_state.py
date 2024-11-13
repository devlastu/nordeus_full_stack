# app/models/game_state.py
from pydantic import BaseModel

class GameState(BaseModel):
    selected_island: str
    attempts: int = 0


class Coordinates(BaseModel):
    x: float
    y: float