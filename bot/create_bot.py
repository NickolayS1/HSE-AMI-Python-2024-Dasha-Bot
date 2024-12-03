import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from decouple import config
from database.data_handler import DataBase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s -%(levelname)s - %(message)s')
logger = logging.getLogger("logs")

database = DataBase()
bot = Bot(token=config('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp_chat = Dispatcher(storage=MemoryStorage())