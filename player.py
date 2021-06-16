import copy
import random
import time



class MyPlayer():

    """
    AHHHH(battle cry)
    """

    """
    Main player class for the AI.

    The algorithm utilizes MiniMax with Alpha-Beta pruning to look ahead certain amounts of moves, in this case, 3.
    Once reached at the leaf nodes, the heuristic functions generates a score for that particular node, that score
    gets passed back through recrusive means and further leaf node scores are generated and so on.

    The final output value is a {tuple} generated from the move function, that represents the current best move.
    
    """

    def __init__(self, my_color, opponent_color, board_size=8):
        self.name = 'alimoha1'
        self.my_color = my_color
        self.opponent_color = opponent_color
        self.board_size = board_size
        self.min = float("-inf")
        self.max = float("inf")

    def move(self, board):

        """
        This function runs through the allowed moves and determines the best choice.

        :param board: The current state of the board.
        :return: a tuple; the best possible co-ordinates to move to.
        """
        valid_moves = self.get_all_valid_moves(self.my_color, board)
        if valid_moves == None:
            return None
        n = self.board_size
        Best_choice = [0,self.min] # ID, score
        # Scan through the legal moves available and replace Best_choice variable with the highest score possible.
        for move in valid_moves:
            choice = self.algorithm(move, board,self.my_color, 3, self.min, self.max, True)
            if choice > Best_choice[1]:
                Best_choice[1] = choice
                Best_choice[0] = move
        return Best_choice[0]


    def algorithm(self, move, board, player, depth, alpha, beta, maximizingPlayer):
        """
        The main algorithm for "predicting" the future. This algorithm helps the main heuristic function by
        looking forward into the game and determining if the choice chosen is truly the best or not.

        :param move: {list} of the co-ordinates of the position to evaluate.
        :param board: {nested_list} of the current state of the board.
        :param player: {int} value representing a player's color.
        :param depth: {int} value representing how many moves ahead to look to.
        :param alpha: {int} or {float} value representing alpha value.
        :param beta: {int} or {float} value representing beta value.
        :param maximizingPlayer: {bool} True if maximizing player, False if not.
        :return: the score of the move given.
        """
        if depth == 0 or not self.is_it_bounded(move[0],move[1]):
            # if algorithm has reached the leaf values, return the score.
            return self.bad_heuristic(board)
        valid_moves = self.get_all_valid_moves(player, board)
        if valid_moves == None:
            # This turn is invalid; return initial value.
            return self.bad_heuristic(board)

        if maximizingPlayer: # maximizing the AI
            v = self.min
            for move in valid_moves:
                boardTemp = copy.deepcopy(board)
                boardTemp = self.play_move(boardTemp, move, player)
                v = max(v, self.algorithm(move, boardTemp, player, depth - 1, alpha, beta, False)) # recursive call.
                alpha = max(alpha, v)
                if beta <= alpha:
                    break

            return v

        else:  # minimizing opponent
            v = self.max
            for move in valid_moves:
                boardTemp = copy.deepcopy(board)
                boardTemp = self.play_move(boardTemp, move,player)
                v = min(v, self.algorithm(move, boardTemp, player, depth - 1, alpha, beta, True))
                beta = min(beta, v)
                if beta <= alpha:
                    break


            return v

    def bad_heuristic(self, board):
        """
        Generates heuristic value for the given board.
        Faster but poor quality.
        :param board: current state of the board
        :return: Score
        """
        b = self.board_size
        Score = 0
        for x in range(b):
            for y in range(b):
                if board[x][y] == self.my_color:
                    # Corner check
                    if [x,y] == [0,0] or [x,y] == [0,b-1] or [x,y] == [b-1,b-1] or [x,y] == [b-1,0]:
                        Score += 4
                    # General ownership.
                    else:
                        Score += 1

        return Score


    def good_heuristic(self, board):
        """
        Using this heuristic crosses the time limit, as such, could not use it.

        The main heuristic function of the AI. Determines the worth of a position.
        The score calculated is relative to max player (the AI).
        Good score = better choice for AI (max)
        Bad score = better choice for Opponent (min)
        There are three factors that will be taken into account, them being:
        1) Corners - 60%
        2) Mobility - 35%
        3) Parity - 5%
        The MaxScore calculates the score for the AI
        The MinSCore for the opponent
        Final score = MaxScore - MinScore

        :param board:
        :return: integer; the score of the position.
        """

        n = self.board_size
        MaxCor, MaxMob, MaxPar = 0,0,0
        MinCor, MinMob, MinPar = 0,0,0
        Corners = [[0,0],[0,n-1],[n-1,n-1],[n-1,0]]
        for x in range(n):
            for y in range(n):
                if board[x][y] == self.my_color:
                    if [x,y] in Corners:
                        MaxCor += 1
                        MaxPar += 1
                    else:
                        MaxPar += 1
                elif board[x][y] == self.opponent_color:
                    if [x,y] in Corners:
                        MinCor += 1
                        MinPar += 1
                    else:
                        MinPar += 1
                else: # Empty space; check for mobility.
                    if self.__is_correct_move([x, y], board, self.my_color):
                        MaxMob += 1
                    if self.__is_correct_move([x, y], board, self.opponent_color):
                        MaxMob += 1

        MaxScore = (60/100)*MaxCor + (35/100)*MaxMob +(5/100)*MaxPar
        MinScore = (60/100)*MinCor + (35/100)*MinMob + (5/100)*MinPar

        Final_score = MaxScore - MinScore

        return Final_score

