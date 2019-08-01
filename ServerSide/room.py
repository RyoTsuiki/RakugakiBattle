import Server
import random

class Room():
    MAX_PLAYER = 2
    waiting = None
    #部屋を作ると同時に親プレイヤーのデータを登録
    def __init__(self, oya_player):
        self.players = [oya_player]
        odai_index = random.randint(0, (len(Server.ODAI) - 1))
        self.odai = Server.ODAI[odai_index]
        self.scores = []
        Room.waiting = self
    #部屋に参加したプレイヤーおデータを登録
    def add_prayer(self, added_player):
        self.players.append(added_player)
        if(len(self.players) == Room.MAX_PLAYER):
            self.battle_start()
            return self
        elif(len(self.players) > Room.MAX_PLAYER):
            added_player.send_error("roomerroroverplayer")
            newRoom = Room(added_player)
            waiting = newRoom
            return Room(newRoom)
    #インスタンスにバトル開始を伝える
    def battle_start(self):
        Room.waiting = None
        for player in self.players:
            player.battle_start(self.odai, self.players)

    #そのまま送る
    def delivery_scores(self,player):
        for player in self.players:
            player.send_battle_result(player.name, player.id, player.scores)

    #結果を登録
    def add_result(self,player):
        self.scores.append([player.score, player.name, player.id])
        if(len(self.scores) == Room.MAX_PLAYER):
            self.battle_end(player)
        else:
            player.client.sendall(b"waiting,")

    #インスタンスにバトル結果を伝える
    def battle_end(self, player):
        print(self.scores)
        self.scores.sort(key=lambda x:x[0])
        self.scores.reverse()
        for i in range(len(self.scores)):
            self.scores[i].append(Server.SocketHandler.search_rank_from_db(player,self.scores[i][2]))

        for player in self.players:
            player.battle_end(self.scores)

    #cancell 
    def cancel(self):
        if(self == Room.waiting):
            Room.waiting = None