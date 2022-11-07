from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from database import get_db
from domain.post import post_schema
from models import Post, Comment, User
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext

router = APIRouter(
    prefix="/api"
    # tags=["post"]
)

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    user = db.query(User).filter(User.username == username).first()
    if user:
        return post_schema.UserInDB(
            username = user.username,
            email = user.email,
            full_name = user.full_name,
            disabled = user.disabled,
            hashed_password = user.hashed_password
        )

def authenticate_user(db: Session, username: str, password: str):
    u = get_user(db, username)
    if not u:
        return False
    if not verify_password(password, u.hashed_password):
        return False
    return u


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/token", response_model=Token, tags=["user"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users/create", tags=["user"])
async def user_create(_user_create: post_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=_user_create.username,
                full_name=_user_create.full_name,
                hashed_password=pwd_context.hash(_user_create.password1),
                email=_user_create.email, 
                disabled = False)
    db.add(db_user)
    db.commit()
    return {"Status":"ok", "data": "user created"}

@router.get("/users/me/", response_model=post_schema.User, tags=["user"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.get("/users/me/items/", tags=["user"])
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

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
def create_item(post: GetPost, db: Session = Depends(get_db)):
    q = Post(subject=post.subject, content=post.content, create_date=datetime.now())
    db.add(q)
    db.commit()
    return {"Status":"ok", "data": "item commited to DB"}

@router.get("/{id}/detail", response_model=post_schema.Post)
def question_detail(id: int, db: Session = Depends(get_db)):
    _question = db.query(Post).get(id)
    return _question

@router.put("/{id}/update", response_model=post_schema.Post)
def question_update(id: int, post: GetPost, db: Session = Depends(get_db)):
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