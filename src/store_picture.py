import time
import re
import os
import requests
from slackclient import SlackClient
from PIL import Image

from emoji_uploader import EmojiUploader


class SlackBotMain:

    workspace = os.environ["WORKSPACE"]
    email = os.environ["EMAIL"]
    password = os.environ["PASSWORD"]
    token = os.environ["SLACK_API_TOKEN"]
    channel = "team7-playground"
    sc = SlackClient(token)

    def __init__(self):
        if SlackBotMain.sc.rtm_connect():
            self.uploader = EmojiUploader(self.workspace, self.email, self.password)
            while True:
                data = SlackBotMain.sc.rtm_read()

                if len(data) > 0:
                    for item in data:
                        SlackBotMain.sc.rtm_send_message(self.channel, self.create_message(item))

                time.sleep(1)
        else:
            print("Connection Failed, invalid token?")

    def create_message(self, data):
        if "type" in data.keys():
            if data["type"] == "message":
                if 'file' in data:
                    url = data['file']['url_private']
                    filename = data['file']['title']
                    token = self.token
                    image = requests.get(url, headers={'Authorization': 'Bearer %s' % token}, stream=True)

                    if os.path.exists(filename):
                        return "<@" + data["user"] + "> " + u"Error: exists file: wait a time or rename upload file"

                    with open(filename, 'wb') as myfile:
                        for chunk in image.iter_content(chunk_size=1024):
                            myfile.write(chunk)
                    return self.resize_picture(filename)

    def resize_picture(self, filename):
        img = Image.open(filename, 'r')
        resize_img = img.resize((64, 64))
        resize_img.save(filename, 'png', quality=100, optimize=True)

        # upload
        title, _ = os.path.splitext(filename)
        self.uploader.upload(title, filename)

        os.remove(filename)

        return ":" + title + ":" + "Uploaded!"


if __name__ == '__main__':
    sbm = SlackBotMain()
