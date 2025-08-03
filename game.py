from tkinter import *
from tkinter.messagebox import *
from time import sleep
import random

# @us10f




# Game Functions and variables -------------------------------------------------------------------------------------------------------------------------

# game dictionary represent 3x3
# keys 1–9 represent cells, values: 0 (empty), 1 (X), 2 (O)
board = {i:0 for i in range(1,10)} 

# status indicates whether a game is currently active
# 'off' = not started, 'on' = game in progress
status = 'off' 

# 1 = Player X, 2 = Player O
turn = 1 


# reset all game components and visual elements
# called after the game ends and the user chooses to play again.
# it:
# - clears the board dictionary
# - resets game status and turn
# - clears the text from each GUI cell
# - resets player and marker selections to default
def refeshComponents():
    global board, status, turn, gridOfCells
    global selectPlayer_ctrlVariable, selectMarker_ctrlVariable, selectReady_ctrlVariable
    
    # reset the game board dictionary to all empty cells
    board = {i: 0 for i in range(1, 10)}
    
    # reset game status to off (not in progress)
    status = 'off'
    
    # set turn back to Player 1 (X)
    turn = 1
    
    # reset visual cells
    for i in range(1, 10):
        cell = gridOfCells[i]
        cell.config(text='')

    # set default options
    selectPlayer_ctrlVariable.set(1) 
    selectMarker_ctrlVariable.set(1) 
    selectReady_ctrlVariable.set(False)





# checks if there is a winner or the game is a tie.
# returns:
# - 1 or 2 if player 1 (X) or player 2 (O) wins
# - 0 if the game is a tie
# - None if the game is still ongoing (there is empty cells)
def checkWin(board):
        
    winning_cases = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9],  
        [1, 4, 7], [2, 5, 8], [3, 6, 9],  
        [1, 5, 9], [3, 5, 7]              
    ]
    for case in winning_cases:
        values = [board[pos] for pos in case]
        if values[0] != 0 and values[0] == values[1] and values[1] == values[2] :
            return values[0]  # return winner identifer

    # check if there is remaining cells can be played on it
    for key, value in board.items():
        if value == 0:  # still can be played
            return None

    return 0 # tide case


# this function is called after every move to check for a win or tie.
# if the game ends:
# - displays the result 
# - ask if the user want to play one more time ?
# - if yes,  resets everything and returns True
# - if no, it quits the application
# if the game is still ongoing, returns False
# هذي تشتغل مع الدالة 
# CheckWin(board)
def take_action_as_checkWin():
    global board
    winner = checkWin(board)
    if winner == 1 or winner == 2:
        showinfo('Winner', f'{'X' if winner == 1 else 'O'} Won !!!')
        if not askyesno('Continue ?', 'Would you like to play another game ?'):
            top.quit()
        else:
            refeshComponents()
        return True
    elif winner == 0:
        showinfo('Tide', 'no one win')
        if not askyesno('Continue ?', 'Would you like to play another game ?'):
            top.quit()
        else:
            refeshComponents()
        return True
    return False 
    

# طريقة البحث عن افضل موقع للحركة القادمة
# 1. ابحث عن اي خلية تخلي الكمبيوتر يفوز
# 2. اذا السابقة ما وجدت فابحث عن نقطة تخلي المستحدم يفوز
# 3. اذا لم يجد السابقات العب بالوسط الخلية خمسة
# 4. اذا ما وجدت السابقة العب باحدى الزواية
# ارجع الموقع الصحيح اللي لقيناه من عملية البحث
def computer_playes(board_copy, main_userTurnMarker, oponent_turnMarker):
    #1
    for index in range(1, 10):
        if board_copy[index] != 0:
            continue
        board_copy[index] = oponent_turnMarker
        if checkWin(board_copy) == oponent_turnMarker:
            board_copy[index] = 0
            return index
        board_copy[index] = 0

    #2
    for index in range(1, 10):
        if board_copy[index] != 0:
            continue
        board_copy[index] = main_userTurnMarker
        if checkWin(board_copy) == main_userTurnMarker:
            board_copy[index] = 0
            return index
        board_copy[index] = 0


    #3
    if board_copy[5] == 0:
        return 5

    #4.
    for indx in [1, 3, 7, 9]:
        if board_copy[indx] == 0:
            return indx
    for key,value in board_copy.items():
        if value == 0:
            return key
        
    return None


# handle the complete move of the computer
# 1. call `computer_playes` to get the best move
# 2. updates the board at the selected index with the computer’s marker (1 for X, 2 for O) and visualize it
# 3. call `take_action_as_checkWin` to check if the game is over
def full_computerMovement(board, main_userTurnMarker, oponent_turnMarker):
        index = computer_playes(board_copy=board.copy(), main_userTurnMarker=main_userTurnMarker, oponent_turnMarker=oponent_turnMarker) 
        board[index] = oponent_turnMarker         
        gridOfCells[index].config(text=f'{'X' if oponent_turnMarker == 1 else 'O'}')
        if take_action_as_checkWin():
            return True
        return False

# function for GUI -------------------------------------------------------------------------------------------------------------------------


