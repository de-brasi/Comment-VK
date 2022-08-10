import datetime
import io
import tkinter.scrolledtext

import variables
from tkinter import constants as tk_constants


def actual_time():
    return datetime.datetime.now()


def get_owners_id(log_file:        io.TextIOWrapper,
                  gui_destination: tkinter.scrolledtext.ScrolledText,
                  link:            str) -> int:
    """
    Getting the owner id of a photo from links to it on an album.
    If owner is club or community return negative value
    :return owner_id
    :return 0 if exception was caught

    get_owners_id('https://vk.com/club1//photo-1_2/Falbum-3_4') -> -1
    get_owners_id('https://vk.com/id1?z=photo1_2%2Fphotos1') -> 1
    """
    invalid_link_user_msg = 'Структура ссылки на изображение не соответствует ожиданию программы!'
    invalid_link_log_msg = f'-> В ссылке {link} не удалось найти подстроку, начинающуюся с "photo",' \
                           f' ссылка не валидна или проблемы в функции {__name__}'
    invalid_id_representation_log_msg = f'-> В ссылке {link} удалось найти подстроку, начинающуюся с "photo",' \
                                        f' но не удалось выделить owner_id которое должно быть int,' \
                                        f' проблемы в функции {__name__}'

    symbols_for_splitting_link = ['/', '?z', '%2', '=']
    for smb in symbols_for_splitting_link:
        link = link.replace(smb, '/')
    link = link.split('/')
    owner_info = link[variables.OWNER_INFO_IDX]
    try:
        if owner_info.startswith('club') and link[variables.PHOTO_INFO_IDX].startswith('photo'):
            perhaps_id = owner_info[len('club'):]
            perhaps_id = int(perhaps_id) * -1
            return perhaps_id
        elif owner_info.startswith('id') and link[variables.PHOTO_INFO_IDX].startswith('photo'):
            perhaps_id = owner_info[len('id'):]
            perhaps_id = int(perhaps_id)
            return perhaps_id
        else:
            gui_destination.insert(tk_constants.INSERT, invalid_link_user_msg)
            log_file.write(invalid_link_log_msg)
    except ValueError:
        gui_destination.insert(tk_constants.INSERT, invalid_link_user_msg)
        log_file.write(invalid_id_representation_log_msg)
        return 0


def get_photos_id(log_file: io.TextIOWrapper,
                  gui_destination: tkinter.scrolledtext.ScrolledText,
                  link: str) -> int:
    """
    Getting photo id from photo links in album
    return get_photos_id
    """
    if link:
        if len(variables.set_owner_id) <= 1:
            split_symb = ['/', '?z', '%2', '=']  # словарь символов для разбиения адреса фото
            for x in split_symb:  # разбиение строки по разделительным символам - костыль регулярных выражений
                link = link.replace(x, '/')
            link = link.split('/')

            flag = False  # индикатор успеха нахождения подстроки photo-... в строке адреса фотографии
            for string in link:
                if string.startswith('photo'):
                    flag = True
                    split_photo_string = ['-',
                                          '_']  # словарь символов для разбиения подстроки содержащей get_photos_id в адресе фото
                    for y in split_photo_string:  # разбиение строки по разделительным символам - костыль регулярных выражений
                        string = string.replace(y, '/')
                    string = string.split('/')
                    photo_id = string[
                        len(string) - 1]  # на момент написания кода get_photos_id было последним элементом в подстроке адреса,
                    try:  # начинающейся с photo-...
                        photo_id = int(photo_id)
                        return photo_id
                    except:
                        # print('Подстрока, начинающаяся с photo-... найдена, но не удалось выделить get_photos_id являющееся int!')
                        gui_destination.insert(tk_constants.INSERT, (
                                '!Подстрока, начинающаяся с photo-... найдена, но не удалось выделить get_photos_id являющееся int!' + 12 * ' '))
                        log_file.write(
                            '!Подстрока, начинающаяся с photo-... найдена, но не удалось выделить get_photos_id являющееся int!' +
                            '\n')
                        gui_destination.insert(tk_constants.INSERT, ' ')
                    break
            if not flag:
                # print('Не удалось найти подстроку, начинающуюся с (photo-...). Проблемы в функции get_photos_id()')
                gui_destination.insert(tk_constants.INSERT,
                               '!Не удалось найти подстроку, начинающуюся с (photo-...). Проблемы в функции get_photos_id()' + 20 * ' ')
                gui_destination.insert(tk_constants.INSERT, ' ')
                log_file.write('!Не удалось найти подстроку, начинающуюся с (photo-...). Проблемы в функции get_photos_id()' +
                                '\n')
        else:
            gui_destination.insert(tk_constants.INSERT,
                           "!Добавленны фото из нескольких групп. Пожалуйста, "
                           "добавляйте фото только из одной группы" +
                           17 * ' ')
            gui_destination.insert(tk_constants.INSERT, ' ')
            log_file.write("!Добавленны фото из нескольких групп. Пожалуйста, "
                      "добавляйте фото только из одной группы" +
                        '\n')
