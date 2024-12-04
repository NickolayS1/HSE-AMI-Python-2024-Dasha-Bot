import asyncio
from bot.create_bot import bot, dp_chat, database
from bot.handlers.group.ban_handler import ban_router


async def main():
    dp_chat.include_routers(ban_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp_chat.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())