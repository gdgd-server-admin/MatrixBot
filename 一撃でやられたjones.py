# このbotは
#
# 部屋内で誰かが「星となれッ！」と発言すると言葉が入っている３つのリストから１つずつ抽選を行う
# 抽選した３つの言葉を繋げて発言する

MATRIX_URL = "https://smith.gdgd.jp.net"
MATRIX_USER = "bottest"
MATRIX_PASS = "********************"
MATRIX_ROOM = "#off-topic:smith.gdgd.jp.net"

MY_NAME = "@bottest:smith.gdgd.jp.net"

# pip install matrix_client を実行してMatrix接続用のモジュールをインストールする
from matrix_client.client import MatrixClient
import random

# リストその１
list_a = []

# リストその２
list_b = []

# リストその３
list_c = []

# リストその１にデータを流し込む
list_a.append("ちょっと待て")
list_a.append("桃園で")
list_a.append("寒空で")

# リストその１にデータを流し込む
list_b.append("光の速さで")
list_b.append("右も左も")
list_b.append("正直歯がゆい")

# リストその１にデータを流し込む
list_c.append("自己破産")
list_c.append("マッチョメン")
list_c.append("連コイン")


# Matrixへのログイン
client = MatrixClient(MATRIX_URL)
token = client.login(username=MATRIX_USER, password=MATRIX_PASS)
room = client.join_room(MATRIX_ROOM)

# 誰かが発言した時の反応
def on_message(room, event):
    if event['type'] == "m.room.message":                               # 部屋の中のメッセージ
        if event['content']['msgtype'] == "m.text":                     # メッセージは文字で画像とか動画ではない
            if not event['sender'] == MY_NAME:                          # 送信者が自分「ではない」
                if event['content']['body'] == "星となれッ！":               # 本文が「星となれッ！」である
                    # 文章１の抽選
                    idx_a = random.randint(0, len(list_a) - 1)
                    word_a = list_a[idx_a]
                    # 文章２の抽選
                    idx_b = random.randint(0, len(list_b) - 1)
                    word_b = list_b[idx_b]
                    # 文章３の抽選
                    idx_c = random.randint(0, len(list_c) - 1)
                    word_c = list_c[idx_c]

                    # word_a、word_b、word_cに抽選結果の言葉が格納された

                    room.send_html("{}<br/>　{}<br/>　　{}".format(word_a,word_b,word_c)) # 三つの言葉を文章として繋げる。改行したいのでHTMLとして送る 

# 裏でメッセージを受け付ける
room.add_listener(on_message)
client.start_listener_thread()

# 無限ループ
while True:
    string = input("文字列を入力してください:") # 文字入力を受け付ける
    if string == "quit":                    # 「quit」と入力されたら
        break                               # ループを抜ける

# プログラム終了