import constants as app_constants
import utils

from Handler import Handler
from Handler import Mode
from tkinter import constants
from tkinter import scrolledtext

import button_functions
import tkinter
import time
import datetime
import DataStorage


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
                 'handling_mode', 'logs_to_user')

    def __init__(self, _handler: Handler):
        self.handler = _handler
        self.handling_mode = Mode("add")

        self.view = tkinter.Tk()
        self.data = DataStorage.Data()
        self.button_references = dict()

        self.view.title(app_constants.TITLE)
        self.view.geometry(app_constants.GEOMETRY)

        self.photo_counter = tkinter.IntVar()
        self.photo_counter.set(0)

        "First interface`s row"
        self.make_getting_start_time_from_user()
        self.make_spacing_plug()

        "Second interface`s row"
        self.make_display_added_photo_count()

        "Third interface`s row"
        self.make_buttons_for_handling_mode()

        "Fourth interface`s row"
        self.make_entering_link()

        "Fifth interface`s row"
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
                text=app_constants.TIME_INVITATION,
                font=app_constants.FONT)
        time_invitation.grid(
            column=0,
            row=0)

        default_time = self.data.get_start_time()
        # Time windows
        time_hour = tkinter.Entry(
            self.view,
            width=2,
            font=app_constants.FONT)
        time_hour.insert(constants.END, str(default_time.hour))
        time_hour.grid(
            column=1,
            row=0)

        time_minute = tkinter.Entry(
            self.view,
            width=2,
            font=app_constants.FONT)
        time_minute.insert(constants.END, str(default_time.minute))
        time_minute.grid(
            column=2,
            row=0)

        time_second = tkinter.Entry(
            self.view,
            width=2,
            font=app_constants.FONT)
        time_second.grid(
            column=3,
            row=0)
        time_second.insert(constants.END, str(default_time.second))

        # Time button
        time_enter_button = tkinter.Button(
            self.view,
            text=app_constants.TIME_ENTER_BUTTON_TEXT,
            font=app_constants.FONT)
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
            font=app_constants.FONT)
        nothing0.grid(
            column=0,
            row=1)

        nothing1 = tkinter.Label(
            self.view,
            text=' ',
            font=app_constants.FONT)
        nothing1.grid(
            column=1,
            row=1)

        nothing2 = tkinter.Label(
            self.view,
            text=' ',
            font=app_constants.FONT)
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
                text=app_constants.PHOTO_COUNT_TEXT,
                font=app_constants.FONT)
        count_photo_text.grid(
            column=0,
            row=1)

        count_photo_val = \
            tkinter.Label(
                self.view,
                textvariable=self.photo_counter,
                font=app_constants.FONT,
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
            self.view, text=app_constants.ADD_PHOTO_TEXT,
            command=lambda: button_functions.set_add_mode(
                self.handling_mode, self.button_references
            ),
            background='light grey',
            font=app_constants.FONT)
        set_add_mode_button.grid(column=0, row=2)
        self.button_references['set_add_mode_button'] = set_add_mode_button

        set_del_mode_button = tkinter.Button(
            self.view, text=app_constants.DEL_PHOTO_TEXT,
            background='light grey',
            command=lambda: button_functions.set_del_mode(
                self.handling_mode, self.button_references
            ),
            font=app_constants.FONT)
        set_del_mode_button.grid(column=4, row=2)
        self.button_references['set_del_mode_button'] = set_del_mode_button

    def make_entering_link(self):
        """
        Make field and button for
        getting link for handle from user.
        :return:
        """
        # TODO: make invitation on Label that disappear when click and add link
        link_invitation = tkinter.Label(
            self.view, text='Cсылка',
            font=app_constants.FONT)
        link_invitation.grid(column=0, row=3)

        link_enter = make_entry(self.view, background="#FFFFEF",
                                font=app_constants.FONT,
                                width=15, border_width=3,
                                temporary_text="Вставьте ссылку")
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
            font=app_constants.FONT
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
            command=lambda: self.start(),
            font=app_constants.FONT)
        start_button.grid(column=0, row=4)
        self.button_references['start_button'] = start_button

    def make_log_field(self):
        """
        Show log to user.
        :return:
        """
        self.logs_to_user = \
            scrolledtext.ScrolledText(
                self.view, width=35, height=10
            )
        self.logs_to_user.grid(
            column=0, row=8, columnspan=6
        )

    def start(self):
        # TODO: multithread version
        """
        Single thread version.
        :return:
        """
        # Пока нормально работает только при одном нажатии
        # TODO: на выполнение этой команды надо создавать отдельный поток
        #  для выполнения core функции. Причем сразу после нажатия кнопки
        #  start необходимо сбрасывать предыдущий поток чтобы не
        #  порождать кучу задач при множественном нажатии

        # TODO: блокировать кнопки ввода дат и фоток,
        #  в идеале вообще отрисовать новое окно.
        #  Тогда добавить и кнопку рестарта приложения с остановкой функции start
        sessions = [
            utils.make_session(user) for user in utils.get_users_access_info()
        ]
        # TODO: как то обработать ситуацию, когда введены неверные данные.
        #  Мб как то смотреть на логин или есть в API методы
        #  для проверки существования
        if not sessions:
            RegistrationWindow().show()
            # assert at least one account saved

        start_time = self.data.get_start_time()
        time_for_sleep = \
            (start_time - datetime.datetime.now()).seconds - \
            app_constants.PREPARATION_TIME_IN_SECONDS
        time.sleep(time_for_sleep)
        while True:
            if datetime.datetime.now() >= start_time:
                self.handler.core(self, sessions)
                break
        # TODO: исчезновение дефолтного времени при начале ввода своего времени


