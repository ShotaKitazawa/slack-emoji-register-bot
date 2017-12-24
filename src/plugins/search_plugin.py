import os

from src.plugins.plugin_base import PluginBase
from src.utils import search_picture, resize_image


class SearchPlugin(PluginBase):
    def __init__(self, *args, **kwargs):
        subcommands = set(['search'])
        super(SearchPlugin, self).__init__(subcommands, *args, **kwargs)

    def process_filtered_massage(self, data):
        channel = data['channel']
        text = data['text'].strip()

        if len(text.split()) < 3:
            self.outputs.append([channel, '検索単語を指定してください'])
            return

        searchname = text.split()[2]

        if len(text.split()) == 4:
            emoji_name = text.split()[3]
        else:
            emoji_name = searchname

        try:
            path = search_picture(searchname)
        except ValueError as e:
            self.outputs.append([channel, str(e)])
            return

        resize_image(path)
        try:
            self.slack_emoji.upload(emoji_name, path)
            self.send_register_message(channel, emoji_name)
        except ValueError as e:
            self.outputs.append([channel, str(e)])
        finally:
            os.remove(path)