# called when the "Start" button is pressed.
# check if the game is already on but the user press start
# in that case show error using messagebox
# check if the user has marked ready
# if already playing, shows an error
# if not ready, shows a warning.
# starts the game by setting status = 'on' and defining which player starts (if computer randomly generate) (if user let X start).
def startGame():
    global status
    global turn
    ready = selectReady_ctrlVariable.get()
    
    # play ongoning and user presses play button
    if status == 'on':
        showerror('error','you are currently playing a game')
        return
    
    if ready:
        status = 'on'
        turn = random.randint(1,2) if selectPlayer_ctrlVariable.get() == 1 else 1
        print(turn)
        playCell(5, True) # to let the computer plays if he is the first one
    else:
        showinfo('Not ready', 'You are not ready to play the game, make sure to check the yes radio')    

# runs whenever a player clicks a cell.
# it checks if the move is allowed, updates the board,
# switches turns, if playing with another player
# let computer play without switching turn, if playing with computer
# it also checks if someone has won after each move.
# - cell: cell to be marked
# - firstMove: when the first move of the game is computer, so this paramter is needed only on first move
# function startGame will call it with True and cell 5 (no matter which cell)
def playCell(cell, firstMove=False):
    global status
    global turn
    global board
    
    if board[cell] != 0:
        return
    
    # if cell is clicked but the game is not started
    if status != 'on':
        return
    
    # get the opponent type: 1 = computer, 2 = player 2
    opponent = selectPlayer_ctrlVariable.get() 
    
    # marker selected by main player: 1 = X, 2 = O
    main_userTurnMarker = selectMarker_ctrlVariable.get() 
    
    # assign opponent's marker: the opposite of the main player
    oponent_turnMarker = 1 if main_userTurnMarker == 2 else 2
    
    print(f"opponent: {opponent}, main_userTurnMarker: {main_userTurnMarker}, oponent_turnMarker: {oponent_turnMarker}, turn: {turn}")

    if opponent == 1 and turn == oponent_turnMarker:
        full_computerMovement(board, main_userTurnMarker, oponent_turnMarker)
        turn = 1 if turn == 2 else 2
        return
    elif firstMove:
        return
    
    board[cell] = turn
    gridOfCells[cell].config(text=f'{'X' if turn == 1 else 'O'}')
    
    
    if take_action_as_checkWin(): 
        return
    
    
    if opponent == 1: #computer !!!
        if full_computerMovement(board, main_userTurnMarker, oponent_turnMarker):
            return
    else:
        turn = 1 if turn == 2 else 2
                     
  
# GUI components -------------------------------------------------------------------------------------------------------------------------

top = Tk()
top.title('Tic-Tac-Toe')
top.geometry('500x450')
top.resizable(False,False)

# play with       o Computer    o Player 2
selectPlayer_label = Label(top,text='Play With                  ')
selectPlayer_ctrlVariable = IntVar() # 1 --- > Computer, 2 --- > Player 2
selectPlayer_ctrlVariable.set(1)
selectPlayer_radio1 = Radiobutton(top, text='Computer', variable=selectPlayer_ctrlVariable, value=1)
selectPlayer_radio2 = Radiobutton(top, text='Player 2', variable=selectPlayer_ctrlVariable, value=2)

selectPlayer_label.grid(row=0, column=0, sticky='w', padx=30)
selectPlayer_radio1.grid(row=0, column=1)
selectPlayer_radio2.grid(row=0, column=2)


# select       o X    o O
selectMarker_label = Label(top, text='Select', padx='35')
selectMarker_ctrlVariable = IntVar() # 1 --- > X, 2 --- > O
selectMarker_ctrlVariable.set(1)
selectMarker_radio1 = Radiobutton(top, text='X', variable=selectMarker_ctrlVariable, value=1)
selectMarker_radio2 = Radiobutton(top, text='O', variable=selectMarker_ctrlVariable, value=2)

selectMarker_label.grid(row=3, column=0, sticky='w')
selectMarker_radio1.grid(row=3, column=1)
selectMarker_radio2.grid(row=3, column=2)

# ready to start the game ?
# if no, pressing start button will prevent you from start the game !!
# Start the game o Yes    o No
selectReady_label = Label(top, text='Start the game')
selectReady_ctrlVariable = BooleanVar()
selectReady_ctrlVariable.set(False)
selectReady_radio1 = Radiobutton(top, text='Yes', variable=selectReady_ctrlVariable, value=True)
selectReady_radio2 = Radiobutton(top, text='No', variable=selectReady_ctrlVariable, value=False)


selectReady_label.grid(row=5, column=0, sticky='w', padx=25)
selectReady_radio1.grid(row=5, column=1)
selectReady_radio2.grid(row=5, column=2)

# start button
startButton = Button(top, text='Start', command=startGame, width=8,height=3, relief='raised')
startButton.grid(row=7, column=3, pady=13)

# grid of celles (that affect the dictonary board of the game)
gridOfCells = [Label(top, text='', height=5, width=12, bg='gray', relief='raised') for i in range(1,10)]
gridOfCells.insert(0,'xxxx') # just to normalize array indices to be 1,2,3,4,5,6,7,8,9 corresponding to each cell of the board

index = 1
for i in range(15,18):
    for j in range(1,4):
        gridOfCells[index].grid(row=i, column=j)
        index += 1
        
for i in range(1,10):
    gridOfCells[i].bind('<Button-1>', lambda x, cell=i: playCell(cell))

        
top.mainloop()


