import os
import imghdr
import tempfile
import zipfile


from src.plugins.plugin_base import PluginBase
from src.download import download


class FileUploadPlugin(PluginBase):
    def __init__(self, *args, **kwargs):
        subcommands = set(['upload'])
        super(FileUploadPlugin, self).__init__(subcommands, *args, **kwargs)

    def process_filtered_massage(self, data):
        channel = data['channel']

        if 'file' not in data:
            self.outputs.append([channel, 'ファイルが添付されていません'])
            return

        url = data['file']['url_private']
        filename = data['file']['title']
        headers = {'Authorization': 'Bearer {}'.format(self.token)}
        path = download(url, headers=headers)

        targets = []
        if filename.endswith('.zip'):
            temp_dir = tempfile.mkdtemp()
            with zipfile.ZipFile(path) as zf:
                zf.extractall(temp_dir)

            for fname in os.listdir(temp_dir):
                path = os.path.join(temp_dir, fname)
                if imghdr.what(path) is not None:
                    targets.append((filename, path))

        elif imghdr.what(path) is not None:
            targets.append((filename, path))

        if not targets:
            self.outputs.append([channel, 'アップロードされたファイルの形式に対応していません'])
            return

        for filename, path in targets:
            emoji_name, _ = os.path.splitext(os.path.basename(filename))

            self.slack_emoji.upload(emoji_name, path)
            self.send_register_message(channel, emoji_name)
