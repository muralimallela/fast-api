
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import mysql.connector
import time

app = FastAPI()

while True:
    try:
        conn =  mysql.connector.connect(host="localhost",user='root',password='',database='fastapi')
        print("Successfully connected to database")
        cursor = conn.cursor(dictionary=True)
        break
    except Exception as error:
        print("Connection failed to database")
        print("Error : ",error)
        time.sleep(2)

class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    
@app.get("/")
def root():
    return {"message":"Hello Wolrd!"}
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * from posts""")
    posts = cursor.fetchall()
    return {"data":posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post : Post):
    cursor.execute("""INSERT INTO posts (title,content,published) values (%s,%s,%s)""",(post.title,post.content,post.published))
    conn.commit();
    cursor.execute("""SELECT * FROM posts WHERE id = LAST_INSERT_ID()""")
    new_post = cursor.fetchone()
    print(cursor)
    return {"data" : new_post}

@app.get("/posts/{id}")
def get_post(id : int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post of id {id} is not found")
    return {"data" : post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post of id {id} is not found")
    cursor.execute("""DELETE FROM posts WHERE id = %s""",(id,))
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}",status_code=status.HTTP_201_CREATED)
def updata_post(id : int,post : Post):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,))
    old_post = cursor.fetchone()
    if not old_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post of id {id} is not found")
    cursor.execute("""UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s""",(post.title,post.content,post.published,id))
    conn.commit()
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(id,))
    new_post = cursor.fetchone()
    
    return {"data" : new_post}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)