from datetime import datetime
from utils import valid_name
from utils import valid_comment
from utils import convert_to_datetime


class Deadline:
    def __init__(self, name: str, comment: str, date: datetime):
        self._name = None
        self._date = None
        self._comment = None
        self.name = name
        self.date = date
        self.comment = comment

    @staticmethod
    def from_dict(dict):
        return Deadline(dict['name'], dict['comment'], dict['date'])

    @property
    def name(self) -> str:
        return self._name

    @property
    def comment(self) -> str:
        return self._comment

    @property
    def date(self) -> datetime:
        return self._date

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str):
            raise TypeError(f'Invalid type for the name argument: {type(name)},'
                            f' required type: str')
        if not valid_name(name):
            raise ValueError("Incorrect name")
        self._name = name

    @comment.setter
    def comment(self, comment: str):
        if not isinstance(comment, str):
            raise TypeError(f'Invalid type for the comment argument: {type(comment)},'
                            f' required type: str')
        if not valid_comment(comment):
            raise ValueError("Incorrect comment")
        self._comment = comment

    @date.setter
    def date(self, date: datetime):
        if not isinstance(date, datetime):
            raise TypeError(f'Invalid type for the date argument: {type(date)},'
                            f' required type: datetime')
        self._date = date
