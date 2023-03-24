# このbotは
#
# RSSからデータを取得して任意のチャンネルに発言として投げる。
# どのRSSからデータを取得するかは起動した時間によって変わるようにタイムスケジュールを組む
# 一定周期で実行したら新着情報を全部発言して終了する

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
# タイムスケジュールに記載されているURLからニュースを取得する
url = ""

JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
d = datetime.datetime.now(JST)
now = "{:0>2}{:0>2}".format(d.hour,int(d.minute / 10)*10) # 現在時刻を４けたの数字にして10分単位にする

# 20:22なら「 2020 」になる

# タイムスケジュール
schedule = {}
schedule["0000"] = ""
schedule["0010"] = ""
schedule["0020"] = ""
schedule["0030"] = ""
schedule["0040"] = ""
schedule["0050"] = ""
schedule["0100"] = ""
schedule["0110"] = ""
schedule["0120"] = ""
schedule["0130"] = ""
schedule["0140"] = ""
schedule["0150"] = ""
schedule["0200"] = ""
schedule["0210"] = ""
schedule["0220"] = ""
schedule["0230"] = ""
schedule["0240"] = ""
schedule["0250"] = ""
schedule["0300"] = ""
schedule["0310"] = ""
schedule["0320"] = ""
schedule["0330"] = ""
schedule["0340"] = ""
schedule["0350"] = ""
schedule["0400"] = ""
schedule["0410"] = ""
schedule["0420"] = ""
schedule["0430"] = ""
schedule["0440"] = ""
schedule["0450"] = ""
schedule["0500"] = ""
schedule["0510"] = ""
schedule["0520"] = ""
schedule["0530"] = ""
schedule["0540"] = ""
schedule["0550"] = ""
schedule["0600"] = ""
schedule["0610"] = ""
schedule["0620"] = ""
schedule["0630"] = ""
schedule["0640"] = ""
schedule["0650"] = ""
schedule["0700"] = "https://assets.wor.jp/rss/rdf/reuters/oddlyenough.rdf" # ロイターの非公式RSS
schedule["0710"] = "https://assets.wor.jp/rss/rdf/ynnews/news.rdf" # よんななニュースの非公式RSS
schedule["0720"] = "https://assets.wor.jp/rss/rdf/maidona/new.rdf" # まいどなニュースの非公式RSS
schedule["0730"] = "https://www.j-cast.com/index.xml" # J-CASTの総合RSS
schedule["0740"] = "https://sportiva.shueisha.co.jp/rss.xml" # スポルティーバのRSS
schedule["0750"] = "https://news.yahoo.co.jp/rss/topics/top-picks.xml" # Yahooニュースの主要トピックスのRSS
schedule["0800"] = ""
schedule["0810"] = ""
schedule["0820"] = "https://rocketnews24.com/feed/" # ロケットニュース24のRSS
schedule["0830"] = ""
schedule["0840"] = ""
schedule["0850"] = ""
schedule["0900"] = ""
schedule["0910"] = ""
schedule["0920"] = "https://rss.itmedia.co.jp/rss/2.0/netlab.xml" # ねとらぼのRSS
schedule["0930"] = ""
schedule["0940"] = ""
schedule["0950"] = ""
schedule["1000"] = "https://news.yahoo.co.jp/rss/media/inumag/all.xml"
schedule["1010"] = ""
schedule["1020"] = ""
schedule["1030"] = "https://rocketnews24.com/feed/" # ロケットニュース24のRSS
schedule["1040"] = "https://news.yahoo.co.jp/rss/media/nekomag/all.xml"
schedule["1050"] = ""
schedule["1100"] = "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FtcGhHZ0pLVUNnQVAB?hl=ja&gl=JP&ceid=JP:ja" # Googleニュースのエンタメカテゴリ>
schedule["1110"] = "https://news.yahoo.co.jp/rss/topics/top-picks.xml" # Yahooニュースの主要トピックスのRSS
schedule["1120"] = ""
schedule["1130"] = ""
schedule["1140"] = ""
schedule["1150"] = "https://rss.itmedia.co.jp/rss/2.0/netlab.xml" # ねとらぼのRSS
schedule["1200"] = "https://assets.wor.jp/rss/rdf/reuters/oddlyenough.rdf" # ロイターの非公式RSS
schedule["1210"] = "https://assets.wor.jp/rss/rdf/ynnews/news.rdf" # よんななニュースの非公式RSS
schedule["1220"] = "https://assets.wor.jp/rss/rdf/maidona/new.rdf" # まいどなニュースの非公式RSS
schedule["1230"] = "https://www.j-cast.com/index.xml" # J-CASTの総合RSS
schedule["1240"] = "https://sportiva.shueisha.co.jp/rss.xml" # スポルティーバのRSS
schedule["1250"] = "https://news.yahoo.co.jp/rss/media/biz_lifeh/all.xml"
schedule["1300"] = ""
schedule["1310"] = ""
schedule["1320"] = ""
schedule["1330"] = "https://rocketnews24.com/feed/" # ロケットニュース24のRSS
schedule["1340"] = ""
schedule["1350"] = ""
schedule["1400"] = "https://news.yahoo.co.jp/rss/topics/top-picks.xml" # Yahooニュースの主要トピックスのRSS
schedule["1410"] = ""
schedule["1420"] = ""
schedule["1430"] = ""
schedule["1440"] = ""
schedule["1450"] = "https://rss.itmedia.co.jp/rss/2.0/netlab.xml" # ねとらぼのRSS
schedule["1500"] = "https://www.gizmodo.jp/index.xml" # ギズモードのRSS
schedule["1510"] = "https://rss.itmedia.co.jp/rss/2.0/topstory.xml" # ITmediaの総合RSS
schedule["1520"] = "https://codezine.jp/rss/new/index.xml" # CodeZineのRSS
schedule["1530"] = "https://news.google.com/rss/topics/CAAqKAgKIiJDQkFTRXdvSkwyMHZNR1ptZHpWbUVnSnFZUm9DU2xBb0FBUAE?hl=ja&gl=JP&ceid=JP:ja" # Googleニュースのテクノロジー[>
schedule["1540"] = ""
schedule["1550"] = ""
schedule["1600"] = "https://rocketnews24.com/feed/" # ロケットニュース24のRSS
schedule["1610"] = ""
schedule["1620"] = ""
schedule["1630"] = "https://news.yahoo.co.jp/rss/topics/top-picks.xml" # Yahooニュースの主要トピックスのRSS
schedule["1640"] = "https://news.yahoo.co.jp/rss/media/nekomag/all.xml"
schedule["1650"] = "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FtcGhHZ0pLVUNnQVAB?hl=ja&gl=JP&ceid=JP:ja" # Googleニュースのエンタメカテゴリ>
schedule["1700"] = "https://assets.wor.jp/rss/rdf/reuters/oddlyenough.rdf" # ロイターの非公式RSS
schedule["1710"] = "https://assets.wor.jp/rss/rdf/ynnews/news.rdf" # よんななニュースの非公式RSS
schedule["1720"] = "https://assets.wor.jp/rss/rdf/maidona/new.rdf" # まいどなニュースの非公式RSS
schedule["1730"] = "https://www.j-cast.com/index.xml" # J-CASTの総合RSS
schedule["1740"] = "https://sportiva.shueisha.co.jp/rss.xml" # スポルティーバのRSS
schedule["1750"] = "https://rss.itmedia.co.jp/rss/2.0/netlab.xml" # ねとらぼのRSS
schedule["1800"] = "https://news.yahoo.co.jp/rss/media/inumag/all.xml"
schedule["1810"] = ""
schedule["1820"] = ""
schedule["1830"] = "https://news.yahoo.co.jp/rss/media/driverweb/all.xml"
schedule["1840"] = ""
schedule["1850"] = "https://news.yahoo.co.jp/rss/media/biz_lifeh/all.xml"
schedule["1900"] = ""
schedule["1910"] = ""
schedule["1920"] = "https://news.yahoo.co.jp/rss/topics/top-picks.xml" # Yahooニュースの主要トピックスのRSS
schedule["1930"] = ""
schedule["1940"] = ""
schedule["1950"] = ""
schedule["2000"] = ""
schedule["2010"] = ""
schedule["2020"] = ""
schedule["2030"] = ""
schedule["2040"] = ""
schedule["2050"] = "https://news.yahoo.co.jp/rss/media/bikeno/all.xml"
schedule["2100"] = "https://news.yahoo.co.jp/rss/media/baseballc/all.xml"
schedule["2110"] = "https://news.yahoo.co.jp/rss/media/flix/all.xml"
schedule["2120"] = ""
schedule["2130"] = ""
schedule["2140"] = ""
schedule["2150"] = ""
schedule["2200"] = "https://news.yahoo.co.jp/rss/media/anmanmv/all.xml"
schedule["2210"] = "https://news.yahoo.co.jp/rss/media/animage/all.xml"
schedule["2220"] = "https://news.yahoo.co.jp/rss/media/animage/all.xml"
schedule["2230"] = ""
schedule["2240"] = ""
schedule["2250"] = ""
schedule["2300"] = ""
schedule["2310"] = ""
schedule["2320"] = ""
schedule["2330"] = ""
schedule["2340"] = ""
schedule["2350"] = ""


# タイムスケジュールから該当する時刻に取得すべきURLを引き出そうと試みる（書き間違えてたりするとやばいことになるので「試みる」）
try:
  url = schedule[now]
except: # 万が一にもやばいことが起こったら
  url = "" # なかったことにする

# URLが空っぽの場合はお茶濁しとして2chのURLを指定しておく
if url == "":
  url = "https://headline.5ch.net/bbynews/news.rss"

# ここにくるまでにurlには何かしらが入っている
if url != "":

  # RSSのニュースを読み込む
  d_atom = feedparser.parse(url)

  # 繰り返し処理でMatrixに発言する
  for news in d_atom.entries:
    room.send_text("{} {}".format(news.title,news.link))
    time.sleep(2)
