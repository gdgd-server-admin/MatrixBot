# このbotは
#
# Matrixサーバ上のデータベースに保存されている通報情報の生データを取得して任意のチャンネルに発言として投げる
# 一定周期で実行したら新着情報を全部発言して終了する

MATRIX_URL = "https://smith.gdgd.jp.net"         # MatrixのサーバURL（ElementのURLではない）
MATRIX_USER = "a.cypher"                         # Matrixのユーザ名
MATRIX_PASS = "*****************"                # Matrixのパスワード
MATRIX_ROOM = "#sg-room:smith.gdgd.jp.net"       # botが発言するチャンネル（個人相手にもできる）

POSTGRES_HOST = "*****************"              # データベースのホスト
POSTGRES_DATABASE = "*************"              # データベース名
POSTGRES_USER = "*************"                  # データベースのユーザ名
POSTGRES_PASS = "*************"                  # データベースのパスワード






# pip install pg8000 を実行してPostgres接続用のモジュールをインストールする
import pg8000.native
# pip install matrix_client を実行してMatrix接続用のモジュールをインストールする
from matrix_client.client import MatrixClient
import os

# データベースに接続する
dbcon = pg8000.native.Connection(POSTGRES_USER, host=POSTGRES_HOST, database=POSTGRES_DATABASE, password=POSTGRES_PASS)
# Matrixに繋ぐ準備をする
client = MatrixClient(MATRIX_URL)

# Matrixにログインする
token = client.login(username=MATRIX_USER, password=MATRIX_PASS)

# 発言するMatrixのチャンネルに入る
room = client.join_room(MATRIX_ROOM)

# event_reports.idの最大値をファイルに保持しておいてその最大値＋１から処理を始める
maxid = 1
# ファイルがあったら読み込む
if os.path.isfile("./maxid"):
  l = open("./maxid")
  maxid = int(l.read())
  l.close()

# 実行するSQL。event_reports.room_idは一見するとどんなチャンネルかわからないのでroom_aliasesから見やすいチャンネル名を取得する
sql = "select id,(select room_alias from room_aliases where room_aliases.room_id = event_reports.room_id limit 1),user_id,reason from event_reports where id > {}".format(maxid)

# SQLを実行した結果を繰り返しで処理する
for row in dbcon.run(sql):
  # row[0] = id、row[1] = user_id、row[2] = room_id（room_aliasesテーブルから見やすい名前を取得したもの）、row[3] = reason
  # 取説には書かれていないがsend_textではなくsend_htmlを使うとHTMLで整形ができる
  room.send_html("@room <b>通報あり</b>  <br/>　通報者：{}  <br/>　チャンネル：{}  <br/>　理由：{}".format(row[1],row[2],row[3]))
  # maxidを更新する
  maxid = int(row[0])

# maxidの最終的な値をファイルに保持する
l = open("./maxid","w")
l.write(str(maxid))
l.close()