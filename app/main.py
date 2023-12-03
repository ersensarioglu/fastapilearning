from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI() # Instance representing fastapi

class Post(BaseModel): # Any named class that will represent schema for a post
    title: str
    content: str
    published: bool = True
#    rating: Optional[int] = None


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {"title": "title of post 2", "content": "content of post 2", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
    return None

def last_id():
    last_id = 0
    for p in my_posts:
        if p["id"] > last_id:
            last_id = p["id"]
    return last_id

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i   
    return None 

@app.get("/") # Decorator links the function below to fastapi and represents the path for GET request
async def root(): # use async for a long operation or you don't need to wait for response. Name doesnt matter but name it descriptive
    return {"message": "Welcome to my API"} # Python dictionary automatically converted to json

@app.get("/posts") # So using /posts in the url points to below function
def get_posts():
    return {"data": my_posts}

@app.get("/posts/latest")  # this decorator should be positioned above the below decorator to be able to get priority, as it works with first match
def latest_post():
    return {"data": my_posts[len(my_posts) - 1]}

@app.get("/posts/{id}") # matches to a url where given value in the root is mapped to id variable
# def get_post(id: int, response: Response):
def get_post(id: int): # that id from decorator is passed as input parameter to function also validates if it is integer, otherwise throws error to user
    post = find_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
#        response.status_code = status.HTTP_404_NOT_FOUND
#        return {"message": f"Post with id: {id} was not found"}
    return {"data": post}

@app.post("/createposts")
def create_posts(payload: dict = Body(...)): # Get everything from body of the message and turns it into python dictionary and assigns to variable payload
    return {"new_posts": f"title: {payload['title']}, content: {payload['content']}"}

@app.post("/createpost")
def create_posts(new_post: Post): # Body will be validated against given pydantic basemodel class and then be assigned to variable defined here
    print(new_post) # See the format of basemodel
    print(new_post.model_dump()) # Turn it into a python dictionary
    return {"new_post": f"title: {new_post.title}, content: {new_post.content}, published: {new_post.published}"}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = last_id() + 1
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}