import asyncio
from aiogram.types import BotCommand, BotCommandScopeDefault
from db import create_table
from create_bot import dp, bot
from handlers import router


async def set_commands():
    """Настройка меню бота"""
    commands = [BotCommand(command='quiz', description='Начать викторину'),
                BotCommand(command='static', description='Статистика игроков')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def main():
    """Запуск бота"""
    await create_table()
    await set_commands()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
