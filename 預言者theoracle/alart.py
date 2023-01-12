# -*- coding: utf-8 -*-

# 気象情報（注意報・警報）の取得

# sqlite3を使用して「どこまで取得したか」を記録する
# 履歴に存在しないデータだけ詳細を取得する
def get_data():

  msg = []

  import requests,sqlite3,time
  import xml.etree.ElementTree as ET
  res = requests.get('https://www.data.jma.go.jp/developer/xml/feed/extra.xml')
  con = sqlite3.connect("data/alart.db")
  cur = con.cursor() 
  cur.execute("CREATE TABLE IF NOT EXISTS HIST(id text,stamp integer)")
  if res.status_code == 200:
    root = ET.fromstring(res.text)
    for child in root.findall("{http://www.w3.org/2005/Atom}entry"):
      sql_find_id = "select * from HIST where id='{}'".format(child.find("{http://www.w3.org/2005/Atom}id").text)
      id_found = cur.execute(sql_find_id)
      if id_found.fetchone() is None:
#        print("履歴に存在しない")
        now = time.time()
        sql_insert_id = "insert into HIST values ('{}',{})".format(child.find("{http://www.w3.org/2005/Atom}id").text,int(time.time()))
        cur.execute(sql_insert_id)
        child_data = requests.get(child.find("{http://www.w3.org/2005/Atom}id").text)
        if child_data.status_code == 200:
          child_data.encoding = 'UTF-8'
          detail_root = ET.fromstring(child_data.text)
          detail_body = detail_root.find("{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}Body")
          detail_infomation = detail_body.findall("{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}Warning")
          for detail in detail_infomation:
            try:
              if str(detail.attrib["type"]).find("気象警報・注意報（府県予報区等）") >= 0:
                for item in detail:
                  info_kinds = item.findall("{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}Kind")
                  info_area = item.find("{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}Area")
                  kinds = []
                  for info_kind in info_kinds:
                    info_kind_name = info_kind.find("{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}Name").text
                    info_kind_status = info_kind.find("{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}Status").text
                    if info_kind_status.find("継続") < 0:
                      kinds.append("{} ： {}".format(info_kind_name,info_kind_status))
                  area_name = info_area.find("{http://xml.kishou.go.jp/jmaxml1/body/meteorology1/}Name").text
                  if len(kinds) > 0:
                    msg.append("<font color=\"gray\"><b>気象情報 【 {} 】</b><br/> <br/>　 {}</font>".format(area_name,"<br/>　 ".join(kinds)))
            except:
              pass
#      row = {}
#      row["id"] = entry.find('id').text
#      msg.append(row)
#  cur.execute("delete from HIST where id=(select id from HIST order by stamp desc limit 1)")
  con.commit()

  return set(msg)
