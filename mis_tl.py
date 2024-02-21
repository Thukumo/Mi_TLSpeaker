import asyncio, json, websockets, yomiage, signal, os, time

async def get_note(token):
    global stop, timestart
    async with websockets.connect(r"wss://misskey.io/streaming?i="+token) as websocket:
    #async with websockets.connect(r"ws://localhost:8765") as websocket: テスト用
        json_data = {
            "type": "connect",
            "body": {
                "channel": "localTimeline",
                "id": "local_tl"
            }
        }
        await websocket.send(json.dumps(json_data))
        while True:
            if 60 < time.perf_counter() - timestart and False:
                print("")
                print("")
                print("60秒ごとの再接続を行っています。")
                print("")
                print("")
                return
            try:
                recv_text = json.loads(await websocket.recv())["body"]["body"]["text"]
            except ValueError:
                continue
            if recv_text != None:
                if len(recv_text) <= 140:
                    if not stop:
                        print(recv_text)
                        try:
                            yomiage.speak(recv_text)
                        except:
                            break
                    else:
                        return

def exitter(hoge, fuga):
    global stop
    stop = True
    print("")
    print("A.I.VIOCE Editorとの接続を終了中...")
    print("現在のノートの再生が停止するまで待機しています")
    yomiage.disconnect()
    print("終了しました。")
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    os._exit(0)


stop = False
try:
    with open("token.json", "r") as f:
        token = json.load(f)
        token = token["token"]
        if(len(token)) == 0:
            print("token.jsonにトークンが設定されていません。")
            print("get_misskey_APIKey.pyを実行するか、Misskeyの設定画面からトークンを取得して保存してください。")
            exit()
except FileNotFoundError:
    print("token.jsonが存在しません。")
    print("get_misskey_APIKey.pyを実行するか、Misskeyの設定画面からトークンを取得して保存してください。")
    exit()

signal.signal(signal.SIGINT, exitter)
timestart = time.perf_counter()
yomiage.connect()
"""
yomiageの説明
yomiage.connect()を実行した際に設定(テキストに入力されていた文字列、カーソル位置など含む)は保存され、
yomiage.disconnect()を実行した際に復元される。
for i in yomiage.voice_lis()
   print(i) 使用できるボイロの名前一覧を確認
yomiage.set_voice("琴葉 葵（蕾）") 名前で読み上げてもらうボイロを指定
yomiage.get_mc()マスターコントロールの値を取得
yomiage.set_mc("SentencePause", 200) マスターコントロールの値を変更(例として文末ポーズの値を200ミリ秒にしてる)
yomiage.set_mc("Speed", 1.5) 速度を変更(例として1.5倍にする)
yomiage.connect()を実行した際に、マスターコントロールのSentencePauseに200, PitchRangeに1.44, Speedに1.44が設定され、
ボイスは"琴葉 葵"に設定される。
"""
while not stop:
    try:
        asyncio.get_event_loop().run_until_complete(get_note(token))
    except websockets.exceptions.ConnectionClosedError:
        print("!接続が切れました。再接続します。")
        yomiage.speak("接続が切れたから再接続するよ。")
    timestart = time.perf_counter()
