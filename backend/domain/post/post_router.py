from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from domain.post import post_schema
from models import Post, Comment, User
from pydantic import BaseModel
from domain.user.user_router import get_current_user

router = APIRouter(
    prefix="/api/post",
    tags=["post"]
)

def get_post(db: Session, question_id: int):
    post = db.query(Post).get(question_id)
    return post

@router.get("/list", response_model=list[post_schema.Post])
def question_list(db: Session = Depends(get_db)):
    _question_list = db.query(Post).order_by(Post.create_date.desc()).all()
    return _question_list

@router.get("/search/{search_tag}", response_model=list[post_schema.Post])
def question_search(search_tag: str, db: Session = Depends(get_db)):
    _question_list = db.query(Post).filter(Post.subject.contains(search_tag)).order_by(Post.create_date.desc()).all()
    return _question_list


class GetPost(BaseModel):
    subject: str
    content: str

@router.post("/create_item")
def create_item(post: GetPost, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    q = Post(subject=post.subject, content=post.content, create_date=datetime.now(), user=current_user)
    db.add(q)
    db.commit()
    return {"Status":"ok", "data": "item commited to DB"}

@router.get("/{id}/detail", response_model=post_schema.Post)
def question_detail(id: int, db: Session = Depends(get_db)):
    _question = db.query(Post).get(id)
    return _question

@router.put("/{id}/update", response_model=post_schema.Post)
def question_update(id: int, post: GetPost, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_post = get_post(db, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_post.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")
    db_post.subject = post.subject
    db_post.content = post.content
    db.commit()
    return db_post

@router.delete("/{id}/delete")
def delete_item(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_post = get_post(db, id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_post.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")

    db.delete(db_post)
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
def create_comment(id: int, comment: GetComment, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_post = get_post(db, id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Question not found")
    c = Comment(content=comment.content, create_date=datetime.now(), question=db_post, user=current_user)
    db.add(c)
    db.commit()
    return {"Status":"ok", "data": "item commited to DB"}

@router.delete("/delete_comment/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_comment = db.query(Comment).filter(Comment.id==comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_comment.user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    
    db.delete(db_comment)
    db.commit()
    return {"Status":"ok", "data": "Comment Deleted"}