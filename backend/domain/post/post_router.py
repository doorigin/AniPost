from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from domain.post import post_schema
from models import Post, Comment
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/post",
    tags=["post"]
)

@router.get("/list", response_model=list[post_schema.Question])
def question_list(db: Session = Depends(get_db)):
    _question_list = db.query(Post).order_by(Post.create_date.desc()).all()
    return _question_list

@router.get("/search/{search_tag}", response_model=list[post_schema.Question])
def question_list(search_tag: str, db: Session = Depends(get_db)):
    _question_list = db.query(Post).filter(Post.subject.contains(search_tag)).order_by(Post.create_date.desc()).all()
    return _question_list


class GetPost(BaseModel):
    subject: str
    content: str

@router.post("/create_item")
def create_item(post: GetPost, db: Session = Depends(get_db)):
    q = Post(subject=post.subject, content=post.content, create_date=datetime.now())
    db.add(q)
    db.commit()
    return {"Status":"ok", "data": "item commited to DB"}

@router.get("/{id}/detail", response_model=post_schema.Question)
def question_list(id: int, db: Session = Depends(get_db)):
    _question = db.query(Post).get(id)
    return _question

@router.put("/{id}/update", response_model=post_schema.Question)
def question_list(id: int, post: GetPost, db: Session = Depends(get_db)):
    q = db.query(Post).get(id)
    q.subject = post.subject
    q.content = post.content
    db.commit()
    return q

@router.delete("/{id}/delete")
def delete_item(id: int, db: Session = Depends(get_db)):
    q = db.query(Post).get(id)
    db.delete(q)
    db.commit()
    return {"Status":"ok", "data": "item deleted"}

# comments
@router.get("/{id}/comments")
def comment_list(id: int, db: Session = Depends(get_db)):
    _question = db.query(Post).get(id)
    return _question.comments

class GetComment(BaseModel):
    content: str

@router.post("/{id}/create_comment")
def create_comment(id: int, comment: GetComment, db: Session = Depends(get_db)):
    q = db.query(Post).get(id)
    c = Comment(content=comment.content, create_date=datetime.now(), question=q)
    db.add(c)
    db.commit()
    return {"Status":"ok", "data": "item commited to DB"}

@router.delete("/delete_comment/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    c = db.query(Comment).filter(Comment.id==comment_id).first()
    db.delete(c)
    db.commit()
    return {"Status":"ok", "data": "Comment Deleted"}