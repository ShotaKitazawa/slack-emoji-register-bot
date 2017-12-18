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
        def match(text):
            at_str = '<@{}>'.format(self.bot_id)
            if not text.startswith(at_str):
                return False

            text = text.strip().split()
            if len(text) < 2:
                return False

            if text[1] not in self.subcommands:
                return False

            return True

        from pprint import pprint
        pprint(data)
        if 'text' in data and match(data['text']):
            self.process_filtered_massage(data)
            return

        if 'file' in data and 'initial_comment' in data['file'] and \
                'comment' in data['file']['initial_comment']:
            comment = data['file']['initial_comment']['comment']
            if match(comment):
                self.process_filtered_massage(data)

    def process_filtered_massage(self, data):
        raise NotImplementedError()

    def send_register_message(self, channel, emoji_name):
        self.outputs.append([channel, ':{}: を登録しました!'.format(emoji_name)])
