"""
Commenting at a specified time on user-defined
    VK photos from one page or group.
Outputting into_logs and obtaining information for
    authentication to / from the project folder.
"""

import vk_api
import random
import datetime
import sys
import os

DIR_PATH = os.getcwd()
LOG_FILE = open(DIR_PATH + '/into_logs.txt', 'a')


def into_logs(event: str) -> None:
    """
    Logging event to into_logs.txt
    """
    LOG_FILE.write(event + '\n')


start_time = datetime.datetime.now()
into_logs(' ')
into_logs(
    str(start_time.date()) +
    f' в {start_time.hour} часов ' +
    f'{start_time.minute} минут ' +
    f'{start_time.second} секунд'
)

# using 2 account
vk_login_src = open(DIR_PATH + '/vkEnterResources.txt', 'r')
login = vk_login_src.readline().strip()
password = vk_login_src.readline().strip()
login_other = vk_login_src.readline().strip()
password_other = vk_login_src.readline().strip()
vk_login_src.close()

# Переменные
comment_content = 'some words that will used as contents of commentary'.split()
set_owner_id = set()  # проверка чтобы все фото из стека были из одной группы
photo_stack = list()  # стек комментируемых фото - глобальная переменная
photos_link = []  # накапливает получаемые ссылки

default_start_time_hour = 17  # стандартные значения переменных,
default_start_time_minute = 0  # изменяемых из GUI
default_start_time_second = 0

HOUR_IDX = 0
MINUTE_IDX = 1
SECOND_IDX = 2

OWNER_INFO_IDX = 3
PHOTO_INFO_IDX = 5


def actual_time() -> tuple:
    """
    Indicates an actual time
    return (hour, minute, second)
    """
    time_now = datetime.datetime.now()
    return time_now.hour, time_now.minute, time_now.second


def get_owners_id(link: str) -> int:
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
    owner_info = link[OWNER_INFO_IDX]
    try:
        if owner_info.startswith('club') and link[PHOTO_INFO_IDX].startswith('photo'):
            perhaps_id = owner_info[len('club'):]
            perhaps_id = int(perhaps_id) * -1
            return perhaps_id
        elif owner_info.startswith('id') and link[PHOTO_INFO_IDX].startswith('photo'):
            perhaps_id = owner_info[len('id'):]
            perhaps_id = int(perhaps_id)
            return perhaps_id
        else:
            log_out.insert(INSERT, invalid_link_user_msg)
            into_logs(invalid_link_log_msg)
    except ValueError:
        log_out.insert(INSERT, invalid_link_user_msg)
        into_logs(invalid_id_representation_log_msg)
        return 0


def photo_id(link: str) -> int:
    """
    Getting photo id from photo links in album
    return photo_id
    """
    if link:
        if len(set_owner_id) <= 1:
            split_symb = ['/', '?z', '%2', '=']  # словарь символов для разбиения адреса фото
            for x in split_symb:  # разбиение строки по разделительным символам - костыль регулярных выражений
                link = link.replace(x, '/')
            link = link.split('/')

            flag = False  # индикатор успеха нахождения подстроки photo-... в строке адреса фотографии
            for string in link:
                if string.startswith('photo'):
                    flag = True
                    split_photo_string = ['-',
                                          '_']  # словарь символов для разбиения подстроки содержащей photo_id в адресе фото
                    for y in split_photo_string:  # разбиение строки по разделительным символам - костыль регулярных выражений
                        string = string.replace(y, '/')
                    string = string.split('/')
                    photo_id = string[
                        len(string) - 1]  # на момент написания кода photo_id было последним элементом в подстроке адреса, 
                    try:  # начинающейся с photo-...
                        photo_id = int(photo_id)
                        return photo_id
                    except:
                        # print('Подстрока, начинающаяся с photo-... найдена, но не удалось выделить photo_id являющееся int!')
                        log_out.insert(INSERT, (
                                '!Подстрока, начинающаяся с photo-... найдена, но не удалось выделить photo_id являющееся int!' + 12 * ' '))
                        into_logs(
                            '!Подстрока, начинающаяся с photo-... найдена, но не удалось выделить photo_id являющееся int!')
                        # log_out.insert(INSERT, ' ')
                    break
            if not flag:
                # print('Не удалось найти подстроку, начинающуюся с (photo-...). Проблемы в функции photo_id()')
                log_out.insert(INSERT,
                               '!Не удалось найти подстроку, начинающуюся с (photo-...). Проблемы в функции photo_id()' + 20 * ' ')
                log_out.insert(INSERT, ' ')
                into_logs('!Не удалось найти подстроку, начинающуюся с (photo-...). Проблемы в функции photo_id()')
        else:
            log_out.insert(INSERT,
                           "!Добавленны фото из нескольких групп. Пожалуйста, "
                           "добавляйте фото только из одной группы" +
                           17 * ' ')
            log_out.insert(INSERT, ' ')
            into_logs("!Добавленны фото из нескольких групп. Пожалуйста, "
                      "добавляйте фото только из одной группы")


