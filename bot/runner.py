import asyncio
from create_bot import bot, dp, database
from handlers.group.black_white_list_handler import black_white_list_router


async def main():
    dp.include_routers(black_white_list_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())