# -*- coding: utf-8 -*-


# 地震情報の取得

# sqlite3を使用して「どこまで取得したか」を記録する
# feedparserモジュールを使用することで処理を簡略化している
# 履歴に存在しないデータだけ詳細を取得する
def get_data():

  msg = []

  import feedparser,sqlite3,time,dateutil.parser
  con = sqlite3.connect("data/quake.db")
  cur = con.cursor() 
  cur.execute("CREATE TABLE IF NOT EXISTS HIST(id text,stamp integer)")

  quake_feed = feedparser.parse("https://www.data.jma.go.jp/developer/xml/feed/eqvol.xml") # 気象庁の高頻度フィード（地震火山）を読み込む

  for entry in quake_feed.entries:
    id = entry.id
    sql_find_id = "select * from HIST where id='{}'".format(id)
    id_found = cur.execute(sql_find_id)
    if id_found.fetchone() is None and str(entry.title).find("震源・震度に関する情報") >= 0: # タイトルで欲しい情報か判別する
      try:
        print("履歴に存在しない地震情報")
        now = time.time()
        sql_insert_id = "insert into HIST values ('{}',{})".format(id, int(time.time())) # 履歴に残す
        cur.execute(sql_insert_id)
        child = feedparser.parse(id) # idが詳細のURLになっているのでそれを読み込む
        summary = child.feed.summary.split("\n") # 後続処理のために行単位で分割する
        stamp = dateutil.parser.parse(summary[0]).strftime("%Y/%m/%d %H:%M") # 最初の１行目が報告時刻らしいのでそれを整形する
        tmp = "<font color=\"gray\"><b>地震情報 【 {} 発生】</b><br/> <br/>　震源地： {} <br/> <br/>".format(stamp,summary[4]) # ５行目に震源地がちょうど来る（feedparserが偶然処理している）
        tmp = tmp + "<table><tr><th>地域</th><th>震度</th></tr>" # 表にした方が見やすいと思うのでHTMLの表を作る
        for s in summary:
          if s.find("<area />") >= 0:
            m = s.replace("<area />","") # <area />というタグが見える行に各地の震度が（偶然）乗る
            if not m == "":
              print(m)
              area = m.split("<code>")[0] # データの中身を見ると<code>の手前までに地域名が見えるので切り取る
              maxint = m.split("</code>")[1] # データの中身を見ると</code>の後に震度が見えるので切り取る
              tmp = tmp + "<tr><td> {} </td><td> {} </td></tr>".format(area,maxint) # 行のHTMLにして繋げる

        tmp = tmp + "</table> </font>" # HTMLを閉じる
        msg.append(tmp)
      except:
        pass

  #cur.execute("delete from HIST")
  #con.commit()

  return set(msg)
