import asyncio
from db import create_table
from create_bot import dp, bot


async def main():
    """Запуск бота"""
    await create_table()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
