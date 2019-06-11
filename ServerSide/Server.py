import socketserver
from ftplib import FTP
import socket
from tinydb import TinyDB, Query
import hashlib
import random
import subprocess

#�T�[�o���̃z�X�g�ƃ|�[�g
HOST, PORT = "", 12345
#����f�[�^�̃t�@�C����
ODAI_TEXT_NAME = "odai.txt"
#������擾
odai_txt = open(ODAI_TEXT_NAME, "r")
ODAI = odai_txt.read().splitlines()
#�f�[�^�x�[�X�̑I��
DB = TinyDB('tiny_db.json')
print(ODAI[random.randint(0, (len(ODAI)-1))])


class SocketHandler(socketserver.BaseRequestHandler):

    #self
    #self.score ���_
    #self.name ���[�U�[��
    #self.id ���[�U�[ID
    #self.client_address�@(IP�A�h���X,�|�[�g�ԍ�)
    #self.client �N���C�A���g


    #��������߂�
    def __decide_odai(self):
        odai_index = random.randint(0, (len(ODAI) - 1))
        return( ODAI[odai_index] )

    #���[�U�[��ID�����߂�
    def __create_id(self):
        return ("test")

    #���ʂ𑗐M
    def __send_result(self, rank):
        my_message = "result,"
        my_message += str(self.score) + ","
        my_message += str(rank)
        self.client.sendall(my_message.encode())

    #�Q�[���f�[�^���b�Z�[�W�𑗂�
    def __send_game_data(self):
        #���b�Z�[�W�쐬�igame_data, ����, ID�j
        my_message = "game_data,"
        my_message += SocketHandler.__decide_odai(self) + ","
        my_message += self.id 

        self.client.sendall(my_message.encode())

    #�O����
    def __mae_syori(self, data):
        pass

    #���_�@�ɉ摜��path��^���ăX�R�A�𓾂�
    def __send_ML(self, img_path):
        score = subprocess.check_output('python MLTest.py img_path').decode('utf-8').strip()        
        return(score)
        
    #�f�[�^�x�[�X�o�^
    def __regist_DB(self):
        pass

    #�f�[�^�x�[�X���珇�ʂ����߂�
    def __search_rank_from_DB(self):
        pass

    #�㏈��
    def __ato_syori(self, data):
        pass

    #�����Ă������b�Z�[�W�����߂���
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
            
    #�N���C�A���g���ڑ����Ă�����
    def handle(self):
        #�ʐM��̃N���C�A���g
        self.client = self.request
        self.id = SocketHandler.__create_id(self)
        print("connected" + str(self.client_address))

        #���b�Z�[�W���󂯎��
        while(True):
            message = self.client.recv(4096).decode('utf-8').strip()
            print(str(self.client_address) + " - " + message)

            SocketHandler.__Interpretation_message(self, message)
            #���b�Z�[�W���Ȃ���ΏI��
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
with open("ttt.png", "rb") as f:  # ���ӁF�o�C�i���[���[�h(rb)�ŊJ���K�v������
    ftp.storbinary("STOR /chinpo.png", f)
