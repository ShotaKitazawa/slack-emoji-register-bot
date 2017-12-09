import time
import os
import zipfile
import requests
import imghdr
from logzero import logger
from bs4 import BeautifulSoup
from slackclient import SlackClient
from PIL import Image

from .emoji_uploader import EmojiUploader


def is_image_file(filename):
    return filename.endswith(('png', 'jpeg', 'jpg', 'gif'))


def extractall_zip(filename):
    ret = []
    dir_name = os.path.splitext(filename)[0]
    dir_name = os.path.join('/tmp', dir_name)

    with zipfile.ZipFile(filename) as zf:
        zf.extractall('/tmp')

    for fname in os.listdir(dir_name):
        fname = os.path.join(dir_name, fname)
        if fname.startswith('__MACOSX'):
            continue
        if not is_image_file(fname):
            continue
        logger.info('ok fname = {}'.format(fname))
        ret.append(fname)

    return ret


class SlackBotMain:
    url = "https://search.yahoo.co.jp/image/search?p={}&ei=UTF-8"
    count = 3

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
            logger.info("Connection Failed, invalid token?")
            exit(1)

        while True:
            data_list = self.sc.rtm_read()

            for data in data_list:
                if 'type' not in data:
                    continue
                if data['type'] != 'message':
                    continue

                text = data['text'].strip()
                channel = data['channel']
                user = data['user']
                at_str = '<@{}> '.format(self.bot_id)

                if text.startswith(at_str):
                    if text.startswith(at_str + 'search '):
                        if len(text.split()) < 3:
                            self.sc.rtm_send_message(channel, 'url を指定してください')
                            continue
                        msg = self.download_img_and_upload_emoji(
                            text.split()[2])
                        self.sc.rtm_send_message(channel, msg)
                    if text.startswith(at_str + 'url'):
                        if len(text.split()) < 3:
                            self.sc.rtm_send_message(channel, 'url を指定してください')
                            continue
                        url = text.split()[2]
                        url = url[1:-1]
                        if len(text.split()) == 4:
                            filename = text.split()[3]
                        else:
                            filename = os.path.basename(url)
                        self.download(url, filename, user)
                        msg = self.create_message(filename)
                        self.sc.rtm_send_message(channel, msg)

                else:
                    if 'file' in data:
                        url = data['file']['url_private']
                        filename = data['file']['title']
                        headers = {'Authorization': 'Bearer %s' % self.token}

                        logger.info('receive filename = {}'.format(filename))

                        self.download(url, filename, user, headers=headers)
                        if filename.endswith('.zip'):
                            fnames = extractall_zip(filename)
                            for fname in fnames:
                                msg = self.create_message(fname)
                                self.sc.rtm_send_message(channel, msg)
                        else:
                            msg = self.create_message(filename)
                            self.sc.rtm_send_message(channel, msg)

            time.sleep(1)

    def download(self, url, filename, user, headers={}):
        image = requests.get(
            url, headers=headers,
            stream=True)

        if os.path.exists(filename):
            return ("<@{}> Error: exists file: "
                    "wait a time or rename upload file").format(user)

        with open(filename, 'wb') as myfile:
            for chunk in image.iter_content(chunk_size=1024):
                myfile.write(chunk)

        return filename

    def create_message(self, filename):
        logger.info('uploading {}'.format(filename))
        return self.resize_picture(filename)

    def resize_picture(self, filename):
        img = Image.open(filename, 'r')
        # resize_img = img.resize((64, 64))
        # 縦横の比率を維持したままresize
        img.thumbnail((64, 64), Image.LANCZOS)
        resize_img = img
        resize_img.save(filename, 'png', quality=100, optimize=True)

        # upload
        title, _ = os.path.splitext(os.path.basename(filename))
        try:
            self.uploader.upload(title, filename)
        except ValueError as e:
            return str(e)
        finally:
            os.remove(filename)

        return ':{}: を登録しました!'.format(title)

    def download_img_and_upload_emoji(self, title):
        response = requests.get(self.url.format(title))
        if response.status_code == 404:
            return 'Error: URL page notfound.'
        html = response.text.encode("utf-8", "ignore")
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find("div", {"id": "contents"})
        image_url = content.find("img")["src"]
        image = requests.get(image_url)
        with open("tmp", 'wb') as myfile:
            for chunk in image.iter_content(chunk_size=1024):
                myfile.write(chunk)

        # title ファイルの形式判別
        extend = imghdr.what("tmp")
        os.rename("tmp", title + "." + extend)

        return self.resize_picture(title + "." + extend)


if __name__ == '__main__':
    sbm = SlackBotMain()
    sbm.run()
