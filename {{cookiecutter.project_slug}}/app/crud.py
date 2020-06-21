"""CRUD utility functions."""

from app import schemas
from db import database

# by id
async def user_get(id: int) -> schemas.User:

    query = """
    SELECT * FROM users WHERE id = :id
    """

    user = await database.fetch_one(query=query, values={"id": id})

    return user


async def user_get_by_email():

    query = """
    """
    pass


async def user_get_level():

    query = """
    """
    pass


async def user_create():

    query = """
    """
    pass


async def user_update():

    query = """
    """
    pass


async def user_delete():

    query = """
    """
    pass


async def get_item():

    query = """
    """
    pass


async def item_create_with_owner():

    query = """
    """
    pass


async def item_get_by_city():

    query = """
    """
    pass


async def item_get_by_uuid():

    query = """
    """
    pass


async def item_get_by_owner():

    query = """
    """
    pass


async def item_update():

    query = """
    """
    pass


async def item_delete():

    query = """
    """
    pass
