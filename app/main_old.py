"""Fast api learning"""
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

# from typing import Optional

app = FastAPI() # Instance representing fastapi

class Post(BaseModel):
    """Any named class that will represent schema for a post"""
    title: str
    content: str
    published: bool = True
#    rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host='localhost',
                                database='fastapi',
                                user='fastapi',
                                password='fastapi',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

my_posts = [{"title": "title of post 1",
             "content": "content of post 1",
             "id": 1},
             {"title": "title of post 2",
              "content": "content of post 2",
              "id": 2}]

def find_post(my_id):
    """Search with id"""
    for p in my_posts:
        if p["id"] == my_id:
            return p
    return None

def last_id():
    """Find the last id"""
    latest_id = 0
    for p in my_posts:
        if p["id"] > latest_id:
            latest_id = p["id"]
    return latest_id

def find_index_post(my_id):
    """Find index position of id"""
    for i, p in enumerate(my_posts):
        if p["id"] == my_id:
            return i
    return None

@app.get("/") # Decorator links the function below to fastapi
              # and represents the path for GET request
async def root(): # use async for a long operation or you don't need to wait for response.
                  # Name doesnt matter but name it descriptive
    """Get root"""
    return {"message": "Welcome to my API"} # Python dictionary automatically converted to json

@app.get("/posts") # So using /posts in the url points to below function
def get_posts():
    """Get all posts"""
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
#    return {"data": my_posts}
    return {"data": posts}

@app.get("/posts/latest")  # this decorator should be positioned above the below decorator
                           # to be able to get priority, as it works with first match
def latest_post():
    """Get latest post"""
    return {"data": my_posts[len(my_posts) - 1]}

@app.get("/posts/{my_id}") # matches to a url where given value in the root is mapped to id variable
# def get_post(id: int, response: Response):
def get_post(my_id: int): # that id from decorator is passed as input parameter to function
                       # also validates if it is integer, otherwise throws error to user
    """Get a given post by id"""
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(my_id)))
    post = cursor.fetchone()
    # post = find_post(int(my_id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {my_id} was not found")
#        response.status_code = status.HTTP_404_NOT_FOUND
#        return {"message": f"Post with id: {id} was not found"}
    return {"data": post}

@app.post("/createposts")
def create_posts(payload: dict = Body(...)): # Gets everything from body of the message
                  # and turns it into python dictionary and assigns to variable payload
    """Upload posts"""
    return {"new_posts": f"title: {payload['title']}, content: {payload['content']}"}

@app.post("/createpost")
def createpost(new_post: Post): # Body will be validated against given pydantic basemodel class
                                # and then be assigned to variable defined here
    """Create a new post"""
    print(new_post) # See the format of basemodel
    print(new_post.model_dump()) # Turn it into a python dictionary
    return {"new_post":
        f"title: {new_post.title}, content: {new_post.content}, published: {new_post.published}"}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    """Create a new post"""
#    post_dict = post.model_dump()
#    post_dict['id'] = last_id() + 1
#    my_posts.append(post_dict)
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
        (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.delete("/posts/{my_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(my_id: int):
    """Delete a post"""
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(my_id),))
    deleted_post = cursor.fetchone()
    conn.commit()

#    index = find_index_post(my_id)
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {my_id} was not found")
#    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{my_id}")
def update_post(my_id: int, post: Post):
    """Update a post"""
    cursor.execute(
        """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s  RETURNING * """,
        (post.title, post.content, post.published, str(my_id)))
    updated_post = cursor.fetchone()
    conn.commit()
#    index = find_index_post(my_id)
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {my_id} was not found")
#    post_dict = post.model_dump()
#    post_dict['id'] = my_id
#    my_posts[index] = post_dict
    return {"data": updated_post}
