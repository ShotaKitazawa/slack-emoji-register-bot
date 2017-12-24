import os
import imghdr

from src.plugins.plugin_base import PluginBase
from src.utils import download, resize_image


class URLUploadPlugin(PluginBase):
    def __init__(self, *args, **kwargs):
        subcommands = set(['url'])
        super(URLUploadPlugin, self).__init__(subcommands, *args, **kwargs)

    def process_filtered_massage(self, data):
        channel = data['channel']
        text = data['text'].strip()

        if len(text.split()) < 3:
            self.outputs.append([channel, 'url を指定してください'])
            return

        url = text.split()[2]
        # <url> でメッセージが来るので <> を削除
        url = url[1:-1]
        if len(text.split()) > 3:
            emoji_name = text.split()[3]
        else:
            emoji_name, _ = os.path.splitext(os.path.basename(url))

        emoji_name = emoji_name.lower()
        path = download(url)

        if imghdr.what(path) is None:
            self.outputs.append([channel, '画像URLを指定してください'])
            return

        resize_image(path)
        try:
            self.slack_emoji.upload(emoji_name, path)
            self.send_register_message(channel, emoji_name)
        except ValueError as e:
            self.outputs.append([channel, str(e)])
        finally:
            os.remove(path)
