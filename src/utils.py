import re
import tempfile
import requests
import urllib.parse

from bs4 import BeautifulSoup
from PIL import Image


def download(url, headers={}):
    # ファイルをダウンロードして，そのファイルへのパスを返します
    downloaded_file = requests.get(
        url, headers=headers, stream=True)

    with tempfile.NamedTemporaryFile(delete=False) as f:
        for chunk in downloaded_file.iter_content(chunk_size=1024):
            f.write(chunk)

        return f.name


def resize_image(path):
    img = Image.open(path, 'r')
    img.thumbnail((128, 128), Image.LANCZOS)
    img.save(path, 'png', quality=100, optimize=True)


def search_picture(searchname):
    URL = "https://search.yahoo.co.jp/image/search?p={}&ei=UTF-8"
    regex = r'[^\x00-\x7F]'
    matchedList = re.findall(regex, searchname)
    for m in matchedList:
        searchname_reg = searchname.replace(m, urllib.parse.quote_plus(m, encoding="utf-8"))  # NOQA
        # TODO: uploadnameが日本語の場合失敗する
    response = requests.get(URL.format(searchname))
    if response.status_code == 404:
        raise ValueError("Error: URL page notfound.")
    html = response.text.encode("utf-8", "ignore")
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", {"id": "contents"})
    if content.find("img") is None:
        raise ValueError("検索結果が見つかりません。")
    # TODO: 検索結果を self.COUNT 個数だけ取ってきて表示 & Button 選択 (Button 受信用 Web サーバ必須)

    image_url = content.find("img")["src"]
    path = download(image_url)
    return path
