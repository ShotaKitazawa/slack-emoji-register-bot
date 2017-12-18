import tempfile
import requests


def download(url, headers={}):
    # ファイルをダウンロードして，そのファイルへのパスを返します
    downloaded_file = requests.get(
        url, headers=headers, stream=True)

    with tempfile.NamedTemporaryFile(delete=False) as f:
        for chunk in downloaded_file.iter_content(chunk_size=1024):
            f.write(chunk)

        return f.name
