import sys
from test_utils import custom_assert
from main import get_owners_id
from main import get_photos_id

if __name__ == "__main__":
    example_link = "https://vk.com/club201267535?z=photo-201267535" \
                   "_457239018%2Falbum-201267535_276356863"
    custom_assert(get_owners_id(example_link), -201267535, "getting owners id")
    custom_assert(get_photos_id(example_link), 457239018, "getting photo id")
    sys.stderr.write("OK! All tests passed")
