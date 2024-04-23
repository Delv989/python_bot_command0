import re

from aiogram.fsm.state import State, StatesGroup


def valid_id(id):
    return bool(re.match(r'^\d+$', id.strip()))


class Admin(StatesGroup):
    enter_new_admin_id = State()
    enter_deadline_message = State()
    enter_deadline_date = State()
