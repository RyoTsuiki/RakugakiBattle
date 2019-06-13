import socket
import time
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("localhost",12345))
    s.sendall("start_game,てすた".encode())
    print(s.recv(4096))
    time.sleep(1)
    s.sendall("end_game".encode())
    print(s.recv(4096))
