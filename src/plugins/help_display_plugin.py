from src.plugins.plugin_base import PluginBase

HELP_MESSAGE = '''
> `@{0} upload hoge`\n
アップロードされたファイルを hoge という名前で emoji に登録します。\n
ファイルアップロード時の [Upload a file?] の画面にて Add Comment に記述してください。\n
> `@{0} url http://example.com/hoge.jpg [fuga]`\n
http://example.com/fuga.jpg にある画像データを hoge という名前、またはエイリアス指定がある場合 fuga という名前で emoji に登録します。\n
> `@{0} search hoge [fuga]`\n
Yahoo!検索(画像) にて hoge を検索し、検索結果の一番目を hoge という名前、またはエイリアス指定がある場合 fuga という名前で emoji に登録します。\n
> `@{0} choose hoge [fuga] [NUMBER]`\n
Yahoo!検索(画像) にて hoge を検索し、NUMBER の数 (1 から 5 までの整数値、デフォルト 3) だけ検索結果とボタンを表示します。\n
ユーザが押したボタンに対応する画像を hoge という名前、またはエイリアス指定がある場合 fuga という名前で emoji に登録します。\n
> `@{0} help`\n
Slack 上に help メッセージを表示します。\n
'''


def output_help(bot_name):
    return HELP_MESSAGE.format(bot_name)


class HelpDisplayPlugin(PluginBase):
    def __init__(self, *args, **kwargs):
        subcommands = set(['help'])
        super(HelpDisplayPlugin, self).__init__(subcommands, *args, **kwargs)

    def process_filtered_massage(self, data):
        channel = data['channel']
        self.outputs.append([channel, output_help(self.bot_name)])
