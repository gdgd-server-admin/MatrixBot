# このbotは
#
# 気象庁で公開されている気象情報APIからデータを取得して任意のチャンネルに発言として投げる。
# 全ての処理を１ファイルに記載するとファイルが長くなりすぎるので取得する情報ごとにファイル分割して
# 「import」を使って外部処理の呼び出しを行う形式にする
# 一定周期で実行したら新着情報を全部発言して終了する

MATRIX_URL = "https://smith.gdgd.jp.net"
MATRIX_USER = "theoracle2"
MATRIX_PASS = "******************"
MATRIX_ROOM = "#wetherquake:smith.gdgd.jp.net"

from matrix_client.client import MatrixClient

client = MatrixClient(MATRIX_URL)

# Existing user
token = client.login(username=MATRIX_USER, password=MATRIX_PASS)

room = client.join_room(MATRIX_ROOM)

import alart
for row in alart.get_data():
  room.send_html(row)

import quake
for row in quake.get_data():
  room.send_html(row)

