import os
import imghdr
from bs4 import BeautifulSoup
import requests

from emoji_uploader import EmojiUploader


class Download:

    def __init__(self, uploader):
        self.uploader = uploader

if __name__ == '__main__':

    uploader = EmojiUploader(os.environ["WORKSPACE"], os.environ["EMAIL"], os.environ["PASSWORD"]).upload
    a = Download(uploader)
    a.download_img_and_upload_emoji("testtttttttttttttttttto")
