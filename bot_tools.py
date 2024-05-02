from datetime import datetime

import db_async
import main
import template_str
from deadline import Deadline


async def send_msg_2_user(user_id: int, msg: str):
    try:
        await main.bot.send_message(user_id, msg)
    except Exception as e:
        print(f"Failed to send notification to user {user_id}: {e}")


async def send_deadline_to_users(user_id: int):
    now = datetime.now()
    if now.hour >= 13:
        events = await db_async.show_all_deadlines()
        for event in events:
            event_time = event.date
            time_difference = event_time - now
            days_left = time_difference.days
            hour_left = time_difference.seconds // 3600
            if 0 < days_left <= 7:
                await send_msg_2_user(user_id, template_str.create_long_time_info(event, days_left))
            if days_left == 0:
                await send_msg_2_user(user_id, template_str.create_close_time_info(event, hour_left))


async def send_new_deadline(deadline: Deadline):
    now = datetime.now()
    people = await db_async.show_all_users()
    time_difference = deadline.date - now
    days_left = time_difference.days
    hour_left = time_difference.seconds // 3600
    if 0 < (deadline.date - now).days <= 7:
        for person in people:
            await send_msg_2_user(int(person[0]), template_str.create_long_time_info(deadline, days_left))
    elif (deadline.date - now).days == 0:
        for person in people:
            await send_msg_2_user(int(person[0]), template_str.create_close_time_info(deadline, hour_left))
