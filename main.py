import requests
from pathlib import Path, PurePath
import argparse
from environs import Env


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

    comic = get_xkcd_meta(args.id)
    comic_image_url = comic["img"]
    title = comic["title"]
    path = PurePath(media_folder).joinpath(f"{title}.png")
    download_image(comic_image_url, media_folder, path)
    print(comic["alt"])


if __name__ == '__main__':
    main()
