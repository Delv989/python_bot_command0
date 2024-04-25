import asyncio
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import db
import main
import schedule


async def send_notification(message):
    people = db.show_all_users()
    for person in people:
        try:
            await main.bot.send_message(int(person[0]), message)
        except Exception as e:
            print(f"Failed to send notification to user {person}: {e}")


async def schedule_send_message_every_day():
    now = datetime.now()
    # Список всех событий
    events = db.show_all_deadlines()
    for event in events:
        event_time = datetime.strptime(event[2], '%Y-%m-%d %H:%M:%S')
        time_difference = event_time - now
        days_left = time_difference.days
        if 0 < days_left <= 7:
            await send_notification(f"До конца {event[1]} осталось {days_left} дней."
                                    f" Закончится: {event[2]}. "
                                    f"Важно: {event[3]}.")


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
        events = db.show_all_deadlines()
        for event in events:
            event_time = datetime.strptime(event[2], '%Y-%m-%d %H:%M:%S')
            time_difference = event_time - now
            days_left = time_difference.days
            hour_left = time_difference.seconds // 3600
            if days_left == 0:
                await send_notification(f"До конца {event[1]} осталось {hour_left} часов."
                                        f" Закончится: {event[2]}. "
                                        f"Важно: {event[3]}.")


scheduler = AsyncIOScheduler()


async def scheduler_task_every_6_hours():
    scheduler.add_job(schedule_send_message_every_6_hours, 'cron', hour='*/6')
    scheduler.start()
