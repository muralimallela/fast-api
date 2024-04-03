from fastapi import FastAPI,status,HTTPException,Response
from pydantic import BaseModel
import mysql.connector
import time


class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    
while True:
    try:
        conn = mysql.connector.connect(host = "localhost",user ="root",password = "",database="fastapi")
        cursor = conn.cursor(dictionary=True)
        print("Successfully connected to database")
        break
    except Exception as error:
        print("Failed to connect database")
        print("Error : ",error)
        time.sleep(2)
        
app = FastAPI()

@app.get("/")
def root():
    return {"messase" : "Please visit 'http:localhost/docs' for api documentation"}

@app.get("/posts",status_code=status.HTTP_200_OK)
def get_posts():
    cursor.execute("""select * from posts""")
    posts = cursor.fetchall()
    return {"data" : posts}

@app.get("/posts/{id}",status_code=status.HTTP_200_OK)
def get_post(id : int):
    cursor.execute("""select * from posts where id = %s""",(id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No record found with id {id}")
    return {"data": post}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post : Post):
    cursor.execute("""insert into posts(title,content,published) values(%s,%s,%s)""",(post.title,post.content,post.published))
    conn.commit()
    cursor.execute("""select * from posts where id = LAST_INSERT_ID()""")
    new_post = cursor.fetchone()
    return {"data":new_post}

@app.put("/posts/{id}",status_code=status.HTTP_201_CREATED)
def update_post(id : int, post : Post):
    cursor.execute("""select * from posts where id = %s""",(id,))
    old_post = cursor.fetchone()
    if not old_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No record found with id {id}")
    cursor.execute("""UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s""",(post.title,post.content,post.published,id))
    conn.commit()
    cursor.execute("""select * from posts where id = %s""",(id,))
    updated_post = cursor.fetchone()
    return {"data" : updated_post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    cursor.execute("""select * from posts where id = %s""",(id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No record found with id {id}")
    cursor.execute("""delete from posts where id = %s""",(id,))
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
