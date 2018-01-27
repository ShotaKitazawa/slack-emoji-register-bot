# 概要

画像を emoji に変換する Slack Bot です。

# 環境

- Python 3.x

# 実行

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
_EOF_
```

実行します。

```
rtmbot
```

## Dockerfile からの実行

イメージを build します

```
docker build . -t slack-emoji-bot
```

実行します。

```
docker run -e WORKSPACE=hoge -e EMAIL=hoge -e PASSWORD=hoge -e SLACK_TOKEN=hoge -itd slack-emoji-bot
```

## Docker Compose での実行

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

- @bot upload hoge
    - アップロードされたファイルを :hoge: という名前で emoji に登録します。
        - ファイルアップロード時の [Upload a file?] の画面にて Add Comment に `@bot upload hoge` を入力
        - zip ファイルにも対応
- @bot url http://example.com/huga.jpg hoge
    - http://example.com/huga.jpg にある画像データを :hoge: という名前で emoji に登録します。
- @bot search hoge
    - Yahoo!検索(画像) にて hoge を検索し、検索結果の一番目を :hoge: という名前で emoji に登録します。
- @bot search hoge huga
    - Yahoo!検索(画像) にて hoge を検索し、検索結果の一番目を :huga: という名前で emoji に登録します。
