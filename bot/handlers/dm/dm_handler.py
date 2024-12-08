# dm_handler.py
import logging

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message
from bot.create_bot import database, bot, logger
from consts import UserTypes, DataBaseResponses
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


dm_router = Router()

class ModerationStates(StatesGroup):
    waiting_for_group_id = State()
    waiting_for_user_ids_to_add = State()
    waiting_for_user_ids_to_delete = State()
    waiting_for_confirmation = State()
    group_id_state = 0

@dm_router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await message.reply("Привет! Пожалуйста, введите group_id, который вы хотите модерировать.")
    await state.set_state(ModerationStates.waiting_for_group_id)

@dm_router.message(F.text, ModerationStates.waiting_for_group_id)
async def process_group_id(message: Message, state: FSMContext):
    try:
        group_id = int(message.text)
        user_type = await database.get_user_type(message.from_user.id, group_id)
        if user_type == UserTypes.MODERATOR:
            await message.reply(f"Вы являетесь модератором группы {group_id}. Теперь вы можете использовать следующие команды:\n/add_to_whitelist\n/delete_from_whitelist\n/ban_not_in_whitelist\n/help")
            ModerationStates.group_id_state = group_id
            print(ModerationStates.group_id_state)
            await state.set_state(None)
        else:
            await message.reply("Вы не являетесь модератором этой группы.")
            await state.set_state(None)
    except ValueError:
        await message.reply("Пожалуйста, введите корректный group_id.")

@dm_router.message(Command(commands=["add_to_whitelist"]))
async def cmd_add_to_whitelist(message: Message, state: FSMContext):
    await message.reply("Отправьте user_id пользователей, которых хотите добавить в белый список, разделенных символом новой строки.")
    await state.set_state(ModerationStates.waiting_for_user_ids_to_add)

@dm_router.message(F.text, ModerationStates.waiting_for_user_ids_to_add)
async def process_user_ids_to_add(message: Message, state: FSMContext):
    user_ids = message.text.strip().split('\n')
    group_id = ModerationStates.group_id_state
    for user_id in user_ids:
        try:
            user_id = int(user_id)
            if await database.get_user_type(group_id, user_id) == UserTypes.IN_WHITELIST:
                await message.reply(f"Пользователь {user_id} уже находится в белом списке.")
            else:
                await database.set_user_type(user_id, group_id, UserTypes.IN_WHITELIST)
                await message.reply(f"Пользователь {user_id} добавлен в белый список.")
        except ValueError:
            await message.reply(f"Некорректный user_id: {user_id}. Пропускаем.")
    await state.set_state(None)

@dm_router.message(Command(commands=["delete_from_whitelist"]))
async def cmd_delete_from_whitelist(message: Message, state: FSMContext):
    await message.reply("Отправьте user_id пользователей, которых хотите удалить из белого списка, разделенных символом новой строки.")
    await state.set_state(ModerationStates.waiting_for_user_ids_to_delete)

@dm_router.message(F.text, ModerationStates.waiting_for_user_ids_to_delete)
async def process_user_ids_to_delete(message: Message, state: FSMContext):
    user_ids = message.text.strip().split('\n')
    group_id = ModerationStates.group_id_state
    for user_id in user_ids:
        try:
            user_id = int(user_id)
            if await database.get_user_type(user_id, group_id) == UserTypes.IN_WHITELIST:

                await database.set_user_type(user_id, group_id, UserTypes.COMMON)
                await message.reply(f"Пользователь {user_id} удален из белого списка.")
            else:
                await message.reply(f"Пользователь {user_id} не находится в белом списке.")
        except ValueError:
            await message.reply(f"Некорректный user_id: {user_id}. Пропускаем.")
    await state.set_state(None)

@dm_router.message(Command(commands=["back"]))
async def cmd_back(message: Message, state: FSMContext):
    await message.reply("Возвращаемся к основным командам.")
    await state.set_state(None)

@dm_router.message(Command(commands=["ban_not_in_whitelist"]))
async def cmd_ban_not_in_whitelist(message: Message, state: FSMContext):
    await message.reply("Вы уверены, что хотите забанить всех пользователей, не находящихся в белом списке? (yes/no)")
    await state.set_state(ModerationStates.waiting_for_confirmation)

@dm_router.message(F.text, ModerationStates.waiting_for_confirmation)
async def process_confirmation(message: Message, state: FSMContext):
    confirmation = message.text.strip().lower()
    if confirmation == "yes":
        await message.reply("Забанил всех пользователей, не находящихся в белом списке.")
        group_id = ModerationStates.group_id_state
        await ban_not_in_whitelist(bot, group_id, database)
    elif confirmation == "no":
        await message.reply("Операция отменена.")
    else:
        await message.reply("Пожалуйста, ответьте 'yes' или 'no'.")
    await state.set_state(None)

@dm_router.message(Command(commands=["help"]))
async def cmd_help(message: Message):
    help_text = (
        "/start - Приветствие и запрос group_id для модерации.\n"
        "/add_to_whitelist - Добавить пользователей в белый список.\n"
        "/delete_from_whitelist - Удалить пользователей из белого списка.\n"
        "/ban_not_in_whitelist - Забанить всех пользователей, не находящихся в белом списке.\n"
        "/back - Вернуться к основным командам.\n"
        "/help - Показать это сообщение."
    )
    await message.reply(help_text)

async def ban_not_in_whitelist(bot: Bot, group_id: int, database):
    # Get all members in the group
    members = await database.get_user_id_list(group_id)
    for user_id in members:
        if await database.get_user_type(user_id, group_id) not in {UserTypes.IN_WHITELIST, UserTypes.MODERATOR}:
            try:
                await bot.ban_chat_member(group_id, user_id)
                print()
                logger.log(msg=f"User {user_id} banned from group {group_id}")
            except Exception as e:
                logger.log(msg=f'Failed to ban user {user_id}: {e.args}', level=logging.ERROR)