import asyncio
from db import create_table
from create_bot import dp, bot
from handlers import router


async def main():
    """Запуск бота"""
    await create_table()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
