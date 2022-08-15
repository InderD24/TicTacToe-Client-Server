class Board:
    # Board initialization
    def __init__(self,newplayer):
        self.p1 = "player1"
        self.p2 = newplayer
        self.tiles = [0,0,0,0,0,0,0,0,0]
        self.finalMove = ""
        self.countGames = 1
        self.ties = 0
        self.ls = {"X": 0, "O": 0}
        self.dubs = {"X": 0, "O": 0}
    
    def isGameFinished(self):
        self.countGames = self.countGames + 1

    # Cleans the board
    def cleanGame(self):
        self.tiles = [0,0,0,0,0,0,0,0,0]

    # Function used for the shared object, locks corresponding turns
    def movementInGame(self,position,player):
        if player == "player1":
            self.tiles[position] = "O"
            self.finalMove = "player1"
        else:
            self.tiles[position] = "X"
            self.finalMove = self.p2

    # Checks if board is full and no more moves can be done
    def boardHaveSpace(self):
        for sqr in self.tiles:
            if sqr == 0:
                return False
        return True

    # Checks if there is a winner by matching rows, columns, and horizontal tiles
    def gameDone(self):
        finish = False
        victory = None
        tile1 = self.tiles[0]
        tile2 = self.tiles[1]
        tile3 = self.tiles[2]
        tile4 = self.tiles[3]
        tile5 = self.tiles[4]
        tile6 = self.tiles[5]
        tile7 = self.tiles[6]
        tile8 = self.tiles[7]
        tile9 = self.tiles[8]

        if (tile1==tile2 and tile1==tile3 and tile1=="O") or (tile4==tile5 and tile4==tile6 and tile4=="O") or (tile7==tile8 and tile7==tile9 and tile7=="O"):
            finish = True
            victory = "O"
            self.dubs["O"] = self.dubs["O"] + 1
            self.ls["X"] = self.ls["X"] + 1
        elif (tile1==tile2 and tile1==tile3 and tile1=="X") or (tile4==tile5 and tile4==tile6 and tile4=="X") or (tile7==tile8 and tile7==tile9 and tile7=="X"):
            finish = True
            victory = "X"
            self.dubs["X"] = self.dubs["X"] + 1
            self.ls["O"] = self.ls["O"] + 1
        elif (tile1==tile4 and tile1==tile7 and tile1=="O") or (tile2==tile5 and tile2==tile8 and tile2=="O") or (tile3==tile6 and tile3==tile9 and tile3=="O"):
            finish = True
            victory = "O"
            self.dubs["O"] = self.dubs["O"] + 1
            self.ls["X"] = self.ls["X"] + 1
        elif (tile1==tile4 and tile1==tile7 and tile1=="X") or (tile2==tile5 and tile2==tile8 and tile2=="X") or (tile3==tile6 and tile3==tile9 and tile3=="X"):
            finish = True
            victory = "X"
            self.dubs["X"] = self.dubs["X"] + 1
            self.ls["O"] = self.ls["O"] + 1
        elif (tile1==tile5 and tile1==tile9 and tile1=="O") or (tile7==tile5 and tile7==tile3 and tile7=="O"):
            finish = True
            victory = "O"
            self.dubs["O"] = self.dubs["O"] + 1
            self.ls["X"] = self.ls["X"] + 1
        elif (tile1==tile5 and tile1==tile9 and tile1=="X") or (tile7==tile5 and tile7==tile3 and tile7=="X"):
            finish = True
            victory = "X"
            self.dubs["X"] = self.dubs["X"] + 1
            self.ls["O"] = self.ls["O"] + 1
        elif self.boardHaveSpace():
            finish = True
            self.ties = self.ties + 1

        return finish,victory
