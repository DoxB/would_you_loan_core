from pydantic import BaseModel

class QuestionRequest(BaseModel):
    user_question: str
    user_id: int

class KeywordRequest(BaseModel):
    report_location: str