import asyncio
import os

from aiogram import Bot, Dispatcher

from birthday_today.run_background import run_continuously
from handlers.add_user import add_user_router
from handlers.replace_user import replace_user_router
from handlers.user import user_router
from db import creat_db


from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())


creat_db.sql_start()
run_continuously()

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

dp.include_routers(add_user_router, replace_user_router)
dp.include_router(user_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
