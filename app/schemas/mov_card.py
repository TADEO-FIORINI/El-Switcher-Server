from pydantic import BaseModel
from .enum import MovType

class MovCard(BaseModel):
    mov_type: MovType
    is_used: bool
