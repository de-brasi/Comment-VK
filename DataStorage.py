import datetime


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
        # TODO: catch case when difference between dates too big that new day start
        pass

    def set_start_time(self, **time_value) -> None:
        hour = time_value['hour'] if time_value['hour'] else 0
        minute = time_value['minute'] if time_value['minute'] else 0
        second = time_value['second'] if time_value['second'] else 0
        if passed time less then now:
            day = next day
        else:
            day = day
        remember values

# TODO: добавить в Дату служебные контейнеры -
#  слова для комментирования, фотки и т.д
