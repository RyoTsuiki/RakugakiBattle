import socket
import subprocess
import numpy as np

cmd = "ls"
str = subprocess.call(cmd.split())
#print(str)
score = 0
#�����L���O�f�[�^
data = [[score,"img"]]*100
print(data)

#�����L���O�ɃX�R�A��ǉ�
def add_score():
    pass
#�����L���O�f�[�^���N���C�A���g�ɑ��M
def return_ranking():
    pass
#CSV�Ƀ����L���O��ۑ�
def save_ranking():
    pass
#CSV�̃����L���O���擾
def load_csv_ranking():
    pass
#�@�B�w�K�Ƀf�[�^�𑗂�X�R�A�𓾂�
def get_scores():
    pass
    
#�����L���O�����߂�
def calc_rankng():
    pass

#�N���C�A���g�ɃX�R�A�𑗂�
def send_score():
    pass