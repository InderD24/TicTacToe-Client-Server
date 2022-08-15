import socket
import threading
import gameboard as gb

from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog

#Global variable initializations
serverAddress = None
serverPort = None
connectionSocket = None
finish = False
GB = False
close = False
start = False
user = False
board = None
position = 0
player1 = ""
name = "Client"

# Main thread for running the game using the recieveMove function
def createThread(c):
    thread = threading.Thread(target = c)
    thread.daemon = True
    thread.start()

# receiveMove function retrieves updated data from the host(server)
def receiveMove():
    global start, position, user, close, GB
    while True:  
        if GB and start and user:
            try:
                data,addr = connectionSocket.recvfrom(1024)
                data = data.decode()
                if data != "":     
                    position,board.finalMove = data.split("-")
                    board.movementInGame(int(position),board.finalMove)
                    if int(position) == 0:          #Updates the corresponding button text in the GUI     
                        button1["text"]="O"
                    elif int(position) == 1:
                        button2["text"]="O"
                    elif int(position) == 2:
                        button3["text"]="O"
                    elif int(position) == 3:
                        button4["text"]="O"
                    elif int(position) == 4:
                        button5["text"]="O"
                    elif int(position) == 5:
                        button6["text"]="O"
                    elif int(position) == 6:
                        button7["text"]="O"
                    elif int(position) == 7:
                        button8["text"]="O"
                    elif int(position) == 8:
                        button9["text"]="O"
                    playGame()
            except:
                pass
        

def establishConnection():
    global start,player1, GB, board, user, name, close, connectionSocket
    while True:
        if GB:
            if (not start or not user):
                data,addr = connectionSocket.recvfrom(1024)
                data = data.decode()
                if data == "Join Request Not accepted":
                    GB = True
                    connectionSocket.close()
                elif data == "Join Request Accepted":
                    sendData = '{}'.format(name).encode()
                    connectionSocket.send(sendData)
                    start = True   
                    close = False            
                elif data == "player1": 
                    player1 = data              
                    board = gb.Board(name)
                    board.finalMove = player1
                    user = True
                    break


createThread(receiveMove)

def playGame():
    global start, close, user, GB
    finish,won = board.gameDone()
    if finish:
        answer = messagebox.askyesno("Question", "Play Game again?")
        if answer:
            sendData = '{}'.format("Play Again?").encode()
            connectionSocket.send(sendData)
            board.isGameFinished()
            resetGame()
        else:
            GB = False
            sendData = '{}'.format("Good Game").encode()
            connectionSocket.send(sendData)
            connectionSocket.close()                     #Close socket after game has finshed 
            start = False
            user = False
            close = True
            resetGame()

# Resets board and clears all the buttons in the grid                
def resetGame():
    board.cleanGame()
    board.finalMove = player1
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
def button(n, button):
    global finish,board
    if start and user and button["text"]==" ":
        if board.finalMove == player1:
            button["text"]="X"
            board.finalMove = name
            sendData = '{}-{}'.format(str(n),board.finalMove).encode()
            connectionSocket.send(sendData)
            board.movementInGame(n,board.finalMove) 
            playGame()

# Sets up the connection between the client and the user
# Asks the client for the hosts ip address and port connection number
def ConnectButton():
    global serverAddress,serverPort,connectionSocket,GB
    if not GB:
        serverAddress = simpledialog.askstring("Input", "What is host's ip address?",parent=window)
        serverPort = simpledialog.askstring("Input", "What is the host's port number?",parent=window)
        if serverAddress != "" and serverPort != "":
            try:
                connectionSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connectionSocket.connect((serverAddress,int(serverPort)))
                GB = True
                try:
                    establishConnection()
                except Exception:
                    GB = False
                    messagebox.showerror("Error", "Host rejected has the connection")
            except Exception:
                messagebox.showerror("Error", "Invalid hostname or port!")
        else:
            messagebox.showerror("Error", "Invalid hostname or port!")
 

#GUI Related Code 
window=Tk()
window.title("TiC-Tac-Toe")
window.geometry("600x500+0+0")
window.resizable(width=False, height=False)
window.configure(background = 'white')

tops = Frame(window, bg ='white', pady =2, width = 1350, height=150, relief = RIDGE)
tops.grid(row=0, column =0)

Title = Label(tops, font=('Times',50,'bold'),text="Tic Tac Toe", bd=21, bg='white',fg='black',justify = CENTER)
Title.grid(row=0,column = 0)

gameFrame = Frame (window, bg = 'white', bd=10,width = 1400, height=700, relief=RIDGE) 
gameFrame.grid(row=1,column=0)

boardFrame = Frame (gameFrame ,bd=10, width =650, height=500, pady=2, padx=8, bg="White", relief=RIDGE)
boardFrame.pack(side=LEFT)


rightFrame = Frame (gameFrame,bd=10, width =300, height=500, padx=3, pady=3, bg="white", relief=RIDGE)
rightFrame.pack(side=RIGHT)

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
buttonConnect=Button(rightFrame, text="Connect", font=('arial', 18, 'bold'), height = 1, width =5,command = ConnectButton)
buttonConnect.grid (row=2, column=0 ,padx=6, pady=11)

window.mainloop()