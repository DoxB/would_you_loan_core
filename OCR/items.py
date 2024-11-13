from pydantic import BaseModel

class FileNameRequest(BaseModel):
    file_name: str
    user_id: int