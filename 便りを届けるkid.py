MATRIX_URL = "https://smith.gdgd.jp.net"
MATRIX_USER = "a.kid"
MATRIX_PASS = "*************"
MATRIX_ROOM = "#news-bot-dev:smith.gdgd.jp.net"

# pip install feedparser を実行してRSS読み取りのモジュールをインストールする
from matrix_client.client import MatrixClient
import os,time,feedparser,datetime

# Matrixへのログイン
client = MatrixClient(MATRIX_URL)
token = client.login(username=MATRIX_USER, password=MATRIX_PASS)
room = client.join_room(MATRIX_ROOM)


# ニュースの取得
# ６つのニュースソースを10分毎に巡回する

url = ""

d = datetime.datetime.now()
if d.minute >= 0 and d.minute <= 9:
  # :00〜:09に起動されたら1番目のニュースソースから取得する
  url = "https://headline.5ch.net/bbynews/news.rss" # 2ch ニュース速報のRSS
if d.minute >= 10 and d.minute <= 19:
  # :10〜:19に起動されたら2番目のニュースソースから取得する
  url = "https://www.j-cast.com/index.xml" # J-CASTの総合RSS
if d.minute >= 20 and d.minute <= 29:
  # :20〜:29に起動されたら3番目のニュースソースから取得する
  url = "https://sportiva.shueisha.co.jp/rss.xml" # スポルティーバのRSS
if d.minute >= 30 and d.minute <= 39:
  # :30〜:39に起動されたら4番目のニュースソースから取得する
  url = "https://assets.wor.jp/rss/rdf/reuters/oddlyenough.rdf" # ロイターの非公式RSS
if d.minute >= 40 and d.minute <= 49:
  # :40〜:49に起動されたら5番目のニュースソースから取得する
  url = "https://assets.wor.jp/rss/rdf/ynnews/news.rdf" # ４７ニュースの非公式RSS
if d.minute >= 50 and d.minute <= 59:
  # :50〜:59に起動されたら6番目のニュースソースから取得する
  url = "https://assets.wor.jp/rss/rdf/maidona/new.rdf" # まいどなニュースの非公式RSS

if url != "":
  # RSSを読み込む
  d_atom = feedparser.parse(url)

  # 読み込んだニュースを繰り返し処理で発言する
  for news in d_atom.entries:
    room.send_text("{} {}".format(news.title,news.link)) # タイトルとURL
    time.sleep(2) # ちょっと待つ