class MessageWindow:
    __slots__ = ('view',)

    def __init__(self, message):
        self.view = tkinter.Tk()
        self.view.geometry(app_constants.GEOMETRY)

        tkinter.Label(
            self.view,
            text=message,
            font=app_constants.FONT
        )
        tkinter.Button(
            self.view, text="Ok",
            command=lambda: destroy_window(self.view),
            background='light grey',
            font=app_constants.FONT
        )

    def show(self):
        self.view.mainloop()


class RegistrationWindow:
    # TODO: показать окно авторизации.
    #  Вызванное окно должно получить от юзера данные,
    #  либо закрыть приложение при отказе вводить
    #  (во избежании переполнения стека)
    __slots__ = ('view',)

    def __init__(self):
        self.view = tkinter.Tk()
        self.view.geometry(app_constants.GEOMETRY)

        login_entry = tkinter.Entry(
            self.view,
            width=15,
            font=app_constants.FONT,
        )
        login_entry.insert(0, "Type login here")
        password_entry = tkinter.Entry()

        get_info_btn = tkinter.Button()
        # TODO: show message if no login or password

    def show(self):
        self.view.mainloop()


def destroy_window(window: tkinter.Tk):
    window.destroy()


def make_entry(parent, background, font,
               width, border_width, temporary_text="") -> tkinter.Entry:
    entry = tkinter.Entry(
        parent, bg=background, width=width, borderwidth=border_width, font=font
    )

    if temporary_text:
        entry.insert(0, temporary_text)
        entry.config(fg=app_constants.TEXT_COLOUR_DEFAULT)
        entry.bind("<FocusIn>", lambda _: focus_in(entry, temporary_text))
        entry.bind("<FocusOut>", lambda _: focus_out(entry, temporary_text))

    return entry


def focus_in(entry_field: tkinter.Entry, default_text: str):
    if entry_field.get() == default_text:
        entry_field.delete(0, "end")
        entry_field.config(fg=app_constants.TEXT_COLOUR_TYPING)


def focus_out(entry_field: tkinter.Entry, default_text: str):
    if not entry_field.get():
        entry_field.insert(0, default_text)
        entry_field.config(fg=app_constants.TEXT_COLOUR_DEFAULT)


# TODO: обобщить создание строк типа: окно ввода + кнопка
