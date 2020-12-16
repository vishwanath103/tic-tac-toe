import random
import math

class Player:
    def __init__(self, letter):
        # letter is x or o
        self.letter = letter
    
    # we want all players to get their next move given a game
    def get_move(self, game):
        pass

class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        # get a random valid spot for our next move
        square = random.choice(game.available_moves())
        return square

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0:8):')
            try:
                val = int(square)
                if val not in game.available_moves():
                    return ValueError
                valid_square = True
            except ValueError:
                print('Invalid Square. Try Again')

        return val

class GeniusComputerPlayer(Player):
    '''A player which uses minimax algorithm to win the game all times'''
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves) # randomly choose one
        else:
            # get the sqaure based on minimax algorithm
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        # first check if the previous movie is a winner
        # base case
        if state.current_winner == other_player:
            # return position and score
            return {'position': None,
                    'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() * 1)
                    }
        elif not state.empty_squares(): # no empty squares
            return {'position': None, 'score': 0}

        # intialize some dictionaries
        if player == max_player:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}

        for possible_move in state.available_moves():
            # step 1: make a move, try that spot
            state.make_move(possible_move, player)

            # step 2: recurse using minimax algorithm to simulate the game after making a move
            sim_score = self.minimax(state, other_player) # alternate players

            # step 3: undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            # step 4: update the dictionaries if necessary
            if player == max_player:
                # maximize the max_player
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                # minize the other player
                if sim_score['score'] < best['score']:
                    best = sim_score

        return best
