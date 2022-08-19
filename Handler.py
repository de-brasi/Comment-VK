import DataStorage
import GUI
import utils
from DataStorage import Data
from tkinter import IntVar
from enum import Enum


class Mode:
    """
    Only nwo mods are valid - delete and add
    """
    __slots__ = ("mode", "available")

    def __init__(self, mode: str) -> None:
        self.available = ("delete", "add")
        assert mode in self.available
        self.mode = mode

    def get_mode(self) -> str:
        return self.mode

    def set_mode(self, mode: str) -> None:
        assert mode in self.available
        self.mode = mode


class Handler:
    """
    Получает user interface,
    получает данные для обработки,
    обрабатывает данные через core-функцию
    и дает обратную связь в user interface.
    """
    def __init__(self):
        pass

    def core(self, user_interface: GUI.Interface):
        collected_data = user_interface.data
        users = utils.get_users_access_info()

    def get_photo_id(self, url: str):
        # TODO: основная работа по валидации должна быть перенесена в validator
        # TODO: Тут же нужно просто брать какой то определенный токен и возвращать его
        """
        Get id of photo from link.
        Assert that the link has the correct structure.
        Parsing link on photo id and owner id is requirement of VK API
        :param url
        :return: None or int
        """
        url = self.split_link(url)
        photo_info = url[4].split('_')
        photo_info = photo_info[-1]
        return int(photo_info)

    def get_owner_id(self, url: str):
        """
        Get id of photo`s owner from link.
        Assert that the link has the correct structure.
        Parsing link on photo id and owner id is requirement of VK API.
        According to VK API id of club is negative integer.
        :param url:
        :return:
        """
        url = self.split_link(url)
        owner_info = url[3]
        if owner_info.startswith('club'):
            return int(owner_info[len('club'):]) * -1
        elif owner_info.startswith('id'):
            return int(owner_info[len('id'):])
        else:
            raise ValueError("Unexpected owner type")

    def validate_url(self, url: str) -> bool:
        if bool(url):
            return bool(url)
        else:
            raise ValueError("invalid link")

    def delete_photo(self, owner: int, photo: int,
                     data_storage: Data, photo_counter: IntVar):
        if data_storage.check_availability(owner, photo):
            if data_storage.delete(owner, photo):
                photo_counter.set(
                    photo_counter.get() - 1
                )
        else:
            # TODO: show information message that not exist
            pass

    def add_photo(self, owner: int, photo: int,
                  data_storage: Data, photo_counter: IntVar):
        if data_storage.check_availability(owner, photo):
            # TODO: show information message that already exist
            pass
        else:
            if data_storage.add(owner, photo):
                photo_counter.set(
                    photo_counter.get() + 1
                )

    def split_link(self, url):
        splitting_symbols = ['/', '?z=', '%2F']  # словарь символов для разбиения адреса фото
        for x in splitting_symbols:  # разбиение строки по разделительным символам - костыль регулярных выражений
            url = url.replace(x, '/')
        url = url.split('/')
        return url
