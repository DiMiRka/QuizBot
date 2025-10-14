from db import create_table


async def main():
    """Запуск бота"""
    await create_table()
    dp.include_routers(start_router, game_router, player_router, statistics_router)
    dp.startup.register(on_startup)
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())