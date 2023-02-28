# -*- coding: utf8 -*-

from matrix_client.client import MatrixClient
from asari.api import Sonar
import time,datetime
import numpy as np
import os,configparser

pid = open("satie.pid","w")
pid.write(str(os.getpid()))
pid.close()

# Matrix接続設定
config = configparser.ConfigParser()
config.read("config.ini")
MATRIX_URL = config["CONNECTION"]["URL"]
MATRIX_USER = config["CONNECTION"]["USER"]
MATRIX_PASS = config["CONNECTION"]["PASS"]
MATRIX_ROOM = config["CONNECTION"]["ROOM"]
MY_NAME = config["CONNECTION"]["MYNAME"]

client = MatrixClient(MATRIX_URL)
token = client.login(username=MATRIX_USER, password=MATRIX_PASS)
room = client.join_room(MATRIX_ROOM)

# AIエンジン
from transformers import BertTokenizer, BertForSequenceClassification, pipeline

tokenizer = BertTokenizer.from_pretrained("koheiduck/bert-japanese-finetuned-sentiment")
model = BertForSequenceClassification.from_pretrained("koheiduck/bert-japanese-finetuned-sentiment")
tokenizer2 = BertTokenizer.from_pretrained("kit-nlp/bert-base-japanese-sentiment-cyberbullying")
model2 = BertForSequenceClassification.from_pretrained("kit-nlp/bert-base-japanese-sentiment-cyberbullying")
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

                score = 0
                ai_judge = []

                # BERTでの判定
                res_bert = pipeline("sentiment-analysis",model=model, tokenizer=tokenizer)(msg)[0]
                print(res_bert)
                if res_bert["label"].lower() == "positive":
                    ai_judge.append(res_bert["score"])
                elif res_bert["label"].lower() == "negative":
                    ai_judge.append(res_bert["score"] * -1.0)

                res_bert2 = pipeline("sentiment-analysis",model=model2, tokenizer=tokenizer2)(msg)[0]
                print(res_bert2)
                if res_bert2["label"].lower() == "ポジティブ":
                    ai_judge.append(res_bert2["score"])
                elif res_bert2["label"].lower() == "ネガティブ":
                    ai_judge.append(res_bert2["score"] * -1.0)

                # asariでの判定
                res_asari = sonar.ping(text=msg)
                _top_class = res_asari["top_class"]
                for i in res_asari["classes"]:
                    if i["class_name"] == _top_class:
                        if _top_class == "positive":
                            ai_judge.append(i["confidence"])
                        elif _top_class == "negative":
                            ai_judge.append(i["confidence"] * -1.0)

                score = np.array(ai_judge).mean()
                print(ai_judge)
                print("score: {}".format(score))

                # 今回のスコアを履歴へ
                newscore = score

                # 今回のスコアを履歴に入れて平均値計算に回す
                score_hist.append(newscore)

                print("{}[{}]->{}".format(event["sender"],event["event_id"],newscore))
                # どう考えても酷いやつは個別に反応する
                if newscore < -0.9:
                    room.send_text("{} こわいことばはいけないんだよ？".format(event['sender']))

                # 0.8くらいを超えたらスマイリーをつけたい
                # https://smith.gdgd.jp.net/_matrix/client/r0/rooms/!MgzQcYvBdERYCDfJZi:smith.gdgd.jp.net/send/m.reaction/m1677225314318.0
                if newscore > 0.9:
                    reaction_content = {}
                    reaction_content["m.relates_to"] = {}
                    reaction_content["m.relates_to"]["rel_type"] = "m.annotation"
                    reaction_content["m.relates_to"]["event_id"] = event["event_id"]
                    reaction_content["m.relates_to"]["key"] = "😄"

                    client.api.send_message_event(event["room_id"], "m.reaction", reaction_content)


                # 履歴に一定の件数が溜まっている時にだけネガポジ判定を行う
                if len(score_hist) > 5:
                    # 平均値を算出して-70を超えたらまずい空気だと思う
                    average = np.array(score_hist).mean()
                    print("avg: {}".format(average))
                    if average < -0.6:
                        room.send_text("@room このおへやこわいよぅ...")

                if len(score_hist) > 10:
                    # 10件超えたら先頭を１個消す
                    score_hist.pop(0)



room.add_listener(on_message)
client.start_listener_thread()

# 無限ループ
while True:
    string = input("文字列を入力してください:") # 文字入力を受け付ける
    if string == "quit":                    # 「quit」と入力されたら
        break                               # ループを抜ける

# プログラム終了
