import socketserver
from ftplib import FTP
import socket
from tinydb import TinyDB, Query
import hashlib
import random
import subprocess

#サーバ側のホストとポート
HOST, PORT = "", 12345
#お題データのファイル名
ODAI_TEXT_NAME = "odai.txt"
#お題を取得
odai_txt = open(ODAI_TEXT_NAME, "r")
ODAI = odai_txt.read().splitlines()
#データベースの選択
DB = TinyDB('tiny_db.json')
print(ODAI[random.randint(0, (len(ODAI)-1))])


class SocketHandler(socketserver.BaseRequestHandler):

    #self
    #self.score 得点
    #self.name ユーザー名
    #self.id ユーザーID
    #self.client_address　(IPアドレス,ポート番号)
    #self.client クライアント


    #お題を決める
    def __decide_odai(self):
        odai_index = random.randint(0, (len(ODAI) - 1))
        return( ODAI[odai_index] )

    #ユーザーのIDを求める
    def __create_id(self):
        return ("test")

    #結果を送信
    def __send_result(self, rank):
        my_message = "result,"
        my_message += str(self.score) + ","
        my_message += str(rank)
        self.client.sendall(my_message.encode())

    #ゲームデータメッセージを送る
    def __send_game_data(self):
        #メッセージ作成（game_data, お題, ID）
        my_message = "game_data,"
        my_message += SocketHandler.__decide_odai(self) + ","
        my_message += self.id 

        self.client.sendall(my_message.encode())

    #前処理
    def __mae_syori(self, data):
        pass

    #推論機に画像のpathを与えてスコアを得る
    def __send_ML(self, img_path):
        score = subprocess.check_output('python MLTest.py img_path').decode('utf-8').strip()        
        return(score)
        
    #データベース登録
    def __regist_DB(self):
        pass

    #データベースから順位を求める
    def __search_rank_from_DB(self):
        pass

    #後処理
    def __ato_syori(self, data):
        pass

    #送られてきたメッセージを解釈する
    def __Interpretation_message(self, message):
        messages = message.split(",")
        reqest = messages[0]

        if reqest == "start_game"   : 
            self.name = messages[1]
            SocketHandler.__send_game_data(self)

        elif reqest == "end_game"   :
            data = "test"
            SocketHandler.__mae_syori(self, data)
            img_path = "" + self.id + ".jpg"

            print(str(self.client_address) + " -sendML- " + img_path)
            self.score = SocketHandler.__send_ML(self, img_path)
            print(str(self.client_address) + " -score- " + str(self.score))

            SocketHandler.__ato_syori(self, data)
            SocketHandler.__regist_DB(self)
            rank = SocketHandler.__search_rank_from_DB(self)
            SocketHandler.__send_result(self, rank)
            
    #クライアントが接続してきたら
    def handle(self):
        #通信先のクライアント
        self.client = self.request
        self.id = SocketHandler.__create_id(self)
        print("connected" + str(self.client_address))

        #メッセージを受け取る
        while(True):
            message = self.client.recv(4096).decode('utf-8').strip()
            print(str(self.client_address) + " - " + message)

            SocketHandler.__Interpretation_message(self, message)
            #メッセージがなければ終了
            if message == "":
                break

    def send(self,object):
        pass


if __name__ == "__main__":
    server = socketserver.TCPServer((HOST, PORT), SocketHandler)
    print("listen" + str((HOST, PORT)))
    server.serve_forever()
    





    
ftp = FTP(
    "e",
    "pee",
    passwd="pass"
)
with open("ttt.png", "rb") as f:  # 注意：バイナリーモード(rb)で開く必要がある
    ftp.storbinary("STOR /chinpo.png", f)
