import random

class Player:

    '''General template for each strategy'''

    name = 'Player'

    classifier = {
        'niceness' : 0,
        'forgiveness' : 0,
        'memory_depth' : 0
    }

    def __init__(self):
        self.history = [] # tracks its own moves
        self.score = 0
    

    def strategy(self, opponent_history):
        '''
        Defines behaviour for a move. Override in subclasses
        
        Function returns one of two values for each move:
        "C" to cooperate,
        "D" to defect.
        
        '''
        raise NotImplementedError()


    def reset(self):
        '''Resets the player's state for a new tournament'''
        self.history = []
        self.score = 0



class TitForTat(Player):

    name = 'Tit_for_tat'

    '''Cooperates on the first move, otherwise returns opponent's last move'''
    
    classifier = {
        'niceness' : 1,
        'forgiveness' : 1,
        'memory_depth' : 1
    }

    def strategy(self, opponent_history):

        if not opponent_history:
            return 'C'
        return opponent_history[-1]


class AlwaysCooperate(Player):

    name = 'Always_cooperate'

    '''Always cooperates'''
    
    classifier = {
        'niceness' : 1,
        'forgiveness' : 1,
        'memory_depth' : 0
    }

    def strategy(self, opponent_history):

        return 'C'


class AlwaysDefect(Player):

    name = 'Always_defect'

    '''Always defects'''
    
    classifier = {
        'niceness' : 0,
        'forgiveness' : 0,
        'memory_depth' : 0
    }

    def strategy(self, opponent_history):

        return 'D'


class TitForTwoTats(Player):
    
    name = 'Tit_for_two_tats'

    '''Cooperate on first move, otherwise only defects if opponent defects twice in a row'''
    
    classifier = {
        'niceness' : 1,
        'forgiveness' : .5,
        'memory_depth' : 2
    }

    def strategy(self, opponent_history):

        '''Counts how many defections in last 2 moves'''
        count_opponent_defections = 0
        for move in opponent_history[-2:]:
            if move == 'D':
                count_opponent_defections += 1

        if not opponent_history or count_opponent_defections < 2:
            return 'C'
        else:
            return 'D'

class Random(Player):

    name = 'Random'

    '''Cooperates or defects randomly'''

    classifier = {
        'niceness' : None,
        'forgiveness' : None,
        'memory_depth' : 0
    }

    def strategy(self, opponent_history):
        
        return random.choice(['C', 'D'])

class Alternator(Player):

    name = 'Alternator'

    '''Alternates between cooperating and defecting'''

    classifier = {
        'niceness' : None,
        'forgiveness' : None,
        'memory_depth' : 0
    }

    def strategy(self, opponent_history):
        
        if len(opponent_history) % 2 == 0:
            return 'C'
        else:
            return 'D'


class NotNiceTitForTat(Player):

    name = 'Not_nice_tit_for_tat'

    '''TitForTat but defects on first move'''

    classifer = {
        'niceness' : 0,
        'forgiveness' : .5,
        'memory_depth' : 1
    }

    def strategy(self, opponent_history):
        
        if not opponent_history:
            return 'D'
        
        else:
            return opponent_history[-1]