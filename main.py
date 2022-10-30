from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from domain.post import post_router

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post_router.router)


# from fastapi import FastAPI, Path, Query, HTTPException, status, Request, Depends
# from fastapi.responses import HTMLResponse
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles
# from models import Post, Comment

# app = FastAPI()
# templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")

# db = {
#     1: {
#         "title": "제목1",
#         "content": "내용1"
#     },
#     2: {
#         "title": "제목2",
#         "content": "내용2"
#     },
#     3: {
#         "title": "제목3",
#         "content": "내용3"
#     }    
# }

# @app.get('/all')
# def index():
#     return db

# # combine path parameter  
# @app.get("/get_item/{item_id}")
# def get_item(item_id: int = Path(None, description="The ID of the inventory", ge=0)):
#     if item_id in db:
#         response = db[item_id]
#         return {"Status":"ok", "data": response}
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item name not found")
    

# # post
# @app.post("/create_item")
# def create_item(item_id: int, item: Post):
#     if item_id in db:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item ID already exists")
#     db[item_id] = item
#     return {"Status":"ok", "data": db[item_id]}

# # Put(update)
# @app.put("/update_item/{item_id}")
# def update_item(item_id: int, item: Post):
#     if item_id not in db:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID does not exist")

#     if item.title != None:
#         db[item_id].title = item.title
    
#     if item.content != None:
#         db[item_id].content = item.content
        
#     return {"Status":"ok", "data": db[item_id]}

# # delete
# @app.delete("/delete_item")
# def delete_item(item_id: int = Query(..., description="The ID of the item to delete",  ge=0)):
#     if item_id not in db:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item ID does not exist")
    
#     del db[item_id]
#     return {"Success": "Item deleted!"}