# Main
def main(login=login, password=password, login_other=login_other, password_other=password_other):
    '''
    Основная функция, выполняемая параллельно tkinter-части
    в потоке th_main.
    Задействует vk_api, заходит в вк через login-password,
    в случае vk_api.exceptions.Captcha заходит в
    login_other\password_other, переименовывая их
    (a, b = b, a)
    Берет ИД фот из photo_stack
    ИД хозяина группы из set_owner_id, где должен храниться только 1 элемент.
    '''
    # Перенаправление потока ошибок в файл логов
    err = open(DIR_PATH + '/into_logs.txt', 'a')
    old_err = sys.stderr
    sys.stderr = err

    session = vk_api.VkApi(login=login, password=password, app_id=2685278)
    session.auth()
    # log.append('выполнен вход в {}'.format(login) + (70 - len('выполнен вход в {}'.format(login))) * ' ')
    log_out.insert(INSERT, '-' * 35)
    log_out.insert(INSERT, 'выполнен вход в {}'.format(login) + (70 - len('выполнен вход в {}'.format(login))) * ' ')
    into_logs('выполнен вход в {}'.format(login))
    # print('-'*20)
    # print('выполнен вход в {}'.format(login))
    # Организация цикла while (список не пустой) с try-except для отправки сообщений
    owner_id = list(set_owner_id)[0]  # -201267535 id группы для комментирования (ТРЕНИРОВОЧНАЯ ГРУППА)

    while True:  # вместо for i in range(10000)
        time = actual_time()
        if time[HOUR_IDX] == default_start_time_hour and time[MINUTE_IDX] == default_start_time_minute and time[
            SECOND_IDX] >= default_start_time_second:
            while photo_stack:  # пока фотот стек не пустой !!!не забывать убирать id из стека после комментирования
                print(photo_stack)
                try:
                    for i in range(len(photo_stack)):
                        photo_id = photo_stack[0]
                        # message = ( str(random.randint(0,100))+chr(random.randint(97, 122)) + ' ' + 
                        #                                    chr(random.randint(65, 90)) + str(random.randint(0,100)) )
                        message = (random.choice(comment_content))
                        session.method('photos.createComment', {'owner_id': owner_id,
                                                                'photo_id': photo_id,
                                                                'message': message})
                        # log.append('оставлен комментарий с {}'.format(login))
                        log_out.insert(INSERT, 'оставлен комментарий с {}'.format(login) + (
                                70 - len('оставлен комментарий с {}'.format(login))) * ' ')
                        into_logs('оставлен комментарий с {}'.format(login))
                        # print('оставлен комментарий с {}'.format(login))
                        photo_stack.remove(photo_id)

                except vk_api.exceptions.Captcha:
                    # log.append('выход из {}'.format(login))
                    # print('-'*20)
                    log_out.insert(INSERT, '-' * 35)
                    # print('выход из {}'.format(login))
                    log_out.insert(INSERT, 'выход из {}'.format(login) + (70 - len('выход из {}'.format(login))) * ' ')
                    into_logs('выход из {}'.format(login))
                    login, login_other = login_other, login  # меняем логин и пароль, аутентифицируемся
                    password, password_other = password_other, password
                    session = vk_api.VkApi(login=login, password=password, app_id=2685278)
                    session.auth()
                    # log.append('выполнен вход в {}'.format(login))
                    # print('-'*20)
                    log_out.insert(INSERT, '-' * 35)
                    # print('выполнен вход в {}'.format(login))
                    log_out.insert(INSERT, 'выполнен вход в {}'.format(login) + (
                            70 - len('выполнен вход в {}'.format(login))) * ' ')
                    into_logs('выполнен вход в {}'.format(login))
                except vk_api.exceptions.ApiError:
                    pass
                global empty_for_normal_text
                empty_for_normal_text = Label(window, text=' ', font=font)
                empty_for_normal_text.grid(column=0, row=8)
            grey_else()
            grey_del()

            global enter_lvl_1
            enter_lvl_1 = Button(window, text="ввести", command=click_enter, font=font)
            enter_lvl_1.grid(column=4, row=0)

            break

    sys.stderr = old_err

    log_out.insert(INSERT, '-' * 35)
    log_out.insert(INSERT, 'Программа закончила выполнение     ')
    into_logs('Программа закончила выполнение     ')


