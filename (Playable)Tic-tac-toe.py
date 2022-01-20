# Tic-Tac-Toe human - bot
import numpy as np
from math import inf as infinity
import itertools
import random

#Initial conditions of game and players
board_state = [[' ',' ',' '],
              [' ',' ',' '],
              [' ',' ',' ']]
players = ['X','O']
# Initialize all possible states with starting value
player = ['X','O',' '] #all possible marks for a square
#nested loops (product(AxB) for all states)
all_board_states = [[list(i[0:3]),list(i[3:6]),list(i[6:10])] for i in itertools.product(player, repeat = 9)]
n_states = len(all_board_states) # total number of board states for: 2 players, 9 spaces - 19683
states_dict = {}
for i in range(n_states):
   states_dict[i] = all_board_states[i]

def checkForWin(board_state):
    # Check horizontal
    if (board_state[0][0] == board_state[0][1] and board_state[0][1] == board_state[0][2] and board_state[0][0] is not ' '):
        return board_state[0][0], "Done"
    if (board_state[1][0] == board_state[1][1] and board_state[1][1] == board_state[1][2] and board_state[1][0] is not ' '):
        return board_state[1][0], "Done"
    if (board_state[2][0] == board_state[2][1] and board_state[2][1] == board_state[2][2] and board_state[2][0] is not ' '):
        return board_state[2][0], "Done"

    # Check vertical
    if (board_state[0][0] == board_state[1][0] and board_state[1][0] == board_state[2][0] and board_state[0][0] is not ' '):
        return board_state[0][0], "Done"
    if (board_state[0][1] == board_state[1][1] and board_state[1][1] == board_state[2][1] and board_state[0][1] is not ' '):
        return board_state[0][1], "Done"
    if (board_state[0][2] == board_state[1][2] and board_state[1][2] == board_state[2][2] and board_state[0][2] is not ' '):
        return board_state[0][2], "Done"

    # Check diagonals
    if (board_state[0][0] == board_state[1][1] and board_state[1][1] == board_state[2][2] and board_state[0][0] is not ' '):
        return board_state[1][1], "Done"
    if (board_state[2][0] == board_state[1][1] and board_state[1][1] == board_state[0][2] and board_state[2][0] is not ' '):
        return board_state[1][1], "Done"

    # Check for draw
    draw_flag = 1
    for i in range(3):
        for j in range(3):
            if board_state[i][j] is ' ':
                draw_flag = 0
    if draw_flag is 1:
        return None, "Draw"
    return None, "Not Done"

def bestMove(state, player):
    moves = []
    cstate_values = []
    empty_squares = []

    # value for all empty_squares
    for i in range(3):
        for j in range(3):
            if state[i][j] == ' ':
                empty_squares.append(i * 3 + (j + 1))
               # print(empty_squares)

    for empty_square in empty_squares:
        moves.append(empty_square)
        nstate = copyGameState(state)
        playMove(nstate, player, empty_square)
        nstate_idx = list(states_dict.keys())[list(states_dict.values()).index(nstate)]
        if player == 'X':
            cstate_values.append(state_values_for_bot_X[nstate_idx])
        else:
            cstate_values.append(state_values_for_bot_0[nstate_idx])

    print('Possible moves = ' + str(moves))
    print('Move score values = ' + str(cstate_values))
    best_move_idx = np.argmax(cstate_values)
    best_move = moves[best_move_idx]
    return best_move

def playMove(state, player, square_num):
    if state[int((square_num-1)/3)][(square_num-1)%3] is ' ':
        state[int((square_num-1)/3)][(square_num-1)%3] = player
    else:
        square_num = int(input("Square is not empty! Choose again(1 to 9): "))
        playMove(state, player, square_num)

def copyGameState(state):
    new_state = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
    for i in range(3):
        for j in range(3):
            new_state[i][j] = state[i][j]
    return new_state

def printBoard(board_state):
    print("Playing board" + "      " + "Reference board")
    print(" " + board_state[0][0] + ' | ' + board_state[0][1] + ' | ' + board_state[0][2] + "           " + "1" + ' | ' + "2" + ' | ' + "3")
    print('---+---+---' + "         " + '---+---+---')
    print(" " + board_state[1][0] + ' | ' + board_state[1][1] + ' | ' + board_state[1][2] + "           " + "4" + ' | ' + "5" + ' | ' + "6")
    print('---+---+---' + "         " + '---+---+---')
    print(" " + board_state[2][0] + ' | ' + board_state[2][1] + ' | ' + board_state[2][2] + "           " + "7" + ' | ' + "8" + ' | ' + "9")

def playGame():

    play = 'y'
    while play == 'y':
        board_state = [[' ', ' ', ' '],
                      [' ', ' ', ' '],
                      [' ', ' ', ' ']]
        current_state = "Not Done"
        print("\nNew Game!")

        printBoard(board_state)
        player_choice = None
        while player_choice == None:
            player_choice = input("Choose which player goes first - X(human) or O(R.Danilo):").lower()
        winner = None

        if player_choice == 'x':
            current_player_idx = 0
        else:
            current_player_idx = 1

        while current_state == "Not Done":
            if current_player_idx == 0:  # Human's turn
                choice = int(input("Choose where to play (1 to 9): "))
                playMove(board_state, players[current_player_idx], choice)

            else:  # bot's turn
                choice = bestMove(board_state, players[current_player_idx])
                playMove(board_state, players[current_player_idx], choice)
                print("R.Danilo plays move: " + str(choice))

            printBoard(board_state)
            winner, current_state = checkForWin(board_state)
            if winner is not None:
                if str(winner) == "X":
                    print("Congratulations! You won!")
                else:
                    print("R.Danilo won!")
            else:
                current_player_idx = (current_player_idx + 1) % 2

            if current_state is "Draw":
                print("It's a draw!")
        play = input('Want to try again?(Y/N) : ').lower()
    print('Well played! Hope to see you again!')

#load the trained bot and start the game
state_values_for_bot_X = np.loadtxt('trained_values_X_stat.txt', dtype=np.float64)
state_values_for_bot_0 = np.loadtxt('trained_values_O_stat.txt', dtype=np.float64)

playGame()