import socket
import subprocess
import numpy as np

cmd = "ls"
str = subprocess.call(cmd.split())
#print(str)
score = 0
#ランキングデータ
data = [[score,"img"]]*100
print(data)

#ランキングにスコアを追加
def add_score():
    pass
#ランキングデータをクライアントに送信
def return_ranking():
    pass
#CSVにランキングを保存
def save_ranking():
    pass
#CSVのランキングを取得
def load_csv_ranking():
    pass
#機械学習にデータを送りスコアを得る
def get_scores():
    pass
    
#ランキングを求める
def calc_rankng():
    pass

#クライアントにスコアを送る
def send_score():
    pass