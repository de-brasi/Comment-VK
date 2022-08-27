from collections import namedtuple
from typing import List

import constants as app_constants
import vk_api


def get_users_access_info() -> List[namedtuple]:
    """
    Parse file with users logins and passwords.
    Return list of namedtuple
    :param :
    :return:
    """
    file = open(app_constants.AUTHORIZATION_INFO_FILE, 'r')
    users_info = list()

    UserInfo = namedtuple("UserInfo", ["login", "password"])

    for login_password in file.readlines():
        login, password = login_password.split()
        users_info.append(UserInfo(login, password))
    return users_info


def make_session(passing_info):
    session = vk_api.VkApi(
        login=passing_info.login,
        password=passing_info.password,
        app_id=app_constants.VK_STANDALONE_APPLICATION_ID
    )
    session.auth()
    return session


def make_comment(session, owner_id, photo_id, *comment_words):
    message = ' '.join(comment_words)
    session.method('photos.createComment', {'owner_id': owner_id,
                                            'photo_id': photo_id,
                                            'message': message})
