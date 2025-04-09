from pydantic import BaseModel
from .enum import FigType

class FigCard(BaseModel):
    fig_type: FigType
    in_hand: bool
    is_blocked: bool
    is_used: bool