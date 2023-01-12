# このbotは
#
# 時間差で２つの発言をして終了する

MATRIX_URL = "https://smith.gdgd.jp.net"
MATRIX_USER = "lin"
MATRIX_PASS = "*************"
MATRIX_ROOM = "#omoneta:smith.gdgd.jp.net"

# pip install feedparser を実行してRSS読み取りのモジュールをインストールする
from matrix_client.client import MatrixClient

# Matrixへのログイン
client = MatrixClient(MATRIX_URL)
token = client.login(username=MATRIX_USER, password=MATRIX_PASS)
room = client.join_room(MATRIX_ROOM)

# 時間を計るときに使う
import time

room.send_text("プラグを抜けるもんなら抜いてみろよサイファー！")

time.sleep(5) # ここで指定した秒数だけ時間差が生まれる。5を指定したので5秒

room.send_text("この裏切りm")