# Tic-Tac-Toe self-learning bot

import numpy as np
from math import inf as infinity
import itertools
import random
from sklearn.preprocessing import minmax_scale

#Initial conditions of game and players

players = ['X','O']
board_state = [[' ', ' ', ' '],
               [' ', ' ', ' '],
               [' ', ' ', ' ']]
# Initialize all possible states with starting value
player = ['X','O',' '] #all possible marks for a square

#nested loops (product(AxB) for all states)
all_board_states = [[list(i[0:3]),list(i[3:6]),list(i[6:10])] for i in itertools.product(player, repeat = 9)]

n_states = len(all_board_states) # total number of board states for: 2 players, 9 spaces - 19683
n_actions = 9
state_values_for_bot_X = np.full((n_states),0.0) # give initial value for all board states of the bot
state_values_for_bot_0 = np.full((n_states),0.0) # give initial value for all board states of the bot

# load the pre-trained states
state_values_for_bot_X = np.loadtxt('trained_values_X_stat.txt', dtype=np.float64)
state_values_for_bot_0 = np.loadtxt('trained_values_O_stat.txt', dtype=np.float64)


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

states_dict = {}
# get value for the current state ( put 1 for WIN\for LOSS is -1\ for draw no change)
for i in range(n_states):
    states_dict[i] = all_board_states[i]
    winner,_ = checkForWin(all_board_states[i])
    if winner == 'X':
        state_values_for_bot_X[i] = 1  # X won the game
        state_values_for_bot_0[i] = -1
    elif winner == '0':
        state_values_for_bot_0[i] = 1  # O won the game
        state_values_for_bot_X[i] = -1




# Update the state based on : c_state = c_state + alpha*(n_state-c_state) , alpha is rate of learning
def newStateValueForX(cstate_idx, nstate_idx, alpha):
    new_val = state_values_for_bot_X[cstate_idx] + alpha * (
            state_values_for_bot_X[nstate_idx] - state_values_for_bot_X[cstate_idx])
    state_values_for_bot_X[nstate_idx] = new_val


def newStateValueFor0(cstate_idx, nstate_idx, alpha):
    new_val = state_values_for_bot_0[cstate_idx] + alpha * (
            state_values_for_bot_0[nstate_idx] - state_values_for_bot_0[cstate_idx])
    state_values_for_bot_0[nstate_idx] = new_val


# Main learning algo functions
def bestMove_Minimax(state, player):
    '''
    Minimax Algorithm
    '''
    winner_loser, done = checkForWin(state)
    if done == "Done" and winner_loser == 'O':
        return 1
    elif done == "Done" and winner_loser == 'X':
        return -1
    elif done == "Draw":  # Draw condition
        return 0

    moves = []
    empty_squares = []
    for i in range(3):
        for j in range(3):
            if state[i][j] is ' ':
                empty_squares.append(i * 3 + (j + 1))

    for empty_square in empty_squares:
        move = {}
        move['index'] = empty_square
        new_state = copyGameState(state)
        playMove(new_state, player, empty_square)

        if player == 'O':  # If AI
            result = bestMove_Minimax(new_state, 'X')  # make more depth tree for opponent
            move['score'] = result
        else:
            result = bestMove_Minimax(new_state, 'O')  # make more depth tree for bot
            move['score'] = result

        moves.append(move)

    # Find best move
    best_move = None
    if player == 'O':  # If bot player
        best = -infinity
        for move in moves:
            if move['score'] > best:
                best = move['score']
                best_move = move['index']
    else:
        best = infinity
        for move in moves:
            if move['score'] < best:
                best = move['score']
                best_move = move['index']

    return best_move

def bestMove(state, player, epsilon):
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
        nstate = copyGameState(state) #gets the new state of the board
        playMove(nstate, player, empty_square)
        nstate_idx = list(states_dict.keys())[list(states_dict.values()).index(nstate)] #get index for new state
        if player == 'X':
            cstate_values.append(state_values_for_bot_X[nstate_idx])
        else:
            cstate_values.append(state_values_for_bot_0[nstate_idx])

    #print('Move values = ' + str(cstate_values))
    best_move_idx = np.argmax(cstate_values)

    if np.random.uniform(0, 1) <= epsilon:  # Exploration
        best_move = random.choice(empty_squares)
        epsilon *= 0.99
    else:  # Exploitation
        best_move = moves[best_move_idx]
    return best_move

def playMove(state, player, square_num):
    if state[int((square_num-1)/3)][(square_num-1)%3] is ' ':
        state[int((square_num-1)/3)][(square_num-1)%3] = player
    else:
        square_num = int(input("Square is not empty! Choose again: "))
        playMove(state, player, square_num)

def copyGameState(state):
    new_state = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
    for i in range(3):
        for j in range(3):
            new_state[i][j] = state[i][j]
    return new_state

def printBoard(board_state):
    print(" " + board_state[0][0] + ' | ' + board_state[0][1] + ' | ' + board_state[0][2])
    print('---+---+---')
    print(" " + board_state[1][0] + ' | ' + board_state[1][1] + ' | ' + board_state[1][2])
    print('---+---+---')
    print(" " + board_state[2][0] + ' | ' + board_state[2][1] + ' | ' + board_state[2][2])
    print("\n")

#save the post-training states
def save_bot():
    bot_X_scaled = minmax_scale(state_values_for_bot_X)
    bot_0_scaled = minmax_scale(state_values_for_bot_0)

    np.savetxt('trained_values_X_stat.txt', bot_X_scaled,fmt = '%.6f')
    np.savetxt('trained_values_O_stat.txt', bot_0_scaled,fmt = '%.6f')
    print("SAVED")

#Training
def training(num_iterations):
    alpha = 0.1
    epsilon = 0.3
    i = 2
    for iteration in range(num_iterations):
        board_state = [[' ', ' ', ' '],
                  [' ', ' ', ' '],
                  [' ', ' ', ' ']]
        current_state = "Not Done"
        winner = None

        print("\nIteration: " + str(iteration))

        if iteration%2 == 0:
            current_player_idx = 1
        else:
            current_player_idx = 0

        while current_state == "Not Done":
            cstate_idx = list(states_dict.keys())[list(states_dict.values()).index(board_state)]
            if current_player_idx == 1:  # AI_X's turn
                square_choice = bestMove_Minimax(board_state, players[current_player_idx])
                playMove(board_state, players[current_player_idx], square_choice)
                nstate_idx = list(states_dict.keys())[list(states_dict.values()).index(board_state)]

            else:  # AI_O's turn
                square_choice = bestMove(board_state, players[current_player_idx],epsilon)
                playMove(board_state, players[current_player_idx], square_choice)
                nstate_idx = list(states_dict.keys())[list(states_dict.values()).index(board_state)]

            #calculating the new state value for each player state
            newStateValueForX(cstate_idx, nstate_idx, alpha)
            newStateValueFor0(cstate_idx, nstate_idx, alpha)
            winner, current_state = checkForWin(board_state) #tells if we have a winner and who it is

            if winner == None:
                if current_state == "Not Done":
                    current_player_idx = (current_player_idx + 1) % 2
                else:
                    continue
            else:
                continue

        if iteration == 10**i:
            save_bot()
            i+=1

    print('Training Complete!')


# load the pre-trained states
state_values_for_bot_X = np.loadtxt('trained_values_X_stat.txt', dtype=np.float64)
state_values_for_bot_0 = np.loadtxt('trained_values_O_stat.txt', dtype=np.float64)
training(1000)
save_bot()


