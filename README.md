# 概要

画像を emoji に変換する Slack Bot です。

# 環境

- Python 3.6.1

# 実行

# ローカル環境での実行

環境変数を設定します。

```
export WORKSPACE=ワークスペース名
export EMAIL=ワークスペースに所属するユーザのメールアドレス
export PASSWORD=EMAILに対応するパスワード
export SLACK_TOKEN=トークン
```

必要なライブラリをインストールします。

```
pip install -r requirements.txt
```

設定ファイルを作成します。

```
cat << _EOF_ > rtmbot.conf
DEBUG: True
SLACK_TOKEN: "$SLACK_TOKEN"
ACTIVE_PLUGINS:
    - src.plugins.FileUploadPlugin
    - src.plugins.URLUploadPlugin
    - src.plugins.SearchPlugin
    - src.plugins.HelpDisplayPlugin
_EOF_
```

実行します。

```
rtmbot
```

## Dockerfile での実行

環境変数を設定します。

```
export WORKSPACE=ワークスペース名
export EMAIL=ワークスペースに所属するユーザのメールアドレス
export PASSWORD=EMAILに対応するパスワード
export SLACK_TOKEN=トークン
```

イメージを build します

```
docker build . -t slack-emoji-bot
```

実行します。

```
docker run -e WORKSPACE=hoge -e EMAIL=hoge -e PASSWORD=hoge -e SLACK_TOKEN=hoge -itd slack-emoji-bot
```

## Docker Compose での実行

環境変数を設定します。

```
export WORKSPACE=ワークスペース名
export EMAIL=ワークスペースに所属するユーザのメールアドレス
export PASSWORD=EMAILに対応するパスワード
export SLACK_TOKEN=トークン
```

イメージを build します。

```
docker-compose build
```

実行します。

```
docker-compose up -d
```

## 使用方法

Slack 上でメンションを送ることで各機能を使用可能です。

- `@bot upload hoge`
    - アップロードされたファイルを hoge という名前で emoji に登録します。
        - ファイルアップロード時の [Upload a file?] の画面にて Add Comment に記述してください
        - zip ファイルにも対応しています
- `@bot url http://example.com/hoge.jpg [fuga]`
    - http://example.com/fuga.jpg にある画像データを hoge という名前、またはエイリアス指定がある場合 fuga という名前で emoji に登録します。
- `@bot search hoge [fuga]`
    - Yahoo!検索(画像) にて hoge を検索し、検索結果の一番目を hoge という名前、またはエイリアス指定がある場合 fuga という名前で emoji に登録します。
- `@{0} choose hoge [fuga] [NUMBER]`
    - Yahoo!検索(画像) にて hoge を検索し、NUMBER の数 (デフォルト 3 つ) だけ検索結果とボタンを表示します。
    - ユーザが押したボタンに対応する画像を hoge という名前、またはエイリアス指定がある場合 fuga という名前で emoji に登録します。
- `@bot help`
    - Slack 上に help メッセージを表示します。

