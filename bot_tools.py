from datetime import datetime

import db
import main


async def send_msg_2_user(user_id: int, msg: str):
    print("123")
    try:

        await main.bot.send_message(user_id, msg)
        print("Отправлено")
    except Exception as e:
        print(f"Failed to send notification to user {user_id}: {e}")


def send_deadline_to_user(user_id: int):
    now = datetime.now()
    if now.hour > 13:
        events = db.show_all_deadlines()
        for event in events:
            print(event)
            event_time = datetime.strptime(event[2], '%Y-%m-%d %H:%M:%S')
            time_difference = event_time - now
            days_left = time_difference.days
            hour_left = time_difference.seconds // 3600
            if 0 < days_left <= 7:
                print("log 7 days")
                send_msg_2_user(user_id, f"До конца {event[1]} осталось {days_left} дней."
                                         f" Закончится: {event[2]}. "
                                         f"Важно: {event[3]}.")
            if days_left == 0:
                print("log hours")
                send_msg_2_user(user_id, f"До конца {event[1]} осталось {hour_left} часов."
                                         f" Закончится: {event[2]}. "
                                         f"Важно: {event[3]}.")
