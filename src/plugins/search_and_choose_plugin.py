from src.plugins.plugin_base import PluginBase
from src.utils import search_pictures_url
import time
import unicodedata


class SearchAndChoosePlugin(PluginBase):
    def __init__(self, *args, **kwargs):
        subcommands = set(['choose'])
        super(SearchAndChoosePlugin, self).__init__(subcommands, *args, **kwargs)

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

        if len(text.split()) >= 5:
            if text.split()[4].isdigit():
                number_of_picture = unicodedata.digit(text.split()[4])
            else:
                self.outputs.append([channel, "Error for Invalid argument. Please refer to `@{} help`".format(self.bot_name)])
                return
        else:
            number_of_picture = 3

        try:
            paths = search_pictures_url(searchname, number_of_picture)
        except ValueError as e:
            self.outputs.append([channel, str(e)])
            return

        attachments = []
        actions = []
        for idx, path in enumerate(paths):
            #self.slack_client.api_call("chat.postMessage", channel=channel, text=path)
            attachments.append({
                "name": str(idx + 1),
                "text": str(idx + 1),
                "image_url": path
            })
            button = {
                "name": "picture",
                "text": str(idx + 1),
                "type": "button",
                "value": path}
            actions.append(button)

        attachments.append({
            "text": "emoji に登録する画像を選んでください!",
            "actions": actions
        })

        self.slack_client.api_call("chat.postMessage", channel=channel, callback_id="choose_picture", attachment_type="default", attachments=attachments)
