"""Fast api learning
Command to start app
uvicorn app.main:app --reload
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, post, user, vote
# from app import models
# from app.database import engine

# This is to create tables automatically
# But since we are using alembic, we don't need that
# models.Base.metadata.create_all(bind=engine)

app = FastAPI() # Instance representing fastapi

# We define allowed origins if it is cross site access
origins=["*"]
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/") # Decorator links the function below to fastapi
              # and represents the path for GET request
async def root(): # use async for a long operation or you don't need to wait for response.
                  # Name doesnt matter but name it descriptive
    """Get root"""
    return {"message": "Welcome to my API"} # Python dictionary automatically converted to json
