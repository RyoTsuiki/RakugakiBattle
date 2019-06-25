import socketserver
import socket
import subprocess
import string
import MySQLdb
import textwrap 
import datetime
import random

ID_LENGTH       = 8 
DISCONNECT      = "disconnect"
RANKING         = "ranking"
REQ_RANKING 	= "req_ranking"
STARTGAME       = "start_game"
ENDGAME         = "end_game"
MLPATH          = "python MLTest.py"
RESULT          = "result"
GAMEDATA        = "game_data"
ERROR           = "error"
FINISH          = "finish"
KARI            = 404
IMG_FOLDER_PATH = ""
#サーバ側のホストとポート
HOST, PORT      = "", 12345
#お題データのファイル名
ODAI_TEXT_NAME  = "odai.txt"
#お題を取得
odai_txt        = open(ODAI_TEXT_NAME, "r", encoding = "utf-8")
odai_lines      = odai_txt.read().splitlines()
n               = len(odai_lines)
odai            = []
for i in range(n):
    odai.append(odai_lines[i].split(",")[0])
ODAI            = odai.copy()
print(ODAI)


# 接続する
conn = MySQLdb.connect(user='root',passwd='labmember',host='localhost',db='rakugaki_battle',charset='utf8')
cursor = conn.cursor()

class SocketHandler(socketserver.BaseRequestHandler):

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
            cursor.execute(sql)
            count = cursor.fetchone()[0]
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
            count = cursor.execute(sql)
            conn.commit() 
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
            count = cursor.execute(sql)
            conn.commit() 
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
            count = cursor.execute(sql)
            conn.commit() 
            return True
        except MySQLdb.Error as e:
            print(e)
            return False

    #データベースから順位を求める
    def __search_rank_from_db(self):
        sql = textwrap.dedent('''
            select leaderboard.rank 
            from (
                select id, rank()OVER(ORDER BY score DESC) as "rank"
                from player_data
                where score IS NOT NULL) leaderboard
            where 	leaderboard.id = "{id}";
        ''').format(id = self.id).strip()
        #IDが重複していればFALSE(違うIDで再び実行されることを期待)
        rank = 0
    
        try:
            cursor.execute(sql)
            rank = cursor.fetchone()[0]
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
            cursor.execute(sql)
            rank = cursor.fetchall()
        except MySQLdb.Error as e:
            print(e)
            return False

        return rank 

    def __db_delete(self):
        sql = textwrap.dedent("""
            delete 
            from player_data 
            where id = "{id}";
        """).format(id = self.id).strip()

        try:
            cursor.execute(sql)
            conn.commit() 
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
        return( ODAI[odai_index] )

    #ユーザーのIDを求める
    def __create_id(self):
        while True:
            id_kouho = SocketHandler.__meke_random_string(self, ID_LENGTH)
            if(SocketHandler.__search_and_insert_ID(self, id_kouho) == True):
                break
        return (id_kouho)

    def __send_ranking(self):
        my_message  = RANKING + ","
        records     = SocketHandler.__db_ranking(self)
        for record in records:
            my_message += "@".join((map(str,record)))
            my_message += ";"

        self.client.sendall(my_message.encode())
        print("send:  " + my_message)



    #ゲームデータメッセージを送る
    def __send_game_data(self):
        #メッセージ作成（game_data, お題, ID）
        my_message = GAMEDATA + ","
        my_message += self.odai + ","
        my_message += self.id + ","

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
    def __send_error(self, error):
        my_message = ERROR + ", " + error + ","
        self.client.sendall(my_message.encode())
        print("send:  " + my_message)
        


    #前処理
    def __mae_syori(self, data):
        pass

    #推論機に画像のpathを与えてスコアを得る
    def __send_ML(self, img_path):
        cmd = ["python",MLPATH,img_path]
        score = subprocess.check_output(cmd).decode('utf-8').strip()        
        return(score)

    #後処理
    def __ato_syori(self, data):
        pass

    #送られてきたメッセージを解釈する
    def __Interpretation_message(self, message):
        messages = message.split(",")
        reqest = messages[0]

        if reqest == STARTGAME: 
            if(self.shinkoudo >= 1):
                SocketHandler.__db_delete(self)
                SocketHandler.__send_error(self,"リスタートされました")

            self.shinkoudo = 1
            self.id = SocketHandler.__create_id(self)
            self.name = messages[1]
            self.odai = SocketHandler.__decide_odai(self)
            SocketHandler.__send_game_data(self)
            SocketHandler.__add_db_name(self)

        elif reqest == ENDGAME:
            if(self.shinkoudo <= 0):
                SocketHandler.__send_error(self,"ゲームが開始されていません")
            else:
                data = "test"
                SocketHandler.__mae_syori(self, data)
                img_path = IMG_FOLDER_PATH + self.id + ".jpg"
                print(str(self.client_address) + " -sendML- " + img_path)
                self.score = SocketHandler.__send_ML(self, img_path)
                print(str(self.client_address) + " -score- " + str(self.score))
                SocketHandler.__ato_syori(self, data)
                SocketHandler.__add_db_score(self)
                rank = SocketHandler.__search_rank_from_db(self)
                SocketHandler.__send_result(self, rank)
                self.shinkoudo = 0
        elif reqest == REQ_RANKING:
            SocketHandler.__send_ranking(self)
        elif reqest == ERROR:
            pass
        else: 
            SocketHandler.__send_error(self,"指定形式のメッセージではありません")

    #クライアントが接続してきたら
    def handle(self):
        #通信先のクライアント
        self.client = self.request
        self.shinkoudo = 0
        print("connected" + str(self.client_address))

        #メッセージを受け取る
        while(True):
            message = self.client.recv(4096).decode('utf-8').strip()
            print(str(self.client_address) + " - " + message)
            if message == DISCONNECT or message == "":
                print("disconnected")
                self.client.sendall(DISCONNECT.encode())
                break
            SocketHandler.__Interpretation_message(self, message)

    def send(self,object):
        pass

if __name__ == "__main__":
    server = socketserver.ThreadingTCPServer((HOST, PORT), SocketHandler)
    print("listen" + str((HOST, PORT)))
    server.serve_forever()
    







ftp = FTP(
    "e",
    "pee",
    passwd="pass"
)
with open("ttt.png", "rb") as f:  # 注意：バイナリーモード(rb)で開く必要がある
    ftp.storbinary("STOR /chinpo.png", f)
