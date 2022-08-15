import socket
import threading
import gameboard as gb

from tkinter import *
from tkinter import messagebox


# Initalize global variables
clientSocket,clientAddress = None, None
start = False
user = False
board = None
position = 0
finish = False
Client = ""

# RUN THE IP.py PROGRAM TO OBTAIN HOST'S IP
serverAddress = socket.gethostbyname(socket.gethostname()) # IP address of host(client will need it)
port = 5050 # Port number(client will need it)
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket
serverSocket.bind((serverAddress,port)) # Attach port number to the socket
serverSocket.listen(1) # Limit client connections to 1 at a time

# Main thread for running the game using the recieveMove function
def createThread(c):
    thread = threading.Thread(target = c)
    thread.daemon = True
    thread.start()
            
def receiveMove():
    global start, position
    while True:
        if start and user:
            try:
                data,addr = clientSocket.recvfrom(1024)
                data = data.decode()
                print(data)
                if data == "Good Game":              
                    gameOver() 
                elif data == "Play Again?":               
                    resetGame()                     #Reset the board if client wants a rematch
                else:
                    position,board.finalMove = data.split("-")
                    board.movementInGame(int(position),board.finalMove)
                    if int(position) == 0:          #Updates the corresponding button text in the GUI 
                        button1["text"]="X"
                    elif int(position) == 1:
                        button2["text"]="X"
                    elif int(position) == 2:
                        button3["text"]="X"
                    elif int(position) == 3:
                        button4["text"]="X"
                    elif int(position) == 4:
                        button5["text"]="X"
                    elif int(position) == 5:
                        button6["text"]="X"
                    elif int(position) == 6:
                        button7["text"]="X"
                    elif int(position) == 7:
                        button8["text"]="X"
                    elif int(position) == 8:
                        button9["text"]="X"
                    finish,won = board.gameDone()
                    if finish:
                        board.gameDone()
                        board.cleanGame()
                        board.finalMove = "player1"
            except:
                pass

def establishConnection():
    global start,user,Client,board
    while True:     
        if start and not user:
            try:
                user = True
                data,addr = clientSocket.recvfrom(1024)
                name = data.decode()
                board = gb.Board(name)
                Client = name
                sendData = '{}'.format("player1").encode()
                clientSocket.send(sendData)
            except:
                pass

# Function for accepting the clients connection
def acceptConnection():
    global clientSocket,clientAddress,start
    clientSocket,clientAddress = serverSocket.accept()
    message = "Join request from "+str(clientAddress)+" client?"
    answer = messagebox.askyesno("Question",message)
    if answer:
        sendData = '{}'.format("Join Request Accepted").encode()
        clientSocket.send(sendData)
        start = True
        resetGame()
        establishConnection()
    else:
        sendData = '{}'.format("Join Request Not accepted").encode()
        clientSocket.send(sendData)
        clientSocket.close()
    


createThread(acceptConnection)
createThread(receiveMove)
        
def gameOver():
    GB = False
    start = False
    user = False
    close = True
    clientSocket.close()
    board.countGames = (board.countGames - 1)
    resetGame()

# resetGame the board after game is finished 
def resetGame():
    button1["text"]=" "
    button2["text"]=" "
    button3["text"]=" "
    button4["text"]=" "
    button5["text"]=" "
    button6["text"]=" "
    button7["text"]=" "
    button8["text"]=" "
    button9["text"]=" "


# Function sets the button based on the users corresponding box choice and updates the board. 
# The updated move also gets sent to the host
# The gameboard class has a shared object which gets locked using the board.finalMove variable
def button(n,button):
    global finish,board
    if start and user and button["text"]==" ":
        if board.finalMove == Client:
            button["text"]="O"
            board.finalMove = "player1"
            sendData = '{}-{}'.format(str(n),board.finalMove).encode()
            clientSocket.send(sendData)
            board.movementInGame(n,board.finalMove)
            finish,won = board.gameDone()
            if finish:
                board.gameDone()
                board.cleanGame()
                board.finalMove = "player1"

# GUI CODE
window=Tk()
window.title("TiC-Tac-Toe")
window.geometry("525x500+0+0")
window.configure(background = 'white')

titleFrame = Frame(window, bg ='white', pady =2, width = 800, height=100, relief = RIDGE)
titleFrame.grid(row=0, column =0)
Title = Label(titleFrame, font=('times',50,'bold'),text="Tic Tac Toe", bd=21, bg='White',fg='black',justify = CENTER)
Title.grid(row=0,column = 0)

gameFrame = Frame (window, bg = 'white', bd=10,width = 800, height=550, relief=RIDGE) 
gameFrame.grid(row=1,column=0)

boardFrame = Frame (gameFrame ,bd=10, width =650, height=500, pady=3, padx=8, bg="White", relief=RIDGE)
boardFrame.pack(side=LEFT)

button1 = Button(boardFrame, text=" ",bg="white", fg="Black",width=8,height=3,font=('Times', 24),command= lambda: button(0, button1))
button1.grid(column=1, row=1, sticky = S+N+E+W)
button2 = Button(boardFrame, text=" ",bg="white", fg="Black",width=8,height=3,font=('Times', 24), command= lambda: button(1, button2))
button2.grid(column=2, row=1, sticky = S+N+E+W)
button3 = Button(boardFrame, text=" ",bg="white", fg="Black",width=8,height=3,font=('Times', 24),command= lambda: button(2, button3))
button3.grid(column=3, row=1, sticky = S+N+E+W)
button4 = Button(boardFrame, text=" ",bg="white", fg="Black",width=8,height=3,font=('Times', 24),command= lambda: button(3, button4))
button4.grid(column=1, row=2, sticky = S+N+E+W)
button5 = Button(boardFrame, text=" ",bg="white", fg="Black",width=8,height=3,font=('Times', 24),command= lambda: button(4, button5))
button5.grid(column=2, row=2, sticky = S+N+E+W)
button6 = Button(boardFrame, text=" ",bg="white", fg="Black",width=8,height=3,font=('Times', 24),command= lambda: button(5, button6))
button6.grid(column=3, row=2, sticky = S+N+E+W)
button7 = Button(boardFrame, text=" ",bg="white", fg="Black",width=8,height=3,font=('Times', 24),command= lambda: button(6, button7))
button7.grid(column=1, row=3, sticky = S+N+E+W)
button8 = Button(boardFrame, text=" ",bg="white", fg="Black",width=8,height=3,font=('Times', 24),command= lambda: button(7, button8))
button8.grid(column=2, row=3, sticky = S+N+E+W)
button9 = Button(boardFrame, text=" ",bg="white", fg="Black",width=8,height=3,font=('Times', 24),command= lambda: button(8, button9))
button9.grid(column=3, row=3, sticky = S+N+E+W)
window.mainloop()