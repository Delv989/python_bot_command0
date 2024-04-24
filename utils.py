import re
from datetime import timezone, timedelta, datetime

from aiogram.fsm.state import State, StatesGroup

users_test = {}
tz = timezone(timedelta(hours=3), name='МСК')


def valid_id(id):
    return bool(re.fullmatch(r'^\d+$', id.strip()))


def valid_comment(comment):
    return valid_name(comment)


def valid_name(name):
    return bool(re.fullmatch(r'(\w+[,.:\s_-]*)+', name.strip()))


def convert_to_datetime(date):
    try:
        ret = datetime.strptime(date.strip(), '%d.%m.%Y %H.%M')
        ret = ret.replace(tzinfo=tz)
    except ValueError:
        ret = None
    return ret


def convert_deadlines_to_output(deadlines):
    deadlines = [(deadline.__str__() + '\n') for deadline in deadlines]
    out = "".join(deadlines)
    return out


def valid_date(date: datetime):
    return date - datetime.now(tz) > timedelta(seconds=1)


class Admin(StatesGroup):
    enter_new_admin_id = State()
    enter_deadline_date = State()
    enter_deadline_name = State()
    enter_deadline_comment = State()
    save_or_cancel = State()
    delete_deadline = State()
    enter_deadline_id = State()
