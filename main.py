import requests
from pathlib import Path, PurePath
import argparse
from environs import Env
from random import randint


def download_image(url, media_folder, path, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()

    Path(media_folder).mkdir(exist_ok=True, parents=True)

    with open(path, "wb") as file:
        file.write(response.content)


def get_xkcd_meta(comic_id=None):
    if comic_id:
        url = f"https://xkcd.com/{comic_id}/info.0.json"
    else:
        url = "https://xkcd.com/info.0.json"

    response = requests.get(url)
    response.raise_for_status()

    return response.json()


def get_upload_address(user_token, group_id):

    url = "https://api.vk.com/method/photos.getWallUploadServer"
    params = {
        "access_token": user_token,
        "v": "5.150",
        "group_id": group_id
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()


def upload_image(upload_url, image_path):
    with open(image_path, "rb") as image:
        url = upload_url
        files = {
            "photo": image
        }

        response = requests.post(url, files=files)
        response.raise_for_status()

        return response.json()


def save_wall_photo(user_token, group_id, upload_result):
    url = "https://api.vk.com/method/photos.saveWallPhoto"
    params = {
        "group_id": group_id,
        "access_token": user_token,
        "v": "5.150",
        "server": upload_result["server"],
        "photo": upload_result["photo"],
        "hash": upload_result["hash"],
    }

    response = requests.post(url, params=params)
    response.raise_for_status()

    return response.json()


def post_on_wall(user_token, group_id, wall_save_response, caption):
    url = "https://api.vk.com/method/wall.post"
    photo_owner = wall_save_response["owner_id"]
    photo_id = wall_save_response["id"]
    params = {
        "access_token": user_token,
        "v": "5.150",
        "attachments": f"photo{photo_owner}_{photo_id}",
        "owner_id": f"-{group_id}",
        "message": caption,
        "from_group": 1
    }

    response = requests.post(url, params=params)
    response.raise_for_status()

    return response.json()


def main():

    env = Env()
    env.read_env()
    media_folder = env.str("MEDIA_FOLDER", "images")
    vk_token = env.str("VK_USER_TOKEN")
    vk_group = env.str("VK_GROUP_ID")

    comics_number = get_xkcd_meta()["num"]
    random_id = randint(1, comics_number)
    comic_id = random_id

    comic = get_xkcd_meta(comic_id)
    comic_image_url = comic["img"]
    title = comic["title"]
    image_path = PurePath(media_folder).joinpath(f"{title}.png")
    download_image(comic_image_url, media_folder, image_path)
    alt_text = comic["alt"]

    upload_address = get_upload_address(vk_token, vk_group)["response"]["upload_url"]
    upload_response = upload_image(upload_address, image_path)
    wall_save_response = save_wall_photo(vk_token, vk_group, upload_response)["response"][0]
    message_caption = f"{title}\n{alt_text}"
    wall_post = post_on_wall(vk_token, vk_group, wall_save_response, message_caption)
    print(wall_post)
    Path(image_path).unlink()


if __name__ == '__main__':
    main()
