 -*- coding: utf8 -*-

'''

このプログラムは

asariとmlaskという２つのAIエンジンを使用して発言内容の感情を解析し、
それが負の感情だと思われる時にアクションを起こすことで人間に通知する。

'''

from matrix_client.client import MatrixClient
from asari.api import Sonar
import time,datetime
import numpy as np

# Matrix接続設定
MATRIX_URL = "https://smith.gdgd.jp.net"
MATRIX_USER = "satie"
MATRIX_PASS = "************************"
MATRIX_ROOM = "#free-talk:smith.gdgd.jp.net"
MY_NAME = "@satie:smith.gdgd.jp.net"

client = MatrixClient(MATRIX_URL)
token = client.login(username=MATRIX_USER, password=MATRIX_PASS)
room = client.join_room(MATRIX_ROOM)

# AIエンジン
sonar = Sonar()

# 追加のAIエンジン
import mlask
emotion_analyzer = mlask.MLAsk()

warning = False
score_hist = []

def on_message(room, event):
    if event['type'] == "m.room.message":                               # 部屋の中のメッセージ
        if event['content']['msgtype'] == "m.text":                     # メッセージは文字で画像とか動画ではない
            if not event['sender'] == MY_NAME:                          # 送信者が自分「ではない」
                msg = event['content']['body']
                res = sonar.ping(text=msg)
                top_class = res["top_class"]
                score = 0
                counter_score = 0
                for i in res["classes"]:
                    if i["class_name"] == top_class:
                        score = i["confidence"]
                    else:
                        counter_score = i["confidence"]

                # 今回のスコアを履歴へ
                newscore = (score - counter_score) * 1.0
                if top_class == "negative":
                    newscore = newscore * -1.0

                # mlaskを使って追加判定する
                res = emotion_analyzer.analyze(msg)
                if res["emotion"] != None:
                    for i in res["emotion"]:
                        if str(i) == "iya":
                            newscore -= 0.1
                        elif str(i) == "yorokobi":
                            newscore += 0.1
                        elif str(i) == "kowa":
                            newscore -= 0.1
                        elif str(i) == "yasu":
                            newscore += 0.1
                        elif str(i) == "aware":
                            newscore -= 0.1
                        elif str(i) == "suki":
                            newscore += 0.1
                        elif str(i) == "ikari":
                            newscore -= 0.1
                        elif str(i) == "takaburi":
                            newscore += 0.1
                        elif str(i) == "haji":
                            newscore -= 0.1
                        elif str(i) == "odoroki":
                            newscore += 0.1

                # 今回のスコアを履歴に入れて平均値計算に回す
                score_hist.append(newscore)

                # どう考えても酷いやつは個別に反応する
                if newscore <= -0.7:
                    room.send_text("{} めっ！だよ？".format(event['sender']))

                # 履歴に一定の件数が溜まっている時にだけネガポジ判定を行う
                if len(score_hist) > 5:
                    # 平均値を算出して-0.50を超えたらまずい空気だと思う
                    average = np.array(score_hist).mean()
                    print("avg: {}".format(average))
                    if average < -0.50:
                        room.send_text("@room このおへやこわいよぅ...")

                if len(score_hist) > 10:
                    # 100件超えたら先頭を１個消す
                    score_hist.pop(0)



room.add_listener(on_message)
client.start_listener_thread()

# 無限ループ
while True:
    string = input("文字列を入力してください:") # 文字入力を受け付ける
    if string == "quit":                    # 「quit」と入力されたら
        break                               # ループを抜ける

# プログラム終了


