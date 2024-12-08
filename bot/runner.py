# runner.py
import asyncio
from bot.create_bot import bot, dp_chat, database
from bot.handlers.group.ban_handler import ban_router
from bot.handlers.group.join_handler import join_router
from bot.handlers.dm.dm_handler import dm_router

async def main():
    # Initialize the database
    await database.initialize()

    # Include routers
    dp_chat.include_routers(ban_router, join_router, dm_router)

    # Start the bot
    await bot.delete_webhook(drop_pending_updates=True)
    await dp_chat.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())