# Многопоточность
from threading import Thread

th_main = Thread(target=main, args=())

from tkinter import *

'''
Упрощенная версия без формирования основного стека, а только else и del
'''


# Действия конопок первого уровня______________________________________________________________________________________________
def click_enter():  # пусть станет серой при нажатии
    '''
    Действие кнопки верхнего уровня для ввода времени.
    Меняет значения hour_input, minute_input, second_input,
        если они были введены в поля Entry.
    Генерирует при первом нажатии такую же кнопку, как и кнопку вызова, но темную.
    '''
    global default_start_time_hour, default_start_time_minute, default_start_time_second
    if time_hour.get(): default_start_time_hour = int(time_hour.get())  # изменение стандартного значения
    if time_minute.get(): default_start_time_minute = int(time_minute.get())  # времени в модуле autocomment_work_module
    if time_second.get(): default_start_time_second = int(time_second.get())
    enter_lvl_1 = Button(window, text="ввести", command=click_enter,
                         bg='light grey', font=font)
    enter_lvl_1.grid(column=4, row=0)

    into_logs('Введенное время - {}:{}:{}'.format(default_start_time_hour, default_start_time_minute,
                                                  default_start_time_second))


# Действия конопок второго уровня_______________________________________________________________________________________________
def else_photo():
    '''
    Действие кнопки второго уровня для добавления ссылки.
    Генерирует поля ввода для ссылки и приглашающую надпись.
    Вызывает функцию вызова кнопки ввода с параметром 'else'.
    "Красит" вызывающую кнопку и меняет геометрию окна window.
    '''
    global link_invintation, link_enter  # !
    link_invintation = Label(window, text='Вставьте ссылку',
                             font=font)
    link_invintation.grid(column=0, row=3)

    link_enter = Entry(window, width=15, font=font)
    link_enter.grid(column=4, row=3)

    enter('else')

    black_grey_else()
    grey_del()
    window.geometry('370x320')


def del_photo():
    '''
    Действие кнопки второго уровня для удаления ссылки.
    Генерирует поля ввода для ссылки и приглашающую надпись.
    Вызывает функцию вызова кнопки ввода с параметром 'delete'.
    "Красит" вызывающую кнопку.
    '''
    global link_invintation, link_enter  # !
    link_invintation = Label(window, text='Вставьте ссылку',
                             font=font)
    link_invintation.grid(column=0, row=3)

    link_enter = Entry(window, width=15, font=font)
    link_enter.grid(column=4, row=3)

    enter('delete')

    black_grey_del()
    grey_else()


