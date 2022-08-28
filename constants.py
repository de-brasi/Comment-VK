import pathlib

FONT = ('Georgia', 10)
TITLE = "ВК-комментарий по таймеру"
GEOMETRY = "440x330"

TIME_INVITATION = "Время (час/мин/сек) - "
TIME_ENTER_BUTTON_TEXT = "ввести"

PHOTO_COUNT_TEXT = "Добавлено фото:"

ADD_PHOTO_TEXT = "Добавить к списку"
DEL_PHOTO_TEXT = "Удалить из списка"

# AUTHORIZATION_INFO_FILE = "./service_data/vk_enter_resources.txt"
AUTHORIZATION_INFO_FILE = \
    str(pathlib.Path(__file__).parent.resolve()) + \
    "/service_data/vk_enter_resources.txt"

PREPARATION_TIME_IN_SECONDS = 2

VK_STANDALONE_APPLICATION_ID = 7755287
