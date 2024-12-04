
from aiogram import Bot, Dispatcher, html, F, Router
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from bot.create_bot import database, bot
from aiogram.types.user import User
from aiogram.filters import ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated
from aiogram.types.chat_member_owner import ChatMemberOwner
from consts import UserTypes, DataBaseResponses, GroupTypes
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, JOIN_TRANSITION
from bot.create_bot import logger
from aiogram.enums import chat_member_status
import logging


ban_router = Router()


@ban_router.message(Command(commands=["ban"]))
async def ban_user(message: Message, command: CommandObject):
    if await database.get_user_type(message.from_user.id, message.chat.id) == UserTypes.MODERATOR:
        user_id = message.reply_to_message.from_user.id
        group_id = message.chat.id
        if isinstance(await bot.get_chat_member(group_id, user_id), ChatMemberOwner):
            try:
                await message.reply('Нос не дорос создателя банить.')
            except Exception as e:
                logger.log(msg=f'Owner ban attempt exception occured: {e.args}', level=logging.ERROR)
                await message.reply('Произошла ошибка при бане в чате.')
            return
        try:
            await bot.ban_chat_member(group_id, user_id)
            await database.set_user_type(user_id, group_id, UserTypes.IN_BLACKLIST)
            await message.reply('Пользователь забанен.')
        except Exception as e:
            logger.log(msg=f'Ban exception occured: {e.args}', level=logging.ERROR)
            await message.reply('Произошла ошибка при бане в чате.')
    else:
        await message.reply(f"Вы не являетесь модератором.")


@ban_router.message(Command(commands=["unban"]))
async def unban_user(message: Message, command: CommandObject):
    if await database.get_user_type(message.from_user.id, message.chat.id) == UserTypes.MODERATOR:
        user_id = message.reply_to_message.from_user.id
        group_id = message.chat.id
        try:
            await bot.unban_chat_member(group_id, user_id)
            await database.set_user_type(user_id, group_id, UserTypes.COMMON)
            await message.reply('Пользователь разбанен.')
        except Exception as e:
            logger.log(msg=f'Unan exception occured: {e.args}', level=logging.ERROR)
            await message.reply('Произошла ошибка при разбане в чате.')
    else:
        await message.reply(f"Вы не являетесь модератором.")

@ban_router.message(Command(commands=["admin"]))
async def unban_user(message: Message, command: CommandObject):
    user_id = message.from_user.id
    group_id = message.chat.id
    if isinstance(await bot.get_chat_member(group_id, user_id), ChatMemberOwner) and message.reply_to_message is None:
        try:
            await database.set_user_type(user_id, group_id, UserTypes.MODERATOR)
            await message.reply('Вы теперь модератор.')
        except Exception as e:
            logger.log(msg=f'Promotion exception occured: {e.args}', level=logging.DEBUG)
            await message.reply('Произошла ошибка при повышении пользователя.')
    elif isinstance(await bot.get_chat_member(group_id, user_id), ChatMemberOwner):
        try:
            await database.set_user_type(message.reply_to_message.from_user.id, group_id, UserTypes.MODERATOR)
            if message.reply_to_message.from_user.last_name is not None:
                name = message.reply_to_message.from_user.first_name + ' ' + message.reply_to_message.from_user.last_name
            else:
                name = message.reply_to_message.from_user.first_name
            await message.reply(f'{name} теперь модератор.')
        except Exception as e:
            logger.log(msg=f'Promotion exception occured: {e.args}', level=logging.DEBUG)
            await message.reply('Произошла ошибка при повышении пользователя.')


@ban_router.message(Command(commands=["white_list"]))
async def unban_user(message: Message, command: CommandObject):
    user_id = message.from_user.id
    group_id = message.chat.id
    if isinstance(await bot.get_chat_member(group_id, user_id), ChatMemberOwner):
        pass
    else:
        await message.reply(f"Вы не являетесь создателем.")
