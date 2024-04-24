import re
from datetime import timezone, timedelta

from aiogram.fsm.state import State, StatesGroup

users_test = {}
tz = timezone(timedelta(hours=3), name='МСК')


def valid_id(id):
    return bool(re.match(r'^\d+$', id.strip()))


def valid_date(date):
    return True if date == 'true' else False;  # todo


def valid_comment(comment):
    return True if comment == 'true' else False;  # todo


def valid_name(name):
    return True if name == 'true' else False;  # todo


def convert_to_datetime(date):
    return date


class Admin(StatesGroup):
    enter_new_admin_id = State()
    enter_deadline_date = State()
    enter_deadline_name = State()
    enter_deadline_comment = State()
