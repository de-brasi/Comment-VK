import io
import tkinter
import random
import sys
import tkinter.scrolledtext
from tkinter import constants as tk_constants
from tkinter import Label
from tkinter import Button

import variables
import tools
import vk_api


def main(
        log_file: io.TextIOWrapper, gui_destination: tkinter.scrolledtext.ScrolledText,
        login=variables.login, password=variables.password,
        login_other=variables.login_other, password_other=variables.password_other
         ):
    '''
    Основная функция, выполняемая параллельно tkinter-части
    в потоке th_main.
    Задействует vk_api, заходит в вк через login-password,
    в случае vk_api.exceptions.Captcha заходит в
    login_other\password_other, переименовывая их
    (a, b = b, a)
    Берет ИД фот из photo_stack
    ИД хозяина группы из variables.set_owner_id, где должен храниться только 1 элемент.
    '''
    # Перенаправление потока ошибок в файл логов
    new_err_stream = open(variables.DIR_PATH + '/logs.txt', 'a')
    old_err_stream = sys.stderr
    sys.stderr = new_err_stream

    session = vk_api.VkApi(login=login, password=password, app_id=2685278)
    session.auth()
    gui_destination.insert(tk_constants.INSERT, '-' * 35)
    gui_destination.insert(tk_constants.INSERT,
                   'выполнен вход в {}'.format(login) + (70 - len('выполнен вход в {}'.format(login))) * ' ')
    log_file.write('выполнен вход в {}'.format(login) +
                   '\n')
    owner_id = list(variables.set_owner_id)[0]

    while True:
        time_now = tools.actual_time()
        if time_now.hour == variables.default_start_time_hour and \
                time_now.minute == variables.default_start_time_minute and time_now.second >= variables.default_start_time_second:
            while variables.photo_stack:  # пока фотот стек не пустой !!!не забывать убирать id из стека после комментирования
                print(variables.photo_stack)
                try:
                    for i in range(len(variables.photo_stack)):
                        photo_id = variables.photo_stack[0]
                        message = (random.choice(variables.comment_content))
                        session.method('photos.createComment', {'owner_id': owner_id,
                                                                'get_photos_id': photo_id,
                                                                'message': message})
                        gui_destination.insert(tk_constants.INSERT, 'оставлен комментарий с {}'.format(login) + (
                                70 - len('оставлен комментарий с {}'.format(login))) * ' ')
                        log_file.write('оставлен комментарий с {}'.format(login) +
                                       '\n')
                        variables.photo_stack.remove(photo_id)

                except vk_api.exceptions.Captcha:
                    gui_destination.insert(tk_constants.INSERT, '-' * 35)
                    gui_destination.insert(tk_constants.INSERT,
                                   'выход из {}'.format(login) + (70 - len('выход из {}'.format(login))) * ' ')
                    log_file.write('выход из {}'.format(login) +
                                   '\n')
                    login, login_other = login_other, login  # меняем логин и пароль, аутентифицируемся
                    password, password_other = password_other, password
                    session = vk_api.VkApi(login=login, password=password, app_id=2685278)
                    session.auth()
                    gui_destination.insert(tk_constants.INSERT, '-' * 35)
                    gui_destination.insert(tk_constants.INSERT, 'выполнен вход в {}'.format(login) + (
                            70 - len('выполнен вход в {}'.format(login))) * ' ')
                    log_file.write('выполнен вход в {}'.format(login) +
                                   '\n')
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

    sys.stderr = old_err_stream

    gui_destination.insert(tk_constants.INSERT, '-' * 35)
    gui_destination.insert(tk_constants.INSERT, 'Программа закончила выполнение     ')
    log_file.write('Программа закончила выполнение     ' +
                   '\n')
