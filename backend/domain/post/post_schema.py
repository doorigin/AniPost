import datetime
from pydantic import BaseModel, validator, EmailStr
class Post(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime

    class Config:
        orm_mode = True

class Comment(BaseModel):
    id: int
    content: str
    question: int
    create_date: datetime.datetime

    class Config:
        orm_mode = True
