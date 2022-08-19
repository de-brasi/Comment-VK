from collections import namedtuple
from typing import List

import constants


def get_users_access_info() -> List[namedtuple]:
    """
    Parse file with users logins and passwords.
    Return list of namedtuple
    :param :
    :return:
    """
    file = open(constants.AUTHORIZATION_INFO_FILE, 'r')
    users_info = list()

    UserInfo = namedtuple("UserInfo", ["login", "password"])

    for login_password in file.readlines():
        login, password = login_password.split()
        users_info.append(UserInfo(login, password))
    return users_info
