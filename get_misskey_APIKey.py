import requests, json, uuid, webbrowser
from time import sleep

try:
    hoge = json.load(open("token.json"))
    if hoge["token"] != "":
        print("トークンがすでに存在します。")
        print("終了後に古いアクセストークンを削除してください。")
except FileNotFoundError:
    pass
#まだ未完成(権限が)
#めも　みすきーのよくわからんやつ aWZkjwCivskarMbigKpCxY4C9I1jLBqY
session_id = str(uuid.uuid4())
webbrowser.open_new("https://misskey.io/miauth/"+session_id+r"?name=TL読み上げ用&permission=read:account")
input("認証が完了したらEnterキーを押してください。")
res = json.loads(str(requests.post(r"https://misskey.io/api/miauth/"+session_id+r"/check").text))

with open("token.json", "w") as f:
    if not res["ok"]:
        print("認証に失敗しました")
        exit()
    print(res["token"])
    json.dump({"token": res["token"]}, fp=f)
    print("トークンを保存しました。")
    exit()
