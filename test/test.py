if __name__ == "__main__":
    import sys

    import constants
    from test_utils import custom_assert
    from Handler import Handler
    from utils import get_users_access_info

    handler = Handler()
    example_link = "https://vk.com/club201267535?z=photo-201267535" \
                   "_457239018%2Falbum-201267535_276356863"
    owner_id = handler.get_owner_id(example_link)
    photo_id = handler.get_photo_id(example_link)
    custom_assert(owner_id, -201267535, "getting owners id")
    custom_assert(photo_id, 457239018, "getting photo id")

    login_pattern = "some@login"
    password_pattern = "somepassword"
    user_info_file = open(constants.AUTHORIZATION_INFO_FILE, 'w')
    user_info_file.write(
        login_pattern + ' ' +
        password_pattern + '\n')
    user_info_file.close()
    user_info_pattern = get_users_access_info()[0]
    custom_assert(
        user_info_pattern.login, login_pattern,
        "getting correct login"
    )
    custom_assert(
        user_info_pattern.password, password_pattern,
        "getting correct password"
    )
    sys.stderr.write("OK! All tests passed")
else:
    raise AttributeError("Nothing to import here!")
