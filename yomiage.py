import os, clr, json
from time import sleep
#import Python
#おまじないゾーン
import Python.Runtime
Python.Runtime.PyObjectConversions.RegisterEncoder(Python.Runtime.Codecs.EnumPyIntCodec.Instance)
Python.Runtime.PyObjectConversions.RegisterDecoder(Python.Runtime.Codecs.EnumPyIntCodec.Instance)
#おまじないゾーン終わり
_editor_dir = os.environ["ProgramW6432"]+"\\AI\\AIVoice\\AIVoiceEditor\\"
if not os.path.isfile(_editor_dir+"AI.Talk.Editor.Api.dll"):
    print(_editor_dir+"AI.Talk.Editor.Api.dllが見つかりません。")
    print("A.I.VOICEがインストールされているか確認してください。")
    exit()
connecting = False
clr.AddReference(_editor_dir+"AI.Talk.Editor.Api")
from AI.Talk.Editor.Api import TtsControl, HostStatus

def connect():
    global tts_control, firstcurnum, firstmc, firstspeaker, firsttext, firsttxteditmode, connecting
    if connecting:
        print("Error: Cannot connect twice.")
        return
    tts_control = TtsControl()
    host_name = tts_control.GetAvailableHostNames()[0]
    tts_control.Initialize(host_name)
    if tts_control.Status == HostStatus.NotRunning:
        tts_control.StartHost()
    tts_control.Connect()
    host_version = tts_control.Version
    #print(f"{host_name} v{host_version}へ接続しました。")
    #print()
    firsttext = tts_control.Text
    firstcurnum = tts_control.TextSelectionStart
    firstmc = json.loads(tts_control.MasterControl)
    #print(firstmc)
    firsttxteditmode = tts_control.TextEditMode
    firstspeaker = tts_control.CurrentVoicePresetName
    tts_control.TextEditMode = 0
    tts_control.CurrentVoicePresetName = "琴葉 葵"
    mcjson = json.loads(tts_control.MasterControl)
    mcjson["SentencePause"] = 200
    mcjson["PitchRange"] = 1.44
    mcjson["Speed"] = 1.44
    tts_control.MasterControl = json.dumps(mcjson)
    connecting = True
def get_mc():
    return json.loads(tts_control.MasterControl)
def voice_lis():
    return tts_control.VoiceNames

def set_voice(voice):
    tts_control.CurrentVoicePresetName = voice
    return

def set_mc(name, value):
    mcjson = json.loads(tts_control.MasterControl)
    mcjson[name] = value
    tts_control.MasterControl = json.dumps(mcjson)
    return

def speak(text, reconnect=True):
    global connecting, tts_control
    if tts_control.Status == HostStatus.NotConnected or connecting == False:
        connecting = False
        if reconnect:
            connect()
        else:
            return
    tts_control.Text = text
    while tts_control.Status == HostStatus.Busy:
        sleep(0.01)
    #playtime = tts_control.GetPlayTime()
    try:
        tts_control.Play()
    except:
        print("再生に失敗しました。")
    #sleep((playtime+500)/1000)
    while tts_control.Status == HostStatus.Busy:
        sleep(0.01)
    return
def disconnect():
    global connecting, firstcurnum, firstmc, firstspeaker, firsttext, firsttxteditmode, tts_control
    if not connecting:
        print("Error: No connection found.")
        return
    while tts_control.Status == HostStatus.Busy:
        sleep(0.01)
    tts_control.MasterControl = json.dumps(firstmc)
    tts_control.Text = firsttext
    tts_control.TextSelectionStart = firstcurnum
    tts_control.TextEditMode = firsttxteditmode
    tts_control.CurrentVoicePresetName = firstspeaker
    tts_control.Disconnect()
    connecting = False
    #print(f"{host_name} v{host_version}との接続を終了しました。")
    return
