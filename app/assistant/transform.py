import re
from typing import Union

class Transform:
    """Для сокращения длинных команд при передаче через callback в кнопках tme"""

    cmd: str = None
    id: Union[str, int] = None
    user_id: Union[int] = None
    chat_id: Union[int] = None
    message_id: Union[int] = None
    value: Union[str, int] = None
    param: Union[str, int] = None
    text: str = None

    author_id: str = None
    from_id: Union[int] = None
    to_id: Union[int] = None

    file_id: Union[str, int] = None
    file_type: Union[str] = None

    date: Union[str, int] = None
    month: Union[str, int] = None
    day: Union[str, int] = None
    hour: Union[int] = None
    minutes: Union[int] = None

    type: Union[str, int] = None
    rate: Union[str, int] = None
    page: Union[int] = None
    stage: Union[str, int] = None

    def __init__(self, *args, **kwargs):

        self.__args = args
        self.__kwargs = kwargs
        self.__dict: dict = {}
        self.__get_cut_back()
        self.__set_var()

    def sort_input(self):
        new_dict = {}
        for _a in self.__args:
            if isinstance(_a, str):
                new_dict = new_dict | self.__str_to_dict(_a)
            elif isinstance(_a, dict):
                new_dict = new_dict | _a
        new_dict = new_dict | self.__kwargs
        return new_dict

    def __set_var(self):
        """Присвоить атрибутам входящие значения"""

        new_dict = self.sort_input()

        for i in new_dict:
            _key = i
            if i in self.__wrapp_dict:
                _value = new_dict[i]
            elif i in self.__un_wrapp_dict:
                _value = self.__un_wrapp_dict[i]
            else:
                continue

            self.__dict[_key] = _value
            self.__setattr__(_key, _value)

    def __str_to_dict(self, text: str) -> dict:
        """Преобразуем входную строку в словарь"""

        def check_type(value):
            pattern = {'None': None, 'False': False, 'True': True}
            try:
                value = int(value)
            except ValueError:
                if value in pattern:
                    value = pattern[value]
            return value

        result = re.findall(r"([a-z]+\d*)=([^=]+(?=/|$))", text)
        return {self.__un_wrapp_dict[i[0]]: check_type(i[1]) for i in result}

    @property
    def str(self):  # Для вывода подготовленной строки
        return "/".join([f"{self.__wrapp_dict[i]}={self.__dict[i]}" for i in self.__dict])

    @property
    def dict(self):  # Для вывода подготовленного словаря
        return self.__dict

    def __str__(self) -> str:
        return str(self.str)

    def __repr__(self) -> str:
        return str(self.str)

    def __getattr__(self, item):
        if item not in ["_NewTransform__dict"]:
            return self.__dict.get(item)

    def __setattr__(self, key, value):
        if key in Transform.__annotations__:
            self.__dict[key] = value
        self.__dict__[key] = value

    @classmethod
    def __get_cut_back(cls):
        """Создать словарь сокращений"""
        c_count = {}
        cls.__wrapp_dict = {}
        cls.__un_wrapp_dict = {}
        for attr in [i for i in cls.__annotations__]:  # Перебор атрибутов класса

            first_c = attr[0]
            if not c_count.get(first_c):

                c_count[first_c] = 0
            _key = f"{first_c}{c_count[first_c]}"

            cls.__un_wrapp_dict[_key] = attr
            cls.__wrapp_dict[attr] = _key
            c_count[first_c] += 1


if __name__ == '__main__':
    pass
