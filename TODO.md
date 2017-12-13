# TODO

- help サブコマンドの実装
- delete サブコマンドの実装
    - `@mention delete test` で :test: を削除
- search サブコマンドの検索結果を emoji 化するか Button の yes/no で決定
    - 検索結果上位3件表示とかも
- 引数が足りない場合のエラーメッセージ表示
    - 例: `@mention search 日本語` ときたら第4引数にアルファベットで登録名が必要
        - Slack は日本語で emoji を登録できないため
- リファクタリング
