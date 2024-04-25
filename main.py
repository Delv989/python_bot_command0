import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config
import handler_user
import handler_admin
import handler_start
import scheduler
import db_async

memory = MemoryStorage()

bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)


async def main():
    dp = Dispatcher(storage=memory)
    await db_async.start_db()
    dp.include_routers(handler_user.router, handler_admin.router, handler_start.router)
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler.scheduler_task_every_day())
    loop.create_task(scheduler.scheduler_task_every_6_hours())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
