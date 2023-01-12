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

  quake_feed = feedparser.parse("https://www.data.jma.go.jp/developer/xml/feed/eqvol.xml")

  for entry in quake_feed.entries:
    id = entry.id
    sql_find_id = "select * from HIST where id='{}'".format(id)
    id_found = cur.execute(sql_find_id)
    if id_found.fetchone() is None:
#     print("履歴に存在しない")
      now = time.time()
      sql_insert_id = "insert into HIST values ('{}',{})".format(id, int(time.time()))
      cur.execute(sql_insert_id)
      child = feedparser.parse(id)
      try:
        for centry in child.entries:
          code = centry["code"]

          # 地震情報はcode=361
          if code == "361" and child.feed.information["type"] == '震源・震度に関する情報（市町村等）':
            # 震源と震度の情報
            summary = child.feed.summary.split("\n")
            stamp = dateutil.parser.parse(summary[0]).strftime("%Y/%m/%d %H:%M")
            tmp = "<font color=\"gray\"><b>地震情報 【 {} 発生】</b><br/> <br/>　震源地： {} <br/> <br/>".format(stamp,summary[4])
            tmp = tmp + "<table><tr><th>地域</th><th>震度</th></tr>"
            for s in summary:
              if s.find("<area />") >= 0:
                m = s.replace("<area />","")
                if not m == "":
                  print(m)
                  area = m.split("<code>")[0]
                  maxint = m.split("</code>")[1]
                  tmp = tmp + "<tr><td> {} </td><td> {} </td></tr>".format(area,maxint)

            tmp = tmp + "</table> </font>"
            msg.append(tmp)
      except:
        pass

#  cur.execute("delete from HIST where id=(select id from HIST order by stamp desc limit 1)")
  con.commit()

  return set(msg)
