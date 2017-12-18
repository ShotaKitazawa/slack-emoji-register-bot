import os

from rtmbot.core import Plugin

from src.slack_emoji import SlackEmoji


class PluginBase(Plugin):
    workspace = os.environ["WORKSPACE"]
    email = os.environ["EMAIL"]
    password = os.environ["PASSWORD"]
    slack_emoji = SlackEmoji(workspace, email, password)

    token = os.environ["SLACK_TOKEN"]

    def __init__(self, subcommands, *args, **kwargs):
        super(PluginBase, self).__init__(*args, **kwargs)
        self.subcommands = subcommands
        self.bot_id = self.slack_client.api_call('auth.test')['user_id']

    def process_message(self, data):
        if 'text' not in data:
            return

        text = data['text']
        if not text.startswith('<@{}>'.format(self.bot_id)):
            return

        text = text.strip().split()
        if len(text) < 2:
            return

        if text[1] not in self.subcommands:
            return

        self.process_filtered_massage(data)

    def process_filtered_massage(self, data):
        raise NotImplementedError()

    def send_register_message(self, channel, emoji_name):
        self.outputs.append([channel, ':{}: を登録しました!'.format(emoji_name)])
