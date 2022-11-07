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

class UserCreate(BaseModel):
    username: str
    full_name: str
    password1: str
    password2: str
    email: EmailStr

    @validator('username', 'password1', 'password2', 'email')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @validator('password2')
    def passwords_match(cls, v, values):
        if 'password1' in values and v != values['password1']:
            raise ValueError('비밀번호가 일치하지 않습니다')
        return v

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

    class Config:
        orm_mode = True