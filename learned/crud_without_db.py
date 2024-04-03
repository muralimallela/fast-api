
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from typing import Optional
from random import randrange



app = FastAPI()




class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[int] = None
    
my_posts =[{"title" : "title1","content" : "content1","publised":"True","id":1} ,
           {"title" : "title2","content":"content2","publised":"False","id":2}]     



def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post

def find_post_index(id):
    for index , post in enumerate(my_posts):
        if post['id'] == id:
            return index
@app.get("/")
def root():
    return {"message":"Hello Wolrd!"}
@app.get("/posts")
def root():
    return {"data":my_posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post : Post):
    my_post = post.model_dump()
    my_post['id'] = randrange(0,1000)
    my_posts.append(my_post)
    return {"data" : my_post}

@app.get("/posts/{id}")
def get_post(id : int):
    post = find_post(id)
    return {"data" : post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    index = find_post_index(id)
    if index == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post of id {id} not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}",status_code=status.HTTP_201_CREATED)
def updata_post(id : int,post : Post):
    index = find_post_index(id)
    if index == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post of id {id} not found")
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data" : post_dict}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)