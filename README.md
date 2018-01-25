# 概要

画像を emoji に変換する Slack Bot です。

# 環境

- Python 3.x

# 使用方法

必要なライブラリをインストールします。

```
pip install -r requirements.txt
```

環境変数を設定します。

```
export WORKSPACE=ワークスペース名
export EMAIL=ワークスペースに所属するユーザのメールアドレス
export PASSWORD=EMAILに対応するパスワード
export SLACK_TOKEN=トークン
```

設定ファイルを作成します。

```
cat << _EOF_ > rtmbot.conf
DEBUG: True
SLACK_TOKEN: $SLACK_TOKEN
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
