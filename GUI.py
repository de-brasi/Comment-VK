from Handler import Handler
from Handler import HandlingMode
from DataStorage import Data
from tkinter import constants
from tkinter import scrolledtext

import button_functions
import tkinter

FONT = ('Georgia', 10)
TITLE = "ВК-комментарий по таймеру"
GEOMETRY = "440x330"

TIME_INVITATION = "Время (час/мин/сек) - "
TIME_ENTER_BUTTON_TEXT = "ввести"

PHOTO_COUNT_TEXT = "Добавлено фото:"

ADD_PHOTO_TEXT = "Добавить к списку"
DEL_PHOTO_TEXT = "Удалить из списка"

TIME_DEFAULT_HOUR = 12
TIME_DEFAULT_MINUTE = 0
TIME_DEFAULT_SECOND = 0


class Interface:
    """
    1) ввод времени
    2) счетчик добавленных
    3) добавить/удалить
    4) ссылка/ ввод
    5) логи
    """
    __slots__ = ('view', 'data', 'handler',
                 'photo_counter', 'button_references',
                 'handling_mode')

    def __init__(self, _handler: Handler):
        self.handler = _handler
        self.handling_mode = HandlingMode.ADD

        self.view = tkinter.Tk()
        self.data = Data()
        self.button_references = dict()

        self.view.title(TITLE)
        self.view.geometry(GEOMETRY)

        self.photo_counter = tkinter.IntVar()
        self.photo_counter.set(0)

        "First interface`s row"
        self.make_getting_start_time_from_user()
        self.make_spacing_plug()

        "Second interface`s row"
        self.make_display_added_photo_count()

        "Third interface`s row"
        self.make_buttons_for_handling_mode()

        "Fourth строка интерфейса"
        self.make_entering_link()

        "Fifth строка интерфейса"
        self.start_useful_work_button()

        # TODO: загрузка (сколько осталось времени)

        self.make_log_field()

    def make_getting_start_time_from_user(self) -> None:
        """
        Make 3 entry fields for time and
        button for getting it as one row.
        :return: None
        """
        # Time invitation
        time_invitation = \
            tkinter.Label(
                self.view,
                text=TIME_INVITATION,
                font=FONT)
        time_invitation.grid(
            column=0,
            row=0)

        # Time windows
        time_hour = tkinter.Entry(
            self.view,
            width=2,
            font=FONT)
        time_hour.insert(constants.END, str(TIME_DEFAULT_HOUR))
        time_hour.grid(
            column=1,
            row=0)

        time_minute = tkinter.Entry(
            self.view,
            width=2,
            font=FONT)
        time_minute.insert(constants.END, str(TIME_DEFAULT_MINUTE))
        time_minute.grid(
            column=2,
            row=0)

        time_second = tkinter.Entry(
            self.view,
            width=2,
            font=FONT)
        time_second.grid(
            column=3,
            row=0)
        time_second.insert(constants.END, str(TIME_DEFAULT_SECOND))

        # Time button
        time_enter_button = tkinter.Button(
            self.view,
            text=TIME_ENTER_BUTTON_TEXT,
            font=FONT)
        self.button_references['time_enter_button'] = time_enter_button
        time_enter_button.config(
            command=lambda: button_functions.get_time_click(
                self.data, time_hour, time_minute, time_second
            )
        )
        time_enter_button.grid(
            column=4,
            row=0)

    def make_spacing_plug(self) -> None:
        """
        Make vertical offset.
        :return: None
        """
        # TODO: reformat it
        nothing0 = tkinter.Label(
            self.view,
            text=' ',
            font=FONT)  # nothing - костыль для пропуска строки
        nothing0.grid(
            column=0,
            row=1)

        nothing1 = tkinter.Label(
            self.view,
            text=' ',
            font=FONT)
        nothing1.grid(
            column=1,
            row=1)

        nothing2 = tkinter.Label(
            self.view,
            text=' ',
            font=FONT)
        nothing2.grid(
            column=2,
            row=1)

    def make_display_added_photo_count(self) -> None:
        """
        Display count of added photo.
        Use a self.photo_counter as a counter.
        :return:
        """
        count_photo_text = \
            tkinter.Label(
                self.view,
                text=PHOTO_COUNT_TEXT,
                font=FONT)
        count_photo_text.grid(
            column=0,
            row=1)

        count_photo_val = \
            tkinter.Label(
                self.view,
                textvariable=self.photo_counter,
                font=FONT,
                background="#fff")
        count_photo_val.grid(
            column=1,
            row=1)

    def make_buttons_for_handling_mode(self):
        """
        Make switchable buttons for selecting mode
        that will be used when handle.
        :return:
        """
        set_add_mode_button = tkinter.Button(
            self.view, text=ADD_PHOTO_TEXT,
            background='light grey',
            font=FONT)
        set_add_mode_button.grid(column=0, row=2)
        self.button_references['set_add_mode_button'] = set_add_mode_button
        set_add_mode_button.config(
            command=lambda: button_functions.set_add_mode(
                self.handling_mode, self.button_references
            )
        )

        set_del_mode_button = tkinter.Button(
            self.view, text=DEL_PHOTO_TEXT,
            background='light grey',
            font=FONT)
        set_del_mode_button.grid(column=4, row=2)
        self.button_references['set_del_mode_button'] = set_del_mode_button
        set_del_mode_button.config(
            command=lambda: button_functions.set_del_mode(
                self.handling_mode, self.button_references
            )
        )

    def make_entering_link(self):
        """
        Make field and button for
        getting link for handle from user.
        :return:
        """
        # TODO: make invitation on Label that disappear when click and add link
        link_invitation = tkinter.Label(
            self.view, text='Вставьте ссылку',
            font=FONT)
        link_invitation.grid(column=0, row=3)

        link_enter = tkinter.Entry(
            self.view, width=15, font=FONT)
        link_enter.grid(column=4, row=3)

        link_enter_button = tkinter.Button(
            self.view,
            text="Ввод",
            command=lambda: button_functions.handle_link(
                link_enter.get(),
                self.data,
                self.photo_counter,
                self.handler,
                self.handling_mode
            ),
            font=FONT
        )
        link_enter_button.grid(column=5, row=3)

    def start_useful_work_button(self):
        """
        Start handling collected to Data instance
        information using Handler.core.
        :return:
        """
        start_button = tkinter.Button(
            self.view, text="Старт",
            command=lambda: self.start,
            font=FONT)
        start_button.grid(column=0, row=4)
        self.button_references['start_button'] = start_button

    def make_log_field(self):
        """
        Show log to user.
        :return:
        """
        log_out = scrolledtext.ScrolledText(self.view, width=35, height=10)
        log_out.grid(column=0, row=8, columnspan=6)

    def start(self):
        pass

# TODO: исчезновение дефолтного времени при начале ввода своего времени
