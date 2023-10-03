import requests
from pathlib import Path, PurePath
from environs import Env
from random import randint


def download_image(url, path, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()

    with open(path, "wb") as file:
        file.write(response.content)


def get_xkcd_meta(comic_id=None):
    if comic_id:
        url = f"https://xkcd.com/{comic_id}/info.0.json"
    else:
        url = "https://xkcd.com/info.0.json"

    response = requests.get(url)
    response.raise_for_status()

    meta = response.json()

    return meta["num"], meta["img"], meta["title"], meta["alt"]


def get_xkcd_num():
    url = "https://xkcd.com/info.0.json"
    response = requests.get(url)
    response.raise_for_status()

    return response.json()["num"]


def get_random_xkcd():
    comics_number = get_xkcd_num()
    comic_id = randint(1, comics_number)
    url = f"https://xkcd.com/{comic_id}/info.0.json"
    response = requests.get(url)
    response.raise_for_status()
    meta = response.json()

    return meta["img"], meta["title"], meta["alt"]


def get_upload_address(user_token, group_id, api_version):

    url = "https://api.vk.com/method/photos.getWallUploadServer"
    params = {
        "access_token": user_token,
        "v": api_version,
        "group_id": group_id
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    response_dict = response.json()
    check_vk_response(response_dict)

    return response_dict["response"]["upload_url"]


def upload_image(upload_url, image_path):
    with open(image_path, "rb") as image:
        url = upload_url
        files = {
            "photo": image
        }

        response = requests.post(url, files=files)
    response.raise_for_status()
    response_dict = response.json()
    check_vk_response(response_dict)

    return response_dict["server"], response_dict["photo"], response_dict["hash"]


def save_wall_photo(user_token, group_id, response_server, response_photo, response_hash, api_version):
    url = "https://api.vk.com/method/photos.saveWallPhoto"
    params = {
        "group_id": group_id,
        "access_token": user_token,
        "v": api_version,
        "server": response_server,
        "photo": response_photo,
        "hash": response_hash,
    }

    response = requests.post(url, params=params)
    response.raise_for_status()
    response_dict = response.json()
    check_vk_response(response_dict)

    return response_dict["response"][0]["owner_id"], response_dict["response"][0]["id"]


def post_on_wall(user_token, group_id, photo_owner, photo_id, caption, api_version):
    url = "https://api.vk.com/method/wall.post"
    params = {
        "access_token": user_token,
        "v": api_version,
        "attachments": f"photo{photo_owner}_{photo_id}",
        "owner_id": f"-{group_id}",
        "message": caption,
        "from_group": 1
    }

    response = requests.post(url, params=params)
    response.raise_for_status()
    response_dict = response.json()
    check_vk_response(response_dict)

    return response_dict


def check_vk_response(vk_response):
    if "error" in vk_response:
        error_message = vk_response["error"].get("error_msg", "Unknown error")
        error_code = vk_response["error"].get("error_code", "Unknown error code")
        raise requests.HTTPError(f"VK API responded with an error code {error_code}: {error_message}")


def main():

    env = Env()
    env.read_env()
    media_folder = env.str("MEDIA_FOLDER", "images")
    vk_token = env.str("VK_USER_TOKEN")
    vk_group = env.str("VK_GROUP_ID")
    vk_api_version = env.str("VK_API_VERSION")

    Path(media_folder).mkdir(exist_ok=True, parents=True)

    comic_image_url, title, alt_text = get_random_xkcd()
    image_path = PurePath(media_folder).joinpath(f"{title}.png")
    try:
        download_image(comic_image_url, image_path)
        upload_address = get_upload_address(vk_token, vk_group, vk_api_version)
        server, photo, vk_hash = upload_image(upload_address, image_path)
        photo_owner, photo_id = save_wall_photo(
            vk_token,
            vk_group,
            server,
            photo,
            vk_hash,
            vk_api_version,
        )
        message_caption = f"{title}\n{alt_text}"
        wall_post = post_on_wall(vk_token, vk_group, photo_owner, photo_id, message_caption, vk_api_version)
        print(wall_post)
    finally:
        Path(image_path).unlink()


if __name__ == '__main__':
    main()
