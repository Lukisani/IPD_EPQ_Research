class Player:

    '''General template for each strategy'''

    name = 'Player'

    classifier = {
        'niceness' : 0,
        'forgiveness' : 0,
        'memory_depth' : 0
    }

    def __init__(self, name):
        self.history = [] # tracks its own moves
        self.opponent_history = []
        self.score = 0
    

    def strategy(self, player_move, opponent_move):
        '''
        Defines behaviour for a move. Override in subclasses
        
        Function returns one of two values for each move:
        "C" to cooperate,
        "D" to defect.
        
        '''
        pass


    def reset(self):
        '''Resets the player's state for a new tournament'''
        self.history = []
        self.opponent_history = []
        self.score = 0



class TitforTat(Player):

    name = 'Tit_for_tat'

    classifier = {
        'niceness' : 1,
        'forgiveness' : 1,
        'memory_depth' : 1
    }

    def strategy(self, player_move, opponent_move):

        self.history.append(player_move)
        self.opponent_history.append(opponent_move)

        if not self.opponent_history:
            return 'C'
        return self.opponent_history[-1]


class AlwaysCooperate(Player):

    name = 'Always_cooperate'

    classifier = {
        'niceness' : 1,
        'forgiveness' : 1,
        'memory_depth' : 0
    }

    def strategy(self, player_move, opponent_move):
        
        self.history.append(player_move)
        self.opponent_history.append(opponent_move)

        return 'C'


class AlwaysDefect(Player):

    name = 'Always_defect'

    classifier = {
        'niceness' : 0,
        'forgiveness' : 0,
        'memory_depth' : 0
    }

    def strategy(self, player_move, opponent_move):
        
        self.history.append(player_move)
        self.opponent_history.append(opponent_move)

        return 'D'


class Titfortwotats(Player):
    
    name = 'Tit_for_two_tats'

    classifier = {
        'niceness' : 1,
        'forgiveness' : 1,
        'memory_depth' : 2
    }

    def strategy(self, player_move, opponent_move):
        
        self.history.append(player_move)
        self.opponent_history.append(opponent_move)

        count_opponent_defections = 0
        for move in self.opponent_history[-2:-1]:
            if move == 'D':
                count_opponent_defections += 1

        if not self.opponent_history or count_opponent_defections < 2: