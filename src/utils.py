import tempfile
import requests

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
    img.save(img, 'png', quality=100, optimize=True)
