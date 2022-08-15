import sys
from test_utils import custom_assert
from Handler import Handler

if __name__ == "__main__":
    handler = Handler()
    example_link = "https://vk.com/club201267535?z=photo-201267535" \
                   "_457239018%2Falbum-201267535_276356863"
    owner_id = handler.get_owner_id(example_link)
    custom_assert(owner_id, -201267535, "getting owners id")
    custom_assert(owner_id, 457239018, "getting photo id")
    sys.stderr.write("OK! All tests passed")
