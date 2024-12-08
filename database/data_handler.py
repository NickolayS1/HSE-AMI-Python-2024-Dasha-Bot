from consts import DataBaseResponses
from consts import GroupTypes
from consts import UserTypes
import aiosqlite
import os

class DataBase:
    def __init__(self, db_path='telegram_database.db'):
        self.db_path = db_path

    async def initialize(self) -> DataBaseResponses:
        return await self.create_database()

    async def create_database(self) -> DataBaseResponses:
        if not os.path.exists(self.db_path):
            async with aiosqlite.connect(self.db_path) as conn:
                cursor = await conn.cursor()
                await cursor.execute('''
                    CREATE TABLE Groups (
                        group_id INTEGER PRIMARY KEY,
                        group_type TEXT,
                        max_group_warns INTEGER
                    )
                ''')
                await cursor.execute('''
                    CREATE TABLE Users (
                        group_id INTEGER,
                        user_id INTEGER,
                        user_type TEXT,
                        user_warns INTEGER,
                        PRIMARY KEY (group_id, user_id),
                        FOREIGN KEY (group_id) REFERENCES Groups(group_id)
                    )
                ''')
                await conn.commit()
        return DataBaseResponses.SUCCESS

    async def add_user_id(self, group_id: int, user_id: int) -> DataBaseResponses:
        """
        Adds a user to the All_Users table
        """
        async with aiosqlite.connect(self.db_path) as conn:
            await conn.execute("INSERT OR REPLACE INTO Users (group_id, user_id, user_type, user_warns) VALUES (?, ?, ?, ?)",
                               (group_id, user_id, UserTypes.COMMON.value, 0))
            await conn.commit()
            return DataBaseResponses.SUCCESS

    async def get_type_of_group(self, group_id: int) -> DataBaseResponses:
        """
        Gets the type of the group via group_id
        """
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.execute("SELECT group_type FROM Groups WHERE group_id=?", (group_id,))
            result = await cursor.fetchone()
            return DataBaseResponses.SUCCESS if result else DataBaseResponses.ERROR

    async def set_type_of_group(self, group_id: int, group_type: GroupTypes) -> DataBaseResponses:
        """
        Sets new type of the group via group_id
        """
        async with aiosqlite.connect(self.db_path) as conn:
            await conn.execute("INSERT OR REPLACE INTO Groups (group_id, group_type) VALUES (?, ?)",
                               (group_id, group_type.value))
            await conn.commit()
            return DataBaseResponses.SUCCESS

    async def get_user_type(self, user_id: int, group_id: int) -> UserTypes:
        """
        Gets user type in a specified group via user_id and group_id
        """
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.execute("SELECT user_type FROM Users WHERE user_id=? AND group_id=?",
                                        (user_id, group_id))
            result = await cursor.fetchone()
            return UserTypes(result[0]) if result else None

    async def set_user_type(self, user_id: int, group_id: int, new_type: UserTypes) -> DataBaseResponses:
        """
        Sets new user type in a specified group via user_id and group_id
        """
        async with aiosqlite.connect(self.db_path) as conn:
            await conn.execute("INSERT OR REPLACE INTO Users (user_id, group_id, user_type) VALUES (?, ?, ?)",
                               (user_id, group_id, new_type.value))
            await conn.commit()
            return DataBaseResponses.SUCCESS

    async def get_user_id_list(self, group_id: int) -> list[int]:
        """
        Gets user_id list from the specified group via group_id
        """
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.execute("SELECT user_id FROM Users WHERE group_id=?", (group_id,))
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

    async def get_amount_of_maximum_warns(self, group_id: int) -> int:
        """
        Gets the maximum number of warns before users get banned
        """
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.execute("SELECT max_group_warns FROM Groups WHERE group_id=?", (group_id,))
            result = await cursor.fetchone()
            return result[0] if result else None

    async def set_amount_of_maximum_warns(self, group_id: int, max_warns: int) -> DataBaseResponses:
        """
        Sets the maximum number of warns before users get banned
        """
        async with aiosqlite.connect(self.db_path) as conn:
            await conn.execute("INSERT OR REPLACE INTO Groups (group_id, max_group_warns) VALUES (?, ?)",
                               (group_id, max_warns))
            await conn.commit()
            return DataBaseResponses.SUCCESS

    async def get_amounts_of_warns(self, user_id: int, group_id: int) -> int:
        """
        Gets the number of warns of the specified user via user_id and group_id
        """
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.execute("SELECT user_warns FROM Users WHERE user_id=? AND group_id=?",
                                        (user_id, group_id))
            result = await cursor.fetchone()
            return result[0] if result else None

    async def get_groups_list(self, user_id: int) -> list[int]:
        """
        Gets the list of [group_id] for groups where user exists
        """
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.execute("SELECT group_id FROM Users WHERE user_id=?", (user_id,))
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

    async def add_group_id(self, group_id: int, group_type: GroupTypes, max_group_warns: int = 3) -> DataBaseResponses:
        """
        Adds a new group to the database
        """
        async with aiosqlite.connect(self.db_path) as conn:
            await conn.execute("INSERT OR REPLACE INTO Groups (group_id, group_type, max_group_warns) VALUES (?, ?, ?)",
                               (group_id, group_type.value, max_group_warns))
            await conn.commit()
            return DataBaseResponses.SUCCESS

    async def is_group_id(self, group_id: int) -> bool:
        """
        Checks if the group ID is already present in the Groups table
        """
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.execute("SELECT 1 FROM Groups WHERE group_id=?", (group_id,))
            result = await cursor.fetchone()
            return result is not None

    async def is_user_id(self, group_id: int, user_id: int) -> bool:
        """
        Checks if the user ID is already present in the Users table for the given group ID
        """
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.execute("SELECT 1 FROM Users WHERE group_id=? AND user_id=?", (group_id, user_id))
            result = await cursor.fetchone()
            return result is not None
