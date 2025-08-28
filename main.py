from fastapi import FastAPI, Response, status, HTTPException 
from fastapi.params import Body
from typing import Optional
from pydantic import BaseModel
from random import randrange 


app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool=True
    rating: Optional[int]= None
    
    
class updatePost():
    title: str
    content: str
    published: bool=True
    rating: Optional[int]= None
    
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
              {"title": "favorite foods", "content": "I like pizza", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id']==id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id']==id:
            return i
        
@app.get("/")
async def root():
    return { "message":" hello world"}

@app.get("/posts")
def get_posts():
    return{ "data": my_posts}

@app.post("/posts")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"new post": f"title {payload['title']} content:{payload['content']}"}

@app.get("/posts/{id}")
def get_post(id:int):
    
    posts=find_post(id)
    if not posts:
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return{"post_detail":posts}

@app.delete("/posts/{id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting posts
    # find the index in the array that has required id
    # my_post.pop(index)
    index= find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post:Post):

    index= find_index_post(id)
    
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_dict=post.dict()
    post_dict["id"]=id
    my_posts[index]=post_dict
    return {"data":post_dict}