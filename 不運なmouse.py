# このbotは
#
# 部屋内で誰かが「さいころ」と発言すると１〜６のランダムな数字を発言する

MATRIX_URL = "https://smith.gdgd.jp.net"
MATRIX_USER = "bottest"
MATRIX_PASS = "****************"
MATRIX_ROOM = "#off-topic:smith.gdgd.jp.net"

MY_NAME = "@bottest:smith.gdgd.jp.net"

# pip install matrix_client を実行してMatrix接続用のモジュールをインストールする
from matrix_client.client import MatrixClient
import random

# Matrixへのログイン
client = MatrixClient(MATRIX_URL)
token = client.login(username=MATRIX_USER, password=MATRIX_PASS)
room = client.join_room(MATRIX_ROOM)

# 誰かが発言した時の反応
def on_message(room, event):
    if event['type'] == "m.room.message":                               # 部屋の中のメッセージ
        if event['content']['msgtype'] == "m.text":                     # メッセージは文字で画像とか動画ではない
            if not event['sender'] == MY_NAME:                          # 送信者が自分「ではない」
                if event['content']['body'] == "さいころ":               # 本文が「さいころ」である
                    room.send_text("[{}]".format(random.randint(1, 6))) # 1から6までのランダムな数字を発現する

# 裏でメッセージを受け付ける
room.add_listener(on_message)
client.start_listener_thread()

# 無限ループ
while True:
    string = input("文字列を入力してください:") # 文字入力を受け付ける
    if string == "quit":                    # 「quit」と入力されたら
        break                               # ループを抜ける

# プログラム終了