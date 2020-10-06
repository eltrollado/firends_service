
from typing import List

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import logging

from app import repository
from app.cache import cache
from app.database import database


logger = logging.getLogger(__name__)


class Friends(BaseModel):
    friends: List[int]


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()
    await cache.connect()
    logger.info('Friend service started')


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    await cache.disconnect()


@app.post("/users/{user_id}/friends/{friend_id}", status_code=201)
async def add_friend(user_id: int, friend_id: int):
    await repository.add_friend(user_id, friend_id)
    await cache.delete(f'user:{user_id}')
    await cache.delete(f'user:{friend_id}')


@app.delete("/users/{user_id}/friends/{friend_id}", status_code=200)
async def remove_friend(user_id: int, friend_id: int):
    await repository.remove_friend(user_id, friend_id)
    await cache.delete(f'user:{user_id}')
    await cache.delete(f'user:{friend_id}')


@app.get("/users/{user_id}/friends")
async def get_friends(user_id: int):
    key = f'user:{user_id}'

    friends = await cache.cached_set(
        key,
        repository.get_friends(user_id),
        int
    )

    return Friends(friends=friends)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