def enter(mod):
    '''
    Вызывается из else_photo или del_photo.
    Функция вызова кнопки для ввода с двумя возможными модификациями:
        'else' - создает кнопку с добавлением ссылки на фото в качестве действия нажатия; 
        'delete' - создает кнопку с удалением, если возможно, ссылки на фото в качестве действия нажатия;
    Кнопка с именем enter_lvl_2 - глобальная для объемлющего модуля переменная.
    '''
    global enter_lvl_2
    if mod == 'else':
        enter_lvl_2 = Button(window, text="     Ввод      ",
                             command=pop_link, font=font)
        enter_lvl_2.grid(column=0, row=4)
    if mod == 'delete':
        enter_lvl_2 = Button(window, text="     Ввод      ",
                             command=del_link, font=font)
        enter_lvl_2.grid(column=0, row=4)


def pop_link():  # отсылает полученную ссылку как строковый элемент в функцию для получения id фото?
    finish_button()
    # log_button()

    link = link_enter.get()
    owner_id = get_owners_id(link)
    photos_id = photo_id(link)
    if link and owner_id and (photos_id not in photo_stack):
        if not set_owner_id:
            photo_stack.append(photos_id)  # пропихнуть ссылку
            set_owner_id.add(owner_id)  # owner_id в сет хозяев групп
            photos_link.append(link)  # добавить введенную ССЫЛКУ в список ссылок
        elif owner_id in set_owner_id:
            photo_stack.append(photos_id)  # пропихнуть ссылку
            photos_link.append(link)  # добавить введенную ССЫЛКУ в список ссылок
        elif owner_id not in set_owner_id:
            # print("!Добавленны фото из нескольких групп. Пожалуйста, добавляйте фото только из одной группы") #вывести предупреждение о том                                                                                                          #   что надо из одной группы кидать
            log_out.insert(INSERT,
                           '!Добавленны фото из нескольких групп. Пожалуйста, добавляйте фото только из одной группы' + 17 * ' ')
            into_logs('!Добавленны фото из нескольких групп. Пожалуйста, добавляйте фото только из одной группы')
    elif not link:
        log_out.insert(INSERT, 'Вставьте ссылку!' + (35 - len('Вставьте ссылку!')) * ' ')
        into_logs('Вставьте ссылку!')
    link_enter.delete(0, END)

    window.geometry('370x370')

    print('photo_stack is {}'.format(photo_stack))
    log_out.insert(INSERT, 'Добавленно {} фото'.format(len(photo_stack)) + (
            35 - len('Добавленно {} фото'.format(len(photo_stack)))) * ' ')
    into_logs('Добавленно {} фото'.format(len(photo_stack)))


def del_link():
    link = link_enter.get()
    if link:
        photos_id = photo_id(link)
        if photos_id in photo_stack:
            photo_stack.remove(photos_id)
            try:
                photos_link.remove(link)  # удалить, если можно, введенную ССЫЛКУ из списка ссылок
            except:
                pass
        else:
            print('!Невозможно удалить из списка - Вы еще не добавляли такого фото.')  # в вывод пользователю
            log_out.insert(INSERT, '!Невозможно удалить из списка - Вы еще не добавляли такого фото.' + (
                    70 - len('!Невозможно удалить из списка - Вы еще не добавляли такого фото.')))
            into_logs('!Невозможно удалить из списка - Вы еще не добавляли такого фото.')
    else:
        log_out.insert(INSERT, 'Вставьте ссылку!' + (35 - len('Вставьте ссылку!')) * ' ')
        into_logs('Вставьте ссылку!')

    link_enter.delete(0, END)
    # print('photo_stack is {}'.format(photo_stack))


