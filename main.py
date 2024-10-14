import asyncio
import os

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler


from birthday_today import search_function
from handlers.add_user import add_user_router
from handlers.replace_user import replace_user_router
from handlers.user import user_router
from db import creat_db


from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())


creat_db.sql_start()


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

dp.include_routers(add_user_router, replace_user_router)
dp.include_router(user_router)


async def main():
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(search_function.sending_message, trigger="cron", hour="10", minute="00", kwargs={"bot": bot})
    scheduler.add_job(search_function.checks_every_5_minutes, trigger="interval", seconds=300,
                      kwargs={"bot": bot})
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
