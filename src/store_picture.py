# coding:utf-8

import time
import re
import os
import requests
from slackclient import SlackClient


class SlackBotMain:

    token = os.environ["SLACK_API_TOKEN"]
    sc = SlackClient(token)

    def __init__(self):
        if SlackBotMain.sc.rtm_connect():
            while True:
                data = SlackBotMain.sc.rtm_read()

                if len(data) > 0:
                    for item in data:
                        SlackBotMain.sc.rtm_send_message("team7-playground", self.create_message(item))

                time.sleep(1)
        else:
            print("Connection Failed, invalid token?")

    def create_message(self, data):
        if "type" in data.keys():
            if data["type"] == "message":
                self.img(data)
                return "<@" + data["user"] + "> " + u"test:wink:"

    def img(self, data):
        if 'file' in data:
            url = data['file']['url_private']
            title, _ = os.path.splitext(data['file']['title'])
            flag = data['file']['filetype']

            token = self.token
            image = requests.get(url, headers={'Authorization': 'Bearer %s' % token}, stream=True)

            with open(title + "." + flag, 'wb') as myfile:
                for chunk in image.iter_content(chunk_size=1024):
                    myfile.write(chunk)
            print("store!")


sbm = SlackBotMain()