########## Auxillary functions (for simulations & assistance) #########################################################


    def get_all_valid_moves(self, players_color, board):
        '''
        Generates a list of legal moves.

        :param players_color: {int} of player color, board: {list} of the current state of the board.
        :return: {list} of valid moves
        '''
        valid_moves = []
        for x in range(self.board_size):
            for y in range(self.board_size):
                if ((board[x][y] == -1) and
                        self.__is_correct_move([x, y], board, players_color)):
                    valid_moves.append((x, y))

        if len(valid_moves) <= 0:
            return None
        return valid_moves

    def __is_correct_move(self, move, board, players_color):
        '''
        :param move: {list} of {int} for position
        :param players_color: {int}
        :return: {bool}
        '''
        if board[move[0]][move[1]] == -1:
            dx = [-1, -1, -1, 0, 1, 1, 1, 0]
            dy = [-1, 0, 1, 1, 1, 0, -1, -1]
            for i in range(len(dx)):
                if self.__confirm_direction(move, dx[i], dy[i], players_color, board):
                    return True

        return False

    def __confirm_direction(self, move, dx, dy, players_color, board):
        '''
        Looks into direction [dx,dy] to find if the move in this direction
         is correct. This means that first stone in the direction is oponents
         and last stone is players.
        :param move: position where the move is made [x,y]
        :param dx: x direction of the search
        :param dy: y direction of the search
        :param player: player that made the move
        :return: True if move in this direction is correct
        '''

        if players_color == self.my_color:
            opponents_color = self.opponent_color
        else:
            opponents_color = self.my_color
        posx = move[0] + dx
        posy = move[1] + dy
        if self.is_it_bounded(posx, posy):
            if board[posx][posy] == opponents_color:
                while self.is_it_bounded(posx, posy):
                    posx += dx
                    posy += dy
                    if self.is_it_bounded(posx, posy):
                        if board[posx][posy] == -1:
                            return False
                        if board[posx][posy] == players_color:
                            return True

        return False

    def is_it_bounded(self, posx, posy):
        '''
        Check if position is in the limits of the board and non-zero.
        :param posx: {int}
        :param posy: {int}
        :return: {bool}
        '''
        return ((posx >= 0) and
                (posx < self.board_size) and
                (posy >= 0) and
                (posy < self.board_size))


    def play_move(self, board, move, players_color):
        '''
        :param move: {list} of {int} for position where the move is made
        :param players_color: {int} color of who made the move
        :return: {None}
        '''
        board[move[0]][move[1]] = players_color
        dx = [-1, -1, -1, 0, 1, 1, 1, 0]
        dy = [-1, 0, 1, 1, 1, 0, -1, -1]
        for i in range(len(dx)):
            if self.__confirm_direction(move, dx[i], dy[i], players_color, board):
                self.__change_stones_in_direction(board, move, dx[i], dy[i], players_color)
        return board


    def can_play(self, players_color):
        '''
        :param players_color: {int} of player color
        :return: True if there is a possible move for player
        '''
        for x in range(self.board_size):
            for y in range(self.board_size):
                if self.is_correct_move([x, y], players_color):
                    return True

        return False


    def __change_stones_in_direction(self, board, move, dx, dy, players_color):
        '''
        :param move: position as a {list} of {int}
        :param dx: {int}
        :param dy: {int}
        :param players_color: {int} of player color
        :return: {None}
        '''
        posx = move[0]+dx
        posy = move[1]+dy
        while (not(board[posx][posy] == players_color)):
            board[posx][posy] = players_color
            posx += dx
            posy += dy




