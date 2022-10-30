from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Post(Base):
    __tablename__ = "post"
    
    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)

class Comment(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    question_id = Column(Integer, ForeignKey("post.id"))
    question = relationship("Post", backref="comments")