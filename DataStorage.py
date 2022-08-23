import datetime
import calendar

from tkinter import IntVar


class TkCounter:
    __slots__ = ('value',)

    def __init__(self):
        self.value = IntVar()
        self.set_value(0)

    def incr(self) -> int:
        self.set_value(self.get_value() + 1)
        return self.get_value()

    def decr(self) -> int:
        self.set_value(self.get_value() - 1)
        return self.get_value()

    def set_value(self, value: int) -> None:
        self.value.set(value)

    def get_value(self) -> int:
        return self.value.get()


class Data:
    __slots__ = (
        "start_time", "photo_counter",
        "owner_to_photo"
    )

    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.photo_counter = 0
        self.owner_to_photo = dict()

    def check_availability(self, owner: int, photo: int) -> bool:
        """
        Return True if associative container owner_to_photo
        contain pair (owner, photo).
        Else return False.
        :param owner:
        :param photo:
        :return:
        """
        return photo in self.owner_to_photo.get(owner, [])

    def delete(self, owner: int, photo: int) -> bool:
        """
        Delete photo from owner`s container.
        If owner had only one photo then delete owner.
        Return True when successfully delete, else - False.
        The check for existence lies with the calling code.
        :param owner:
        :param photo:
        :return:
        """
        try:
            self.owner_to_photo[owner].remove(photo)
            if not self.owner_to_photo[owner]:
                self.owner_to_photo.pop(owner)
            return True
        except:
            return False

    def add(self, owner: int, photo: int) -> bool:
        """
        Add photo to owner`s container.
        If owner had no one photo then owner create.
        Return True when successfully add, else - False.
        The check for existence lies with the calling code.
        :param owner:
        :param photo:
        :return:
        """
        try:
            owners_photo = self.owner_to_photo.get(owner, set())
            owners_photo.add(photo)
            self.owner_to_photo[owner] = owners_photo
            return True
        except:
            return False

    def get_start_time(self) -> datetime.datetime:
        self._adjust_time_value()
        return self.start_time

    def set_start_time(self, **received_time) -> None:
        received_hour = received_time['hour'] if received_time['hour'] else 0
        received_minute = received_time['minute'] if received_time['minute'] else 0
        received_second = received_time['second'] if received_time['second'] else 0

        self.start_time = datetime.datetime(
            year=self.start_time.year,
            month=self.start_time.month,
            day=self.start_time.day,
            hour=received_hour,
            minute=received_minute,
            second=received_second
        )
        self._adjust_time_value()

    def _adjust_time_value(self):
        """
        Compares the start_time value with the current time
        and changes the start_time.day if needed.
        If actual time (h:m:s) more than stored, increase stored day.
        """
        stored_time = datetime.time(
            self.start_time.hour,
            self.start_time.minute,
            self.start_time.second
        )

        actual_time = datetime.datetime.now()
        correct_day = actual_time.day
        correct_month = actual_time.month
        correct_year = actual_time.year
        actual_time = datetime.time(
            actual_time.hour,
            actual_time.minute,
            actual_time.second
        )

        if stored_time < actual_time:
            correct_day += 1
            # catch days overflow in month
            # catch month overflow in year
            days_idx = 1
            max_day_for_this_month = calendar.monthrange(
                correct_year, correct_month)[days_idx]
            if correct_day > max_day_for_this_month:
                correct_day = 1
                correct_month += 1
                if correct_month > 12:
                    correct_month = 1
                    correct_year += 1

        self.start_time = datetime.datetime(
            year=correct_year,
            month=correct_month,
            day=correct_day,
            hour=stored_time.hour,
            minute=stored_time.minute,
            second=stored_time.second
        )


# TODO: добавить в Дату служебные контейнеры -
#  слова для комментирования, фотки и т.д
