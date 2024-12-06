# To test use cd database; python -m pytest

import os
import pytest
import aiosqlite
import pytest_asyncio

from consts import DataBaseResponses, GroupTypes, UserTypes
from data_handler import DataBase

TEST_DB_PATH = 'test_telegram_database.db'

@pytest_asyncio.fixture
async def db():
    database = DataBase(TEST_DB_PATH)
    try:
        os.remove(TEST_DB_PATH)
    except Exception:
        pass
    await database.initialize()
    yield database
    os.remove(TEST_DB_PATH)

@pytest.mark.asyncio
async def test_get_type_of_group(db):
    async with aiosqlite.connect(db.db_path) as conn:
        await conn.execute(
            "INSERT INTO Groups (group_id, group_type, max_group_warns) VALUES (?, ?, ?)",
            (42, GroupTypes.WHITE.value, 3))
        await conn.commit()
    res = await db.get_type_of_group(42)
    assert res == DataBaseResponses.SUCCESS


@pytest.mark.asyncio
async def test_set_type_of_group(db):
    group_id = 42
    group_type = GroupTypes.WHITE
    res = await db.set_type_of_group(group_id, group_type)
    assert res == DataBaseResponses.SUCCESS


@pytest.mark.asyncio
async def test_get_user_type(db):
    group_id = 42
    user_id = 101
    user_type = UserTypes.MODERATOR
    async with aiosqlite.connect(db.db_path) as conn:
        await conn.execute(
            "INSERT INTO Users (group_id, user_id, user_type) VALUES (?, ?, ?)",
            (group_id, user_id, user_type.value))
        await conn.commit()
    res = await db.get_user_type(user_id, group_id)
    assert res == user_type


@pytest.mark.asyncio
async def test_set_user_type(db):
    group_id = 42
    user_id = 101
    new_type = UserTypes.COMMON
    res = await db.set_user_type(user_id, group_id, new_type)
    assert res == DataBaseResponses.SUCCESS


@pytest.mark.asyncio
async def test_get_user_id_list(db):
    group_id = 42
    user_ids = [101, 102, 103]
    async with aiosqlite.connect(db.db_path) as conn:
        for user_id in user_ids:
            await conn.execute(
                "INSERT INTO Users (group_id, user_id, user_type) VALUES (?, ?, ?)",
                (group_id, user_id, str(UserTypes.COMMON)))
        await conn.commit()
    res = await db.get_user_id_list(group_id)
    assert sorted(res) == sorted(user_ids)


@pytest.mark.asyncio
async def test_get_amount_of_maximum_warns(db):
    group_id = 42
    max_warns = 5
    async with aiosqlite.connect(db.db_path) as conn:
        await conn.execute(
            "INSERT INTO Groups (group_id, max_group_warns) VALUES (?, ?)",
            (group_id, max_warns))
        await conn.commit()
    res = await db.get_amount_of_maximum_warns(group_id)
    assert res == max_warns


@pytest.mark.asyncio
async def test_set_amount_of_maximum_warns(db):
    group_id = 42
    max_warns = 7
    res = await db.set_amount_of_maximum_warns(group_id, max_warns)
    assert res == DataBaseResponses.SUCCESS


@pytest.mark.asyncio
async def test_get_amounts_of_warns(db):
    group_id = 42
    user_id = 101
    warns = 2
    async with aiosqlite.connect(db.db_path) as conn:
        await conn.execute(
            "INSERT INTO Users (group_id, user_id, user_warns) VALUES (?, ?, ?)",
            (group_id, user_id, warns))
        await conn.commit()
    res = await db.get_amounts_of_warns(user_id, group_id)
    assert res == warns


@pytest.mark.asyncio
async def test_get_groups_list(db):
    user_id = 101
    group_ids = [42, 43, 44]
    async with aiosqlite.connect(db.db_path) as conn:
        for group_id in group_ids:
            await conn.execute(
                "INSERT INTO Users (group_id, user_id, user_type) VALUES (?, ?, ?)",
                (group_id, user_id, str(UserTypes.COMMON)))
        await conn.commit()
    res = await db.get_groups_list(user_id)
    assert sorted(res) == sorted(group_ids)
