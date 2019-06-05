# coding: utf-8
# Your code here!
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
    1
#ランキングデータをクライアントに送信
def return_ranking():
    0
#CSVにランキングを保存
def save_ranking():
    1
#CSVのランキングを取得
def load_csv_ranking():
    4
#機械学習にデータを送りスコアを得る
def get_scores():
    4
    
#ランキングを求める
def calc_rankng():
    5

#クライアントにスコアを送る
def send_score():
    77s