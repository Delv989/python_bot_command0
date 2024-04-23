import re

from aiogram.fsm.state import State, StatesGroup


def valid_id(id):
    return bool(re.match(r'^\d+$', id.strip()))


def valid_date(date):
    return date #todo




def valid_comment(comment):
    return comment   # todo

def valid_name(name):
    return name   # todo



class Admin(StatesGroup):
    enter_new_admin_id = State()
    enter_deadline_date = State()
    enter_deadline_name = State()
    enter_deadline_comment = State()
