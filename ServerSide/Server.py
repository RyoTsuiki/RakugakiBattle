import socketserver
import socket
import subprocess
import string
import MySQLdb
import textwrap 
import datetime
import random
import sys
import room
import threading
import cv2
sys.path.append("../MachineLearning")
import predict
import np_load
import time
import numpy as np
from tensorflow.python.keras.models import load_model
'''
from keras import backend as K
from keras.datasets import cifar10
from keras.models import load_model
from keras.utils import to_categorical
from keras_compressor import custom_objects
'''
#sys.path.append("C:\\Users\\Ryo Tsuiki\\Desktop\\local\\RakugakiBattle\\MachineLearning")
#import predict

ID_LENGTH       = 8 
BATTLEDATA      = "battle_data"
DISCONNECT      = "disconnect"
RANKING         = "ranking"
REQ_RANKING 	= "req_ranking"
STARTGAME       = "start_game"
ENDGAME         = "end_game"
MLPATH          = "MLTest.py"
RESULT          = "result"
GAMEDATA        = "game_data"
ERROR           = "error"
FINISH          = "finish"
JOIN            = "join"
CANCEL          = "cancel"
SCORE_TOTYU_KAZU= 3
IMG_FOLDER_PATH = "../img/"
DATA            = "data" 
#サーバ側のホストとポート
HOST, PORT      = "", 12345
#お題データのファイル名
ODAI_TEXT_NAME  = "odai.txt"
BATTLE_START    = "battle_start"
BATTLE_CANCEL   = "battle_cancel"
BATTLEEND       = "battle_end"
REQ_SCORE       = "req_score"
MODEL_PATH      = "../../standard/model.h5"
label_path      = "../../standard/label.csv"
#お題を取得
odai_txt        = open(ODAI_TEXT_NAME, "r", encoding = "utf-8")
odai_lines      = odai_txt.read().splitlines()
n               = len(odai_lines)
odai            = []
for i in range(n):
    odai.append(odai_lines[i].split(","))
ODAI            = odai.copy()


# 接続する
conn = MySQLdb.connect(user='root',passwd='labmember',host='localhost',db='rakugaki_battle',charset='utf8')
cursor = conn.cursor()

