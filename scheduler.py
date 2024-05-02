import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import db_async
import main
import schedule

import template_str


async def send_notification(message):
    people = await db_async.show_all_users()
    for person in people:
        try:
            await main.bot.send_message(int(person[0]), message)
        except Exception as e:
            print(f"Failed to send notification to user {person}: {e}")


async def schedule_send_message_every_day():
    now = datetime.now()
    # Список всех событий
    events = await db_async.show_all_deadlines()
    for event in events:
        event_time = event.date
        time_difference = event_time - now
        days_left = time_difference.days
        if 0 < days_left <= 7:
            await send_notification(template_str.create_long_time_info(event, days_left))


async def scheduler_task_every_day():
    schedule.every().day.at("13:00").do(asyncio.create_task, schedule_send_message_every_day())

    # Периодически проверяем расписание каждую минуту
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


async def schedule_send_message_every_6_hours():
    now = datetime.now()
    if 8 <= now.hour < 23:
        # Список всех событий
        events = await db_async.show_all_deadlines()
        for event in events:
            event_time = event.date
            time_difference = event_time - now
            days_left = time_difference.days
            hour_left = time_difference.seconds // 3600
            if days_left == 0:
                await send_notification(template_str.create_close_time_info(event, hour_left))


scheduler = AsyncIOScheduler()


async def scheduler_task_every_6_hours():
    scheduler.add_job(schedule_send_message_every_6_hours, 'cron', hour='*/3')
    scheduler.start()
