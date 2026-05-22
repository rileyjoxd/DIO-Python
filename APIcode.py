from contextlib import asynccontextmanager
from controllers import auth, post
from fastapi import FastAPI

from database import database, engine, metadata



@asynccontextmanager
async def lifespan(app:FastAPI):
    from models.post import posts
    await database.connect()
    metadata.create_all(engine)
    yield 
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
app.include_router(auth.router)
app.include_router(post.router)





# 45.176.145.6 - IP IXC