from datetime import UTC, datetime

from fastapi import FastAPI, status, Response, Cookie, Header, APIRouter
from typing import Annotated

from schemas.post import PostIn
from views.post import PostOut

router = APIRouter(prefix="/posts")

fake_db = [
    {"title": "Criando uma aplicação com Django", "date": datetime.now(UTC), "published": True},
    {"title": "Criando uma aplicação com FastAPI", "date": datetime.now(UTC), "published": True},
    {"title": "Criando uma aplicação com Flask", "date": datetime.now(UTC), "published": True},
    {"title": "Criando uma aplicação com Starlett", "date": datetime.now(UTC), "published": True},
]

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostOut)
def create_post(post: PostIn):
    fake_db.append(post.model_dump())
    return post

@router.get("/", response_model=list[PostOut])
def read_posts(
    response: Response,
    published: bool,
    limit: int,
    skip: int = 0,
    ads_id: Annotated[str | None, Cookie()] = None,
    user_agent: Annotated[str | None, Header()] = None,
    ):
    response.set_cookie(key="user", value="bviana1529@gmail.com")
    print(f"Cookie: {ads_id}")
    print(f"User-agent: {user_agent}")
#def read_posts(published: bool, skip: int = 0, limit: int = len(fake_db)):
    return [post for post in fake_db[skip : skip + limit] if post['published'] is published]
    #posts = []
    #for post in fake_db:
    #    if len(posts) == limit:
    #        break
    #    if post["published"] is published:
    #        posts.append(post)
    
    #return posts

@router.get("/{framework}", response_model=PostOut)
def read_framework_posts(framework: str):
    return {
        "posts": [
            {"title": "Criando uma aplicação com {framework}", "date": datetime.now(UTC)},
            {"title": "Criando uma aplicação com {framework}", "date": datetime.now(UTC)},
        ]
    }
    
