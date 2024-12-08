# join_handler.py
import logging

from consts import GroupTypes
from aiogram.types import ChatMemberUpdated
from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message
from bot.create_bot import database, bot, logger

join_router = Router()


@join_router.message(Command(commands=["hi_bot"]))
async def hi_bot_command(message: Message):
    group_id = message.chat.id
    if await database.is_group_id(group_id):
        await message.reply("Бот уже добавлен в базу данных для этой группы.")
    else:
        await database.add_group_id(group_id, GroupTypes.WHITE)
        await message.reply("Бот добавлен в группу и зарегистрирован в базе данных.")

@join_router.chat_member(F.new_chat_member.status.in_({"member", "administrator", "creator"}))
async def member_added_to_group(event: ChatMemberUpdated):
    group_id = event.chat.id
    user_id = event.new_chat_member.user.id
    await database.add_group_id(group_id, GroupTypes.WHITE)
    await bot.send_message(group_id, "Hi, friendo")
    try:
        await database.add_user_id(group_id, user_id)
    except Exception as e:
        logger.log(msg=f'error adding user: {e.args}', level=logging.ERROR)

