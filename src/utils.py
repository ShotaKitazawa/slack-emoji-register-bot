import re
import tempfile
import requests
import urllib.parse

from bs4 import BeautifulSoup
from PIL import Image


def search(searchname):
    URL = "https://search.yahoo.co.jp/image/search?p={}&ei=UTF-8"
    regex = r'[^\x00-\x7F]'
    matchedList = re.findall(regex, searchname)
    for m in matchedList:
        searchname_reg = searchname.replace(m, urllib.parse.quote_plus(m, encoding="utf-8"))  # NOQA

    response = requests.get(URL.format(searchname))
    if response.status_code == 404:
        raise ValueError("Error: URL page notfound.")

    html = response.text.encode("utf-8", "ignore")
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", {"id": "contents"})

    if content.find("img") is None:
        raise ValueError("検索結果が見つかりません。")

    return content


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


def search_and_download_picture(searchname):
    content = search(searchname)
    image_url = content.find("img")["src"]
    path = download(image_url)
    return path


def search_pictures_url(searchname, number):
    content = search(searchname)
    image_urls = list(map(lambda x: x["src"], content.find_all("img")[:number]))
    return image_urls
