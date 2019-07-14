from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import sys
import time

root = Tk()
root.title("Connect Four")
root.configure(background='blue')
root.resizable(False, False)

empty_img = ImageTk.PhotoImage(Image.open("empty_space.png"))
yellow_img = ImageTk.PhotoImage(Image.open("yellow_space.png"))
red_img = ImageTk.PhotoImage(Image.open("red_space.png"))
yellow_turn = ImageTk.PhotoImage(Image.open("yellow_circle.png"))

def make_row():
    row = ['' for x in range(6)]
    return row
def make_row_Image():
    rowImage = ['' for x in range(6)]
    return rowImage

colorScheme = {'':empty_img, 'y': yellow_img, 'r': red_img}
boardState = {0: make_row(), 1: make_row(), 2: make_row(), 3: make_row(), 4: make_row(), 5: make_row(),
                  6: make_row()}
boardImage = {0: make_row_Image(),1: make_row_Image(), 2: make_row_Image(), 3: make_row_Image(), 4: make_row_Image(), 5: make_row_Image(),
                  6: make_row_Image()}

turnCount = [1]

def checkFullBoard():
    fullRows = 0
    boardFullStatus = False
    for row in boardState.values():
        if '' not in row:
            fullRows += 1

    if fullRows >=7:
        boardFullStatus = True
    return boardFullStatus

def check4Horizontal(element, row):

    sliceRows = [row[0:4],row[1:5], row[2:6], row[3:]]
    connectFours = 0
    for sliceRow in sliceRows:
        if all(x == element for x in sliceRow):
            connectFours +=1
            break
        else:
            pass
    if connectFours == 0:
        return False
    else:
        return True

def checkWinHorizontal(color,coordinates):

    #check horizontal win
    rSpot = coordinates[1]
    cSpot = coordinates[0]
    winCondition = False
    #adjacent piece for same color
    fourList = []

    for row in boardState.values():
        fourList.append(row[rSpot])
    if fourList.count(color) >= 4:
        if check4Horizontal(color,fourList):
            winCondition = True

    return winCondition

def check4Vertical(element, column):

    sliceCols = [column[0:4], column[1:5], column[2:]]
    connectFours = 0
    for sliceCol in sliceCols:
        if all(x == element for x in sliceCol):
            connectFours += 1
            break
        else:
            pass
    if connectFours == 0:
        return False
    else:
        return True

def checkWinVertical(color,column):
    #check vertical win
    columnList = boardState[column]
    connectFours = 0

    if columnList.count(color)>=4:
        if check4Vertical(color,columnList):
            connectFours += 1

    if connectFours == 0:
        return False
    else:
        return True

def checkWinDiagonal(color,coordinates):

    connectFours = 0
    winningDiagonals = {'a6': [(0,5), (1,4),(2,3),(3,2)], 'a5': [(0,4), (1,3), (2,2), (3,1)], 'a4': [(0,3), (1,2), (2,1), (3,0)],
                        'b6': [(1,5), (2,4),(3,3),(4,2)], 'b5': [(1,4), (2,3), (3,2), (4,1)], 'b4': [(1,3), (2,2), (3,1), (4,0)],
                        'c6': [(2,5), (3,4),(4,3),(5,2)], 'c5': [(2,4), (3,3), (4,2), (5,1)], 'c4': [(2,3), (3,2), (4,1), (5,0)],
                        'd6a': [(3,5), (2,4),(1,3),(0,2)], 'd5a': [(3,4), (2,3), (1,2), (0,1)], 'd4a': [(3,3), (2,2), (1,1), (0,0)],
                        'd6b': [(3,5), (4,4),(5,3),(6,2)], 'd5b': [(3,4), (4,3), (5,2), (6,1)], 'd4b': [(3,3), (4,2), (5,1), (6,0)],
                        'e6': [(4,5), (3,4),(2,3),(1,2)], 'e5': [(4,4), (3,3), (2,2), (1,1)], 'e4': [(4,3), (3,2), (2,1), (1,0)],
                        'f6': [(5,5), (4,4),(3,3),(2,2)], 'f5': [(5,4), (4,3), (3,2), (2,1)], 'f4': [(5,3), (4,2), (3,1), (2,0)],
                        'g6': [(6,5), (5,4),(4,3),(3,2)], 'g5': [(6,4), (5,3), (4,2), (3,1)], 'g4': [(6,3), (5,2), (4,1), (3,0)]}

    diagonalsList = winningDiagonals.values()
    for diagonal in diagonalsList:
        colorsList = []
        for c in diagonal:
            cSpot = c[0]
            rSpot = c[1]
            colorSpot = boardState[cSpot][rSpot]
            colorsList.append(colorSpot)

        if all(x == color for x in colorsList):
            connectFours += 1

    if connectFours == 0:
        return False
    else:
        return True



def getColor(turnCount):
    color = ''
    if turnCount[-1] % 2 != 0:
        color = 'y'
    else:
        color = 'r'
    return color

def showNextTurn(turnCount):

    if turnCount % 2 == 0:
        color = 'r'
    else:
        color = 'y'

    Label(gameFrame, text="Player turn: ").grid(row=11, column=0)
    Label(gameFrame, image=colorScheme[color]).grid(row=11, column=1)

def make_move(column, turnCount):
    color = getColor(turnCount)

    boardFull = False
    horizontalWin = False
    verticalWin = False
    diagonalWin = False

    for r in range(1,8):
        rIndex = 0-r
        if boardState[column][rIndex] == '':
            rowIndex = rIndex + 6
            gridRowIndex = rIndex + 9
            coordinates = (column,rowIndex)
            boardState[column][rIndex] = color
            boardImage[column][rIndex] = Label(gameFrame, image = colorScheme[color]).grid(row=gridRowIndex,column=column)
            break
    boardFull = checkFullBoard()
    horizontalWin = checkWinHorizontal(color, coordinates)
    verticalWin = checkWinVertical(color, column)
    diagonalWin = checkWinDiagonal(color, coordinates)

    if color == 'r':
        playerColor = "red"
    else:
        playerColor = "yellow"

    if boardFull:
       messagebox.showinfo("Full Board!", "The board is full! Game over.")
       sys.exit(0)

    elif horizontalWin:

        messagebox.showinfo("Horizontal Win!", "Connect four horizontal win for %s! Game over." %playerColor)
        sys.exit(0)

    elif verticalWin:
        messagebox.showinfo("Vertical Win!","Connect four vertical win for %s! Game Over." %playerColor)
        sys.exit(0)

    elif diagonalWin:
        messagebox.showinfo("Diagonal Win!", "Connect 4 diagonal win for %s! Game over" %playerColor)
        sys.exit(0)

    else:
        pass

    turnCount.append(turnCount[-1] + 1)
    showNextTurn(turnCount[-1])

gameFrame = Frame(root, bg = 'blue', width = 650, height= 30).grid(columnspan = 7)

Label(gameFrame,text= "Player turn: ").grid(row=11,column=0)
Label(gameFrame, image = yellow_img).grid(row=11, column = 1)

for c in range(7):
    for r in range(3,9):
        img = empty_img
        boardImage[c][r-3] = Label(gameFrame, image= img).grid(row=r, column = c)

for r in range(7):
    Button(gameFrame, text = "Drop", bg = 'light blue', activebackground = 'yellow', command = lambda x = r: make_move(x, turnCount)).grid(row= 10, column = r)

root.mainloop()