import requests
from pathlib import Path, PurePath
import argparse
from environs import Env
from pprint import pprint


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


def get_group_info(user_token):
    url = f"https://api.vk.com/method/groups.get"
    params = {
        "access_token": user_token,
        "v": "5.150"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()


def get_upload_address(user_token, group_id):

    url = f"https://api.vk.com/method/photos.getWallUploadServer"
    params = {
        "access_token": user_token,
        "v": "5.150",
        "group_id": group_id
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--id",
        help="id of comic to get",
        type=int
    )

    args = parser.parse_args()

    env = Env()
    env.read_env()
    media_folder = env.str("MEDIA_FOLDER")
    vk_token = env.str("VK_USER_TOKEN")
    vk_group = env.str("VK_GROUP_ID")

    # comic = get_xkcd_meta(args.id)
    # comic_image_url = comic["img"]
    # title = comic["title"]
    # path = PurePath(media_folder).joinpath(f"{title}.png")
    # download_image(comic_image_url, media_folder, path)
    # print(comic["alt"])

    server = get_upload_address(vk_token, vk_group)
    pprint(server)


if __name__ == '__main__':
    main()
