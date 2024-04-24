from datetime import datetime

import utils
from utils import valid_name
from utils import valid_comment


class Deadline:
    def __init__(self, name: str, comment: str, date: datetime):
        self._id = None
        self._name = None
        self._date = None
        self._comment = None
        self.name = name
        self.date = date
        self.comment = comment

    @staticmethod
    def from_dict(dict_):
        return Deadline(dict_['name'], dict_['comment'], dict_['date'])

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, id_: int):
        if not isinstance(id_, int):
            raise TypeError(f'Invalid type for the id argument: {type(id_)},'
                            f' required type: int')
        self._id = id_

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

    def __str__(self) -> str:
        return f'Дедлайн, id={self._id}, имя={self._name}, дата={self._date}, комментарий={self._comment}'


#
# d1 = Deadline('name1', 'comment1', datetime.now())
# d2 = Deadline('name2', 'comment2', datetime.now())
# d3 = Deadline('name3', 'comment3', datetime.now())
# lst = [d1, d2, d3]
# print(utils.convert_deadlines_to_output(lst))
