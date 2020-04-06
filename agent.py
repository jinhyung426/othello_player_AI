"""
An AI player for Othello.
"""

import random
import sys
import time

cached = {}

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)

# Method to compute utility value of terminal state
def compute_utility(board, color):
    result = get_score(board)
    dark = result[0]
    white = result[1]
    if color == 1:
        return dark - white
    else:
        return white - dark

# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    #IMPLEMENT
    return 0 #change this!x

############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    if color == 1:
        opponent = 2
    else:
        opponent = 1
    moves = get_possible_moves(board, opponent)

    if moves == [] or limit == 0:
        return (-1, -1), compute_utility(board, color)

    if limit == 0:
        return compute_utility(board, color)

    min_utility = float('inf')

    for i in range(len(moves)):
        temp_board = play_move(board, opponent, moves[i][0], moves[i][1])


        if caching == 1:
            if temp_board in cached:
                temp_utility = cached[temp_board]
            else:
                temp_move, temp_utility = minimax_max_node(temp_board, color, limit - 1, caching)
                cached[temp_board] = temp_utility

        else:
            temp_move, temp_utility = minimax_max_node(temp_board, color, limit - 1, caching)


        if temp_utility < min_utility:
            min_utility = temp_utility
            min_move = moves[i]

    return min_move, min_utility

def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility

    moves = get_possible_moves(board, color)
    if moves == [] or limit == 0:
        return (-1, -1), compute_utility(board, color)

    max_utility = - float('inf')

    for i in range(len(moves)):
        temp_board = play_move(board, color, moves[i][0], moves[i][1])

        if caching == 1:
            if temp_board in cached:
                temp_utility = cached[temp_board]
            else:
                temp_move, temp_utility = minimax_min_node(temp_board, color, limit - 1, caching)
                cached[temp_board] = temp_utility
        else:
            temp_move, temp_utility = minimax_min_node(temp_board, color, limit - 1, caching)


        if temp_utility > max_utility:
            max_utility = temp_utility
            max_move = moves[i]

    return max_move, max_utility

def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    """
    cached = {}
    move, utility = minimax_max_node(board, color, limit, caching)
    return move

def takeSecond(elem):
    return elem[1]

############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):

    if color == 1:
        opponent = 2
    else:
        opponent = 1
    moves = get_possible_moves(board, opponent)

    if moves == [] or limit == 0:
        return (-1, -1), compute_utility(board, color)

    if limit == 0:
        return compute_utility(board, color)

    min_utility = float('inf')
    successors = []

    for i in range(len(moves)):
        temp_board = play_move(board, opponent, moves[i][0], moves[i][1])
        successors.append((temp_board, compute_utility(temp_board, color)))

    if ordering == 1:
        successors.sort(key=takeSecond, reverse=True)

    for i in range(len(successors)):

        if caching == 1:
            if successors[i][0] in cached:
                temp_utility = cached[successors[i][0]]
            else:
                temp_move, temp_utility = alphabeta_max_node(successors[i][0],
                                                             color, alpha, beta,
                                                             limit - 1, caching,
                                                             ordering)
                cached[successors[i][0]] = temp_utility
        else:
            temp_move, temp_utility = alphabeta_max_node(successors[i][0], color, alpha, beta, limit - 1, caching, ordering)

        if temp_utility < min_utility:
            min_utility = temp_utility
            min_move = moves[i]

        if beta > min_utility:
            beta = min_utility
            if beta <= alpha:
                break

    return min_move, min_utility


def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):

    moves = get_possible_moves(board, color)
    if moves == [] or limit == 0:
        return (-1, -1), compute_utility(board, color)

    max_utility = - float('inf')
    successors = []

    for i in range(len(moves)):
        temp_board = play_move(board, color, moves[i][0], moves[i][1])
        successors.append((temp_board, compute_utility(temp_board, color)))

    if ordering == 1:
        successors.sort(key=takeSecond, reverse=True)

    for i in range(len(successors)):

        if caching == 1:
            if successors[i][0] in cached:
                temp_utility = cached[successors[i][0]]
            else:
                temp_move, temp_utility = alphabeta_min_node(successors[i][0],
                                                             color, alpha, beta,
                                                             limit - 1, caching,
                                                             ordering)
                cached[successors[i][0]] = temp_utility
        else:
            temp_move, temp_utility = alphabeta_min_node(successors[i][0], color, alpha, beta, limit - 1, caching, ordering)

        if temp_utility > max_utility:
            max_utility = temp_utility
            max_move = moves[i]

        if alpha < max_utility:
            alpha = max_utility
            if beta <= alpha:
                break

    return max_move, max_utility

def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations.
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations.
    """
    cached = {}
    move, utility = alphabeta_max_node(board, color, - float('inf'), float('inf'), limit, caching, ordering)
    return move

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")

    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light.
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
            # object. The format is a list of rows. The
            # squares in each row are represented by
            # 0 : empty square
            # 1 : dark disk (player 1)
            # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)

            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
