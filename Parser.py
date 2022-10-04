import vk_api as vk
import asyncio

# все дополнительные поля для метода users.get
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


async def get_user_info_by_id_async(token: str, id: int, fields: str = None) -> list[dict]:
    try:
        vk_session = vk.VkApi(token=token).method(method='users.get', values={
            'user_id': id,
            'fields': fields,
            'v': 5.194
        })
        return vk_session
    except:
        return []


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
            'v': 5.194
        })
        return vk_session
    except:
        return [{}]


async def get_user_friends_id_async(token: str, id: int) -> list[int]:
    try:
        vk_session = vk.VkApi(token=token).method(method='friends.get', values={
            'user_id': id,
            'v': 5.194
        })
        return vk_session['items']
    except:
        return []


def get_count_photos(user_info) -> int:
    try:
        count_photos = user_info[0]['counters']['photos']
        return count_photos
    except:
        return 0


def async_parse(tokens_path: str, id_path: str, min_count_photos: int) -> None:
    with open(tokens_path, 'r', encoding='UTF-8') as tokens_file, \
            open(id_path, 'r', encoding='UTF-8') as id_file, \
            open('result_pars.txt', 'w+', encoding='UTF-8') as result_file:  # Создал файл для записи итогов

        tokens_list = tokens_file.readlines()  # Записал токены в массив
        id_list = id_file.readlines()  # Записал id в массив

        # прошёлся по всем пользователям и записал ифнормацию о них в итоговый файл
        info_about_users_from_file = get_users_info_by_ids(tokens_list[0], id_list, all_fields)  # использую первый
        # токен, потому что выполняю единоразово, рассинхронить это не имеет большого смысла
        for info in info_about_users_from_file:
            result_file.write(str(info) + '\n')

        # прошёлся по всем друзьям пользователя и выбрал те, у которых количество фотографий больше N
        ids_correct_friends = []  # массив id друзей, у которых больше N фоток
        friends_ids_lists = asyncio.run(go_on_users(tokens_list, id_list))  # Список, состоящий из списков id друзей
        # пользователей
        friends_ids_list = []  # Общий список id друзей пользователей
        for i in friends_ids_lists:
            friends_ids_list.extend(i)
        friends_info = asyncio.run(go_on_friends(tokens_list, friends_ids_list))  # информация о друзьях
        for friend_info in friends_info:
            if get_count_photos(friend_info) > min_count_photos:
                string_friend_id = str(friend_info[0]['id'])
                ids_correct_friends.append(string_friend_id)

        # прошёлся по всем подходящим друзьям и записал информацию о них в итоговый файл
        ids_correct_friends = list(set(ids_correct_friends))  # id уникальных друзей, у которых больше N фоток
        info_about_correct_friends = get_users_info_by_ids(tokens_list[0], ids_correct_friends, all_fields)
        # информация о подходящих друзьях. Использую первый токен, потому что запрос выполняется всего 1 раз
        for info in info_about_correct_friends:
            result_file.write(str(info) + '\n')


# Асинхронный проход по друзьям
async def go_on_friends(tokens_list, friends_ids_list):
    tasks = []

    for counter_of_id in range(0, len(friends_ids_list), len(tokens_list)):
        for token_i in range(0, len(tokens_list)):
            if (counter_of_id + token_i) < len(friends_ids_list):
                task = asyncio.create_task(get_user_info_by_id_async(tokens_list[token_i],
                                                                     friends_ids_list[counter_of_id + token_i],
                                                                     'counters'))
                tasks.append(task)
    return await asyncio.gather(*tasks)


# асинхронный проход по пользователям, возвращает список со списками id друзей пользователя
async def go_on_users(token_list, id_list):
    tasks = []
    for counter_of_id in range(0, len(id_list), len(token_list)):
        for token_i in range(0, len(token_list)):
            if (counter_of_id + token_i) < len(id_list):
                task = asyncio.create_task(get_user_friends_id_async(token_list[token_i],
                                                                     int(id_list[counter_of_id + token_i].rstrip(
                                                                         '\n'))))
                tasks.append(task)
    return await asyncio.gather(*tasks)
