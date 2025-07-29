from pydantic import BaseModel
class QuizRequest(BaseModel):
    topic:str