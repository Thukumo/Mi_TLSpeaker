[![SUSHI-WARE LICENSE](https://img.shields.io/badge/license-SUSHI--WARE%F0%9F%8D%A3-blue.svg)](https://github.com/MakeNowJust/sushi-ware)
# Mi_TLSpeaker
Misskey.ioのローカルタイムラインを琴葉葵ちゃんに読み上げてもらうPythonスクリプト<br>
現在はA.I.VOICEのみの対応ですが、そのうちVOICEVOXに対応する...かも
# 導入
まず、このリポジトリをクローンしたディレクトリでターミナルを開いてください。
```
pip install -r requirements.txt
python get_misskey_APIKey.py
```
を実行します。ブラウザで、アカウントへのアクセスの許可について聞かれたらはいと答えてください。<br>
その後ターミナルに戻ってエンターキーを押してください。<br>
"トークンを保存しました。"と表示されれば成功です。
# 実行方法
```
python mis_tl.py
```
を実行してください。設定等を変えたい場合はmis_tl.pyの中身を書き換えてください。<br>
終了時は必ずCtrl+Cで終了するようにしてください。<br>
また、現在のところ数分ごとにwebsocketの接続が切断されます。(自動で再接続される)
# その他
yomiage.pyはA.I.VOICEをPythonから使用するためのライブラリとして使うことができます。<br>
仕様などはmis_tl.pyに書かれた説明とyomiage.pyを読んで理解してください。
