# xkcd to VK comic publisher

Upload xkcd comics to groups in Vkontakte

## How to install

## Installing

Download the project to your local machine.

Python3 should already be installed. 
Use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

Using virtual environment [virtualenv/venv](https://docs.python.org/3/library/venv.html) is recommended for project isolation.

Create `.env` file in root folder of the project  
Put the following variables in it:

- MEDIA_FOLDER - path to desired folder where images are saved to (and are deleted afterwards). Defaults to "images"
- VK_APP_ID - ID of your Vkontakte application (see below) 
- VK_USER_TOKEN - your user access token from VK
- VK_GROUP_ID - the group where you will post the comics

### VK app and user token

To use this project you'll need to [register a VK app](https://vk.com/editapp?act=create). Select "standalone" type of app.  
You need to set it up to be "turned on and visible to everyone" in its settings. On the same page you'll find the app's ID. If you can't find it, copy the number from the address bar of your browser.

Next, follow the [Implicit Flow procedure](https://vk.com/dev/implicit_flow_user) to procure user access token. The rights to give to the token are: `photos`, `groups`, `wall` and `offline`.

## How to use

After everything is set up, simply launch the code:
```commandline
python main.py
```

By default, script posts a random xkcd comic. You can specify a specific one with the use of the following arguments (those are mutually exclusive):

-  `--id ID` - id of comic to get
-  `-l`, `--latest` - get the latest comic

Script will upload the comic to the wall of your VK group with the comic's title and alt text as the post caption.

## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).