"""
Commenting at a specified time on user-defined
    VK photos from one page or group.
Outputting into logs and obtaining information for
    authentication to / from the project folder.
"""

import vk_api
import random
import sys
import os

import core
import variables
import tools

DIR_PATH = os.getcwd()
LOG_FILE = open(DIR_PATH + '/service_information/logs.txt', 'a')

start_time = tools.actual_time()
LOG_FILE.write(
    '\n' +
    str(start_time.date()) +
    f' в {start_time.hour} часов ' +
    f'{start_time.minute} минут ' +
    f'{start_time.second} секунд' +
    '\n'
)

OWNER_INFO_IDX = 3
PHOTO_INFO_IDX = 5


# Многопоточность
from threading import Thread

th_main = Thread(target=core.main, args=())

from tkinter import *

# ____________________________________________Main_part______________________________________________________________________#
if __name__ == "__main__":
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

# TODO: функция click_enter делает переменные default_start_time_hour,
#  default_start_time_minute, default_start_time_second глобальными.
#  Изначально импортируются из variables

# TODO: общие блоки кода с логированием в logs.txt и GUI вынести в одну функцию (
#  встречается в core.py, tools.py, main.py)
