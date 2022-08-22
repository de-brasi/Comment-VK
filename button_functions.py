from DataStorage import Data
from Handler import Handler
from Handler import Mode
from tkinter import Entry
from tkinter import IntVar


def get_time_click(data_storage: Data,
                   time_hour: Entry,
                   time_minute: Entry,
                   time_second: Entry
                   ):
    """
    Getting time value from user.
    Store in data storage.
    """
    if any((time_hour.get(), time_minute.get(), time_second.get())):
        data_storage.set_start_time(
            hour=time_hour.get(),
            minute=time_minute.get(),
            second=time_second.get()
        )
        # TODO: show message about working time: DAY/HOUR/MIN/SEC
    else:
        # TODO: show message that time not write
        pass


# TODO: make switch-buttons class for
#  auto select colours for non-active buttons
def set_add_mode(selected_mode: Mode,
                 button_refs: dict
                 ):
    selected_mode.set_mode("add")
    button_refs['set_add_mode_button'].config(
        background='grey'
    )
    button_refs['set_del_mode_button'].config(
        background='light grey'
    )


def set_del_mode(selected_mode: Mode,
                 button_refs: dict
                 ):
    selected_mode.set_mode("delete")
    button_refs['set_del_mode_button'].config(
        background='grey'
    )
    button_refs['set_add_mode_button'].config(
        background='light grey'
    )


def handle_link(link: str,
                data_storage: Data,
                photo_counter: IntVar,
                handler: Handler,
                mode: Mode):
    # TODO: raise exception page if link not valid
    try:
        handler.validate_url(link)
        owner = handler.get_owner_id(link)
        photo = handler.get_photo_id(link)
        # TODO: нормальная реализация класса для mode,
        # TODO: вместо mode[0]
        if mode.get_mode() == "add":
            handler.add_photo(
                owner, photo, data_storage, photo_counter
            )
        else:
            handler.delete_photo(
                owner, photo, data_storage, photo_counter
            )
    except ValueError:
        # Erase info to user about non-correct link view
        pass
