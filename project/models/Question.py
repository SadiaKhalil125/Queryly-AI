from pydantic import BaseModel
from typing import Optional, List
from models.Option import Option  # adjust the import path as needed

class Question(BaseModel):
    topic: str
    description: str
    options: List[Option]
    correct_option_id: int
