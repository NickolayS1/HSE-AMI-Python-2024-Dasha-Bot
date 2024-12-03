
from aiogram import Bot, Dispatcher, html, F, Router
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from create_bot import database, bot
from aiogram.types.user import User
from aiogram.types import ChatMemberUpdated
from aiogram.utils import executor
from consts import UserTypes, DataBaseResponses, GroupTypes


black_white_list_router = Router()

async def check_user_to_ban(user_id: int, group_id: int) -> bool:
    if database.get_user_type(user_id, group_id) == UserTypes.IN_BLACKLIST:
        return True
    if database.get_type_of_group(group_id) == GroupTypes.WHITE and \
            database.get_user_type(user_id, group_id) != UserTypes.IN_WHITELIST:
        return True
    return False
    
     

@black_white_list_router.chat_member_handler()
async def handle_new_chat_member(event: ChatMemberUpdated):
    if event.new_chat_member.status == "member":
        user_id = event.new_chat_member.user.id
        group_id = event.chat.id
        if check_user_to_ban(user_id, group_id):
            bot.ban_chat_member()
        else:
            await bot.send_message(
                chat_id=group_id,
                text=f"Добро пожаловать, {event.new_chat_member.user.username}!"
            )

@black_white_list_router.message(Command(commands=["ban"]))
async def ban_user(message: Message, command: CommandObject):
    if database.get_user_type(message.from_user.id, message.chat.id) == UserTypes.MODERATOR:
        args = command.args
        if args is None:
            await message.reply(f"Вы не передали тег пользователя.")
            return
        ban_user_id = User(username=args)
        try:
            response = database.set_user_type(ban_user_id, message.chat.id, UserTypes.IN_BLACKLIST)
            if response == DataBaseResponses.SUCCESS:
                await message.reply(f"Пользователь {args} внесен в черный список.")
            else:
                await message.reply(f"Произошла ошибка.")
        except Exception:
            await message.reply(f"Произошла ошибка.")
    else:
        await message.reply(f"Вы не являетесь модератором.")


@black_white_list_router.message(Command(commands=["unban"]))
async def unban_user(message: Message, command: CommandObject):
    if database.get_user_type(message.from_user.id, message.chat.id) == UserTypes.MODERATOR:
        args = command.args
        if args is None:
            await message.reply(f"Вы не передали тег пользователя.")
            return
        unban_user_id = User(username=args)
        try:
            response = database.set_user_type(unban_user_id, message.chat.id, UserTypes.IN_WHITELIST)
            if response == DataBaseResponses.SUCCESS:
                await message.reply(f"Пользователь {args} убран из черного списка.")
            else:
                await message.reply(f"Произошла ошибка.")
        except Exception:
            await message.reply(f"Произошла ошибка.")
    else:
        await message.reply(f"Вы не являетесь модератором.")


@black_white_list_router.message(Command(commands=["moderator"]))
async def unban_user(message: Message, command: CommandObject):
    if database.get_user_type(message.from_user.id, message.chat.id) == UserTypes.MODERATOR:
        args = command.args
        if args is None:
            await message.reply(f"Вы не передали тег пользователя.")
            return
        unban_user_id = User(username=args)
        try:
            response = database.set_user_type(unban_user_id, message.chat.id, UserTypes.MODERATOR)
            if response == DataBaseResponses.SUCCESS:
                await message.reply(f"Пользователь {args} теперь модератор.")
            else:
                await message.reply(f"Произошла ошибка.")
        except Exception:
            await message.reply(f"Произошла ошибка.")
    else:
        await message.reply(f"Вы не являетесь модератором.")