# Действия конопок третьего уровня______________________________________________________________________________________________
def finish_button():
    global flag, start

    nothing = Label(window, text=' ', font=font)
    nothing.grid(column=0, row=5)

    start = Button(window, text="Начало работы", command=main_start,
                   font=font)
    start.grid(column=0, row=6)


def main_start():
    '''
    Действия кнопки начала работы.
    Сначала запускает поток th_main с выполнением функции main(главная функция программы),
        потом в логи выводит ссылки, которые должен был откомментить.
    '''
    th_main.start()

    into_logs('-Введенные для комментирования ссылки:-')
    for link in photos_link:
        into_logs(link)
    into_logs('-Конец списка ссылок-')


# Состояния конопок второго уровня_______________________________________________________________________________________________        

def grey_else():
    global switch_photo_else
    switch_photo_else = Button(window, text="Добавить к списку",
                               command=else_photo, font=font)
    switch_photo_else.grid(column=0, row=2)


def black_grey_else():
    global switch_photo_else
    switch_photo_else = Button(window, text="Добавить к списку",
                               bg='light grey', command=else_photo, font=font)
    switch_photo_else.grid(column=0, row=2)


def grey_del():
    global switch_photo_del
    switch_photo_del = Button(window, text="Удалить из списка",
                              command=del_photo, font=font)
    switch_photo_del.grid(column=4, row=2)


def black_grey_del():
    global switch_photo_del
    switch_photo_del = Button(window, text="Удалить из списка",
                              bg='light grey', command=del_photo, font=font)
    switch_photo_del.grid(column=4, row=2)


# ____________________________________________Main_part______________________________________________________________________#   

font = ('Georgia', 10)  # шрифты Arial Bold
window = Tk()
window.title('ВК-комментарий по таймеру')
window.geometry('370x270')

# Определение нужного времени
time_invitation = Label(window, text='Время (час/мин/сек) - ',
                         font=font)
time_invitation.grid(column=0, row=0)

time_hour = Entry(window, width=2, font=font)
time_hour.grid(column=1, row=0)

time_minute = Entry(window, width=2, font=font)
time_minute.grid(column=2, row=0)

time_second = Entry(window, width=2, font=font)
time_second.grid(column=3, row=0)

enter_lvl_1 = Button(window, text="ввести", command=click_enter, font=font)
enter_lvl_1.grid(column=4, row=0)

nothing0 = Label(window, text=' ', font=font)  # nothing - костыль для пропуска строки
nothing0.grid(column=0, row=1)

nothing1 = Label(window, text=' ', font=font)
nothing1.grid(column=1, row=1)

nothing2 = Label(window, text=' ', font=font)
nothing2.grid(column=2, row=1)

# для одинакового ввода времени
empty_for_normal_time_entry0 = Label(window, text=' ', font=font)
empty_for_normal_time_entry0.grid(column=1, row=2)

empty_for_normal_time_entry1 = Label(window, text=' ', font=font)
empty_for_normal_time_entry1.grid(column=2, row=2)

empty_for_normal_time_entry2 = Label(window, text=' ', font=font)
empty_for_normal_time_entry2.grid(column=3, row=2)
# Ввод кнопок
grey_else()
grey_del()

# Костыль для нормального вывода текста
empty_for_normal_text = Label(window, text=' ', font=font)
empty_for_normal_text.grid(column=0, row=7)

from tkinter import scrolledtext

log_out = scrolledtext.ScrolledText(window, width=35, height=10)
log_out.grid(column=0, row=8, columnspan=6)

log_out.insert(INSERT, 'По умолчанию значение времени(ч\м\с) = 17:0:0' + (
        70 - len('По умолчанию значение времени(ч\м\с) = 17:0:0')) * ' ')

window.mainloop()

LOG_FILE.close()
