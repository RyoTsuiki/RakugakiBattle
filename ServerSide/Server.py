# coding: utf-8
# Your code here!
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
    1
#�����L���O�f�[�^���N���C�A���g�ɑ��M
def return_ranking():
    0
#CSV�Ƀ����L���O��ۑ�
def save_ranking():
    1
#CSV�̃����L���O���擾
def load_csv_ranking():
    4
#�@�B�w�K�Ƀf�[�^�𑗂�X�R�A�𓾂�
def get_scores():
    4
    
#�����L���O�����߂�
def calc_rankng():
    5

#�N���C�A���g�ɃX�R�A�𑗂�
def send_score():
    77s