from src.plugins.plugin_base import PluginBase
from src.utils import search_pictures_url
import time


class SearchAndChoosePlugin(PluginBase):
    def __init__(self, *args, **kwargs):
        subcommands = set(['choose'])
        super(SearchAndChoosePlugin, self).__init__(subcommands, *args, **kwargs)
        # TODO: thread で 0.0.0.0:10080 に web サーバを建てる

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
                number_of_picture = int(text.split()[4])
                if not number_of_picture > 0 or not number_of_picture <= 5:
                    self.outputs.append([channel, "Error for Invalid argument. Please refer to `@{} help`".format(self.bot_name)])
                    return
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
            attachments.append({
                "name": str(idx + 1),
                "text": str(idx + 1),
                "callback_id": "choose_picture",
                "image_url": path
            })
            button = {
                "name": "picture",
                "text": str(idx + 1),
                "type": "button",
                "value": path}
            actions.append(button)

        attachments.append({
            "name": "buttons",
            "text": "emoji に登録する画像を選んでください!",
            "color": "#87CEEB",
            "callback_id": "choose_picture",
            "actions": actions
        })

        self.slack_client.api_call("chat.postMessage", channel=channel, attachments=attachments)
