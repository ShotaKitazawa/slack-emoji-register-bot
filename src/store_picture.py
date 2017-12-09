import time
import os
import requests
from slackclient import SlackClient
from PIL import Image

from .emoji_uploader import EmojiUploader


class SlackBotMain:

    def __init__(self):
        self.workspace = os.environ["WORKSPACE"]
        self.email = os.environ["EMAIL"]
        self.password = os.environ["PASSWORD"]
        self.token = os.environ["SLACK_API_TOKEN"]
        self.sc = SlackClient(self.token)
        self.uploader = EmojiUploader(
            self.workspace, self.email, self.password)
        self.bot_id = self.sc.api_call('auth.test')['user_id']

    def run(self):
        if not self.sc.rtm_connect():
            print("Connection Failed, invalid token?")
            exit(1)

        while True:
            data_list = self.sc.rtm_read()

            for data in data_list:
                if 'type' not in data:
                    continue
                if data['type'] != 'message':
                    continue

                text = data['text']
                channel = data['channel']
                if text.startswith('<@{}>'.format(self.bot_id)):
                    # botへのメンション
                    pass
                else:
                    self.sc.rtm_send_message(
                        channel, self.create_message(data))

            time.sleep(1)

    def create_message(self, data):
        if 'file' in data:
            url = data['file']['url_private']
            filename = data['file']['title']
            token = self.token
            image = requests.get(
                url, headers={'Authorization': 'Bearer %s' % token},
                stream=True)

            if os.path.exists(filename):
                return ("<@{}> Error: exists file: "
                        "wait a time or rename upload file").format(
                    data['user'])

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
        try:
            self.uploader.upload(title, filename)
        except ValueError as e:
            return str(e)
        finally:
            os.remove(filename)

        return ':{}: を登録しました!'.format(title)


if __name__ == '__main__':
    sbm = SlackBotMain()
    sbm.run()
