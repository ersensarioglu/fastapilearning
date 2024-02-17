"""Fast api learning"""
from fastapi import FastAPI
from app.routers import auth, post, user
from app import models
from app.database import engine

models.Base.metadata.create_all(bind=engine) # Use of our db model

app = FastAPI() # Instance representing fastapi

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/") # Decorator links the function below to fastapi
              # and represents the path for GET request
async def root(): # use async for a long operation or you don't need to wait for response.
                  # Name doesnt matter but name it descriptive
    """Get root"""
    return {"message": "Welcome to my API"} # Python dictionary automatically converted to json
