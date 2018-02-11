from src.plugins.plugin_base import PluginBase
from src.utils import search_and_download_picture


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

        if len(text.split()) >= 4:
            emoji_name = text.split()[3]
        else:
            emoji_name = searchname

        try:
            path = search_and_download_picture(searchname)
        except ValueError as e:
            self.outputs.append([channel, str(e)])
            return

        self.upload_emoji(channel, path, emoji_name)
