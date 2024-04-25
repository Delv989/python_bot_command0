import re
from datetime import timezone, timedelta, datetime
from aiogram.fsm.state import State, StatesGroup

tz = timezone(timedelta(hours=3), name='МСК')


def valid_id(id_):
    return bool(re.fullmatch(r'^\d+$', id_.strip()))


def valid_comment(comment):
    return valid_name(comment)


def valid_name(name):
    return bool(re.fullmatch(r'([a-zA-Zа-яА-Я]+[,.:\s\d_-]*)+', name.strip()))


def convert_to_datetime(date):
    try:
        ret = datetime.strptime(date.strip(), '%d.%m.%Y %H.%M')
        ret = ret.replace(tzinfo=tz)
    except ValueError:
        ret = None
    return ret


def convert_deadlines_to_output(deadlines):
    deadlines = [(deadline.__str__() + '\n') for deadline in deadlines if deadline is not None]
    out = "".join(deadlines)
    if len(out) == 0:
        out = "На данный момент дедлайнов нет"
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
