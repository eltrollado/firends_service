import asyncpg
from app.database import database


async def get_friends(user_id):
    results = await database.fetch_all(query=f'SElECT friend FROM friends WHERE "user" = :user_id', values={'user_id': user_id})
    friends = [r['friend'] for r in results]
    return friends


async def add_friend(user_id, friend_id):
    values = [
        {'user_id': user_id, 'friend_id': friend_id},
        {'user_id': friend_id, 'friend_id': user_id},
    ]
    try:
        await database.execute_many(query='INSERT INTO friends("user", friend) VALUES (:user_id, :friend_id)', values=values)
    except asyncpg.exceptions.UniqueViolationError:
        return None


async def remove_friend(user_id, friend_id):
    values = [
        {'user_id': user_id, 'friend_id': friend_id},
        {'user_id': friend_id, 'friend_id': user_id},
    ]
    await database.execute_many(query=f'DELETE FROM friends WHERE "user" = :user_id AND friend = :friend_id', values=values)