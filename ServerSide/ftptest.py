from ftplib import FTP
ftp = FTP(
    "192.168.11.28",
    "labmember",
    passwd="labmember"
)
with open("odai.txt", "rb") as f:  # 注意：バイナリーモード(rb)で開く必要がある
    print("ok")
    ftp.storlines("STOR test.txt", f)