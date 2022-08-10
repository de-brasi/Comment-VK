import os

DIR_PATH = os.getcwd()

OWNER_INFO_IDX = 3
PHOTO_INFO_IDX = 5

# Enter sources
vk_login_src = open(DIR_PATH + '/service_information/vkEnterResources.txt', 'r')
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