class SocketHandler(socketserver.BaseRequestHandler):
    haita = threading.Semaphore(1)
    waiting_room = None
    #self
    #self.score 得点
    #self.name ユーザー名
    #self.id ユーザーID
    #self.client_address　(IPアドレス,ポート番号)
    #self.client クライアント

    #IDがかぶってなければDBに追加
    def __search_and_insert_ID(self, id_kouho):
        sql = textwrap.dedent('''
            SELECT COUNT(*)
            FROM player_data
            WHERE id = "{id}" 
            LIMIT 1;
        ''').format(id = id_kouho).strip()
        #IDが重複していればFALSE(違うIDで再び実行されることを期待)
        count = 0
        
        
        try:
            self.cursor.execute(sql)
            count = self.cursor.fetchone()[0]
        except MySQLdb.Error as e:
            print(e)
            return False
    
        if(int(count) >= 1):
            return False

        
        sql = textwrap.dedent('''
            INSERT INTO player_data(id)
            VALUES ("{id}"); 
        ''').format(id = id_kouho).strip()
        
        try:
            count = self.cursor.execute(sql)
            self.conn.commit() 
            return True
        except MySQLdb.Error as e:
            print(e)
            return False
        
    #名前をDBに追加
    def __add_db_name(self):
        sql = textwrap.dedent('''
            UPDATE player_data
            SET name = "{name}", odai = "{odai}"
            WHERE id = "{id}";
        ''').format(id = self.id, name = self.name, odai = self.odai).strip()

        try:
            count = self.cursor.execute(sql)
            self.conn.commit() 
            return True
        except MySQLdb.Error as e:
            print(e)
            return False

    #スコアを追加
    def __add_db_score(self):
        sql = textwrap.dedent('''
            UPDATE player_data
            SET score = "{score}"
            WHERE id = "{id}";
        ''').format(id = self.id, score = self.score).strip()

        try:
            count = self.cursor.execute(sql)
            self.conn.commit() 
            return True
        except MySQLdb.Error as e:
            print(e)
            return False

    #データベースから順位を求める
    def search_rank_from_db(self, xp_id):
        sql = textwrap.dedent('''
            select leaderboard.rank 
            from (
                select id, rank()OVER(ORDER BY score DESC) as "rank"
                from player_data
                where score IS NOT NULL) leaderboard
            where 	leaderboard.id = "{id}";
        ''').format(id = xp_id).strip()
        rank = 0
        try:
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            rank = res[0]
        except MySQLdb.Error as e:
            print(e)
            return False

        return rank 

    def __db_ranking(self):
        sql = textwrap.dedent("""
            select rank()OVER(ORDER BY score DESC) as "rank", player_data.*
            from player_data
            where score IS NOT NULL
            limit 5;
        """).strip()

        try:
            self.cursor.execute(sql)
            rank = self.cursor.fetchall()
        except MySQLdb.Error as e:
            print(e)
            return False

        return rank 

    #指定したIDのdataを消す
    def __db_delete(self):
        sql = textwrap.dedent("""
            delete 
            from player_data 
            where id = "{id}";
        """).format(id = self.id).strip()

        try:
            self.cursor.execute(sql)
            self.conn.commit() 
            print("deleted{self.id}")
        except MySQLdb.Error as e:
            print(e)
            return False

    #ランダムな文字列を作成
    def __meke_random_string(self, length):
        return("".join([random.choice(string.ascii_letters + string.digits) for i in range(length)]))


    #お題を決める
    def __decide_odai(self):
        odai_index = random.randint(0, (len(ODAI) - 1))
        return( ODAI[odai_index][0] , ODAI[odai_index][1])


    #ユーザーのIDを求める
    def __create_id(self):
        while True:
            id_kouho = self.__meke_random_string(ID_LENGTH)
            if(self.__search_and_insert_ID(id_kouho) == True):
                break
        return (id_kouho)

    def __send_ranking(self):
        my_message  = RANKING + ","
        records     = self.__db_ranking()
        for record in records:
            my_message += "@".join((map(str,record)))
            my_message += ";"

        self.client.sendall(my_message.encode())
        print("send:  " + my_message)



    #ゲームデータメッセージを送る
    def __send_game_data(self):
        #メッセージ作成（game_data, お題, ID）
        my_message = GAMEDATA + ","
        my_message += self.odai_japanese + ","
        my_message += self.id + ","
        self.client.sendall(my_message.encode())
        print("send:  " + my_message)
    
    #スコアの系列を送る
    def __send_data(self, data):
        my_message = DATA + ","
        #メッセージ作成
        for label, score in data.items(): 
            my_message += "@".join([label, str(int(score*100))]) + ","
        self.client.sendall(my_message.encode())
        print("send:  " + my_message)

    #結果を送信
    def __send_result(self, rank):
        my_message = RESULT + ","
        my_message += str(self.score) + ","
        my_message += str(rank) + ","

        self.client.sendall(my_message.encode())
        print("send:  " + my_message)

    #エラーを送信
    def send_error(self, error):
        my_message = ERROR + ", " + error + ","
        self.client.sendall(my_message.encode())
        print("send:  " + my_message)

    #前処理
    def __mae_syori(self, data):
        pass

    #推論機に画像のpathを与えてスコアを得る
    def __send_ML(self, img_path):
        return predict.predict(self.model,img_path,label_path,raw_model_flag = True)

    #後処理
    def __ato_syori(self, data):
        score = int(data[self.odai] * 1000) 
        return score
    #バトルの情報を送信
    def __send_battle_data(self,players):
        #メッセージ作成（game_data, お題, ID）
        my_message = BATTLEDATA + ","
        my_message += self.odai + ","
        my_message += self.id + ","
        for player in players:
            my_message += player.name + ","
        self.client.sendall(my_message.encode())

    def battle_start(self, room_odai, players):
            if(self.shinkoudo >= 1):
                self.__db_delete()
                self.send_error("リスタートされました")

            self.shinkoudo = 1
            self.id = self.__create_id()
            self.odai = room_odai
            self.__add_db_name()
            self.__send_battle_data(players)

    def battle_end(self,scores):
        my_message = BATTLEEND + ","
        for player_rs in scores:
            my_message += "@".join(map(str,([player_rs[0],player_rs[1],player_rs[2],player_rs[3]]))) + ","
        self.client.sendall(my_message.encode())
        self.my_room = None
    #送られてきたメッセージを解釈する
    def __Interpretation_message(self, message):
        messages = message.split(",")
        reqest = messages[0]
        #ゲーム開始時
        if reqest == STARTGAME: 
            if(self.shinkoudo >= 1):
                self.__db_delete()
                self.send_error("リスタートされました")

            self.shinkoudo = 1
            self.id = self.__create_id()
            self.name = messages[1]
            self.odai,self.odai_japanese = self.__decide_odai()
            self.__send_game_data()
            self.__add_db_name()
        #スコア要求時
        elif reqest == REQ_SCORE:
            data = self.__send_ML(IMG_FOLDER_PATH + self.id + ".png")
            self.__send_data(data)
        #落書き終了時
        elif reqest == ENDGAME:
            if(self.shinkoudo <= 0):
                self.send_error("ゲームが開始されていません")
            else:
                data = "test"
                self.__mae_syori(data)
                img_path = IMG_FOLDER_PATH + self.id + ".png"
                print(str(self.client_address) + " -sendML- " + img_path)
                data = self.__send_ML(img_path)
                self.score = self.__ato_syori(data)
                print(str(self.client_address) + " -score- " + str(self.score))
                self.__add_db_score()
                if(self.my_room is None):
                    rank = self.search_rank_from_db(self.id)
                    self.__send_result(rank)
                    self.shinkoudo = 0
                else:
                    self.my_room.add_result(self)
                    self.shinkoudo = 0
        #ランキング要求時
        elif reqest == REQ_RANKING:
            self.__send_ranking()
        #バトル開始時
        elif reqest == BATTLE_START:
            if(not(self.my_room is None)): 
                self.send_error("すでに開始されています")
                return
            self.name = messages[1]
            SocketHandler.haita.acquire()
            if(room.Room.waiting is None):
                self.my_room = room.Room(self)
                print(str(self.client_address) + " -roomMake- ")
                self.client.sendall(b"waiting")
            else:
                self.my_room = room.Room.waiting.add_prayer(self)
                print(str(self.client_address) + " -roomAdd- ")
                self.client.sendall(b"added")
            SocketHandler.haita.release()
        #バトルキャンセル時
        elif reqest == BATTLE_CANCEL:
            if self.shinkoudo >= 1:
                self.send_error("バトルが開始されています")
            elif self.my_room is None:
                self.send_error("部屋を立てていません")
            else:
                self.my_room.cancel()
                self.my_room = None
                self.send_error("キャンセルされました")
        elif reqest == ERROR:
            pass
        else: 
            self.send_error("指定形式のメッセージではありません")

    #クライアントが接続してきたら
    def handle(self):
        #通信先のクライアント
        self.conn = conn

        self.model = load_model(MODEL_PATH)
        self.cursor  = cursor
        self.client = self.request
        self.shinkoudo = 0
        self.my_room = None
        print("connected" + str(self.client_address))

        #メッセージを受け取る
        while(True):
            message = self.client.recv(4096).decode('utf-8').strip()
            print(str(self.client_address) + " - " + message)
            if message == DISCONNECT or message == "":
                print("disconnected")
                if(not self.my_room is None):   self.my_room.cancel()
                self.client.sendall(DISCONNECT.encode())
                SocketHandler.haita.release()
                break
            self.__Interpretation_message(message)

    def send(self,object):
        pass

if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer((HOST, PORT), SocketHandler)
    print("listen" + str((HOST, PORT)))
    server.serve_forever()
    








