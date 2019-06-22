# 注意事項
## 文字コードについて
サーバーサイド(Linux) で使用予定のプログラムのソースコードはUTF-8 にしておくと吉  
-> デフォルトがUTF-8 のため (Windows -> Shift JIS)

(参考)  
vim にて文字コードを指定する  
UTF-8 でファイルを開き直す

```
:e ++enc=cp932
```

UTF-8 でファイルを保存

```
:se fenc=cp932
```

[参考](https://qiita.com/bezeklik/items/2c9925f9c07762559471)

## ネットワーク通信について
Linux の場合, いくつか引っかかったため以下参考

### PermissionError: [Errno 13] Permission denied
プログラム実行に管理者権限が必要 (sudo)

### OSError: [Errno 98] Address already in use
プログラムで使用予定のポート番号がすでに使われているときに発生  
以下対処法  
* 再起動
* ポート番号を使用しているプログラムを停止する

特定のポート番号を使用しているプログラムを表示させる場合  

```
sudo lsof -i:ポート番号
```

(そもそもきちんとソケットを閉じることが大切)

## インストールが必要なライブラリ
* python==3.5 (anaconda にて入れる)
* tensorflow==1.5.0 (gpuの場合 tenforflow-gpu==1.5.0)
* h5py (pip install h5py)
* scikit.learn (pip install scikit-learn)
