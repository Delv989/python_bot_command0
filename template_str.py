from deadline import Deadline


def create_close_time_info(deadline: Deadline, hour_left) -> str:
    return (f"До конца {deadline.name} осталось {hour_left} часов."
            f"Закончится: {deadline.date}. "
            f"Важно: {deadline.comment}.")


def create_long_time_info(deadline: Deadline, days_left) -> str:
    return (f"До конца {deadline.name} осталось {days_left} дней."
            f" Закончится: {deadline.date}. "
            f"Важно: {deadline.comment}.")
