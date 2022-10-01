import vk_api as vk

string_token = "vk1.a.NjumBvUZXE1Gj2vhN0R1Pe37brn8C22" \
               "HGORaBA7TndKwtUeJFcleN1vFw8hXrrj1dQmUETByyr" \
               "lygHbBWi87mT3PiGtFGJQpEW4pd881bUjAv5Y8Hft2w" \
               "Y_LH_QxFf8XYzNOv74WWJg9HG0Y8P8hTyLLqkNcVucaFjKj9M_XAaSPMF9dOkefJOk8X3UpolH-"
all_fields = "activities, about, blacklisted, blacklisted_by_me, books," \
             " bdate, can_be_invited_group, can_post, can_see_all_posts," \
             "can_see_audio, can_send_friend_request, can_write_private_message," \
             " career, common_count, connections, contacts, city, country, crop_photo," \
             " domain, education, exports, followers_count, friend_status, has_photo, has_mobile," \
             " home_town, photo_100, photo_200, photo_200_orig, photo_400_orig, photo_50, sex, site," \
             " schools, screen_name, status, verified, games, interests, is_favorite, is_friend," \
             " is_hidden_from_feed, last_seen, maiden_name, military, movies, music, nickname, occupation," \
             " online, personal, photo_id, photo_max," \
             " photo_max_orig, quotes, relation, relatives, timezone, tv, universities, counters"


def get_user_info_by_id(token: str, id: int, fields: str = None):
    vk_session = vk.VkApi(token=token).method(method='users.get', values={
        'user_id': id,
        'fields': fields,
    })
    return vk_session


def get_users_info_by_ids(token: str, ids: list[str], fields: str = None) -> list[dict]:
    string_ids = ''
    for i in range(len(ids)):
        if i < len(ids) - 1:
            string_ids += f'{ids[i]}, '
        else:
            string_ids += ids[i]
    try:
        vk_session = vk.VkApi(token=token).method(method='users.get', values={
            'user_id': string_ids,
            'fields': fields,
        })
        return vk_session
    except:
        return [{}]


def get_user_friends_id(token: str, id: int) -> list[int]:
    vk_session = vk.VkApi(token=token).method(method='friends.get', values={
        'user_id': id
    })
    return vk_session['items']


def get_count_photos(user_info) -> int:
    try:
        count_photos = user_info[0]['counters']['photos']
        return count_photos
    except:
        return 0


def parse(tokens_path: str, id_path: str, N: int) -> None:
    tokens_file = open(tokens_path, 'r', encoding='UTF-8')  # Считал все токены
    id_file = open(id_path, 'r', encoding='UTF-8')  # Считал все id
    result_file = open('result.txt', 'w+', encoding='UTF-8')  # Создал файл для записи итогов
    try:
        tokens_list = tokens_file.readlines()  # Записал токены в массив
        id_list = id_file.readlines()  # Записал id в массив
        ids_correct_friends = []  # массив id друзей, у которых больше N фоток
        # прошёлся по всем пользователям и записал ифнормацию о них в итоговый файл
        info_about_users_from_file = get_users_info_by_ids(tokens_list[0], id_list, all_fields)
        for info in info_about_users_from_file:
            result_file.write(str(info) + '\n')
            # прошёлся по всем друзьям пользователя и выбрал те, у которых количество фотографий больше N
            for friend_id in get_user_friends_id(tokens_list[0], info['id']):
                friend_info = get_user_info_by_id(tokens_list[0], friend_id, 'counters')
                if get_count_photos(friend_info) > N:
                    string_friend_id = str(friend_id)
                    ids_correct_friends.append(string_friend_id)
        # прошёлся по всем подходящим друзьям и записал информацию о них в итоговый файл
        info_about_correct_friends = get_users_info_by_ids(tokens_list[0], ids_correct_friends, all_fields)
        for info in info_about_correct_friends:
            result_file.write(str(info) + '\n')

    finally:
        tokens_file.close()
        id_file.close()
        result_file.close()