from pydantic import BaseModel
from typing import Optional, List
from models.Question import Question  # adjust the import path as needed

class Quiz(BaseModel):
    questions_count: int = 10
    questions: List[Question]
    min_passing_marks: int = 8
    meta_data: Optional[str] = None 
