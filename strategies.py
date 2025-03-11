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
    
    def clone(self):
        '''
        Creates a new instance of the same strategy with the same initial state.
        Subclasses inherit this method and do not need to override it.
        '''
        # Create a new instance of the same class
        new_instance = self.__class__()
        # Copy the name and classifier (if they are instance-specific)
        new_instance.name = self.name
        new_instance.classifier = self.classifier.copy()
        return new_instance



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


class Friedman(Player):

    name = 'Grim_Trigger'

    '''Cooperates until the opponent defects; once defected against, it defects forever.'''

    classifier = {
        'niceness': 1,
        'forgiveness': 0,
        'memory_depth': float('inf')
    }

    def strategy(self, opponent_history):

        return 'D' if 'D' in opponent_history else 'C'


class Pavlov(Player):

    name = 'Pavlov'

    '''Cooperates if the previous round resulted in a payoff of 3 (mutual cooperation) or 5 (exploiting the opponent), otherwise defects.'''

    classifier = {
        'niceness': 0.75,
        'forgiveness': 0.75,
        'memory_depth': 1
    }

    def strategy(self, opponent_history):

        if not opponent_history:
            return 'C'
        return 'C' if opponent_history[-1] == self.history[-1] else 'D'


class Prober(Player):

    name = 'Prober'

    '''Defects initially to test the opponent, then behaves like Tit for Tat or Always Defect based on the opponent's response.'''

    classifier = {
        'niceness': 0.5,
        'forgiveness': 0.5,
        'memory_depth': float('inf')
    }

    def strategy(self, opponent_history):
        if len(opponent_history) < 3:
            return 'D' if len(opponent_history) in [0, 2] else 'C'
        return 'D' if opponent_history[1:3] == ['D', 'D'] else TitForTat().strategy(opponent_history)


class Tester(Player):

    name = 'Tester'

    '''Starts with "DCC", then cooperates if the opponent defects in response to defection; otherwise, defects forever.'''
    
    def strategy(self, opponent_history):

        if len(opponent_history) < 3:
            return 'D' if len(opponent_history) == 0 else 'C'
        return 'C' if opponent_history[1] == 'D' else 'D'


class Joss(Player):

    name = 'Joss'

    '''A variant of Tit For Tat that randomly defects with a small probability (e.g., 10%).'''

    def strategy(self, opponent_history):

        if not opponent_history:
            return 'C'
        return 'D' if random.random() < 0.1 else opponent_history[-1]


class SoftMajority(Player):

    name = 'Soft_Majority'

    '''Cooperates if the opponent has cooperated more than they have defected; otherwise, defects.'''

    def strategy(self, opponent_history):
        if not opponent_history:
            return 'C'
        return 'C' if opponent_history.count('C') > opponent_history.count('D') else 'D'

class AdaptiveTitForTat(Player):
    name = 'Adaptive_Tit_For_Tat'

    '''Starts with cooperation but adjusts its behavior by being more forgiving if the opponent cooperates frequently.'''

    def strategy(self, opponent_history):
        if not opponent_history:
            return 'C'
        if opponent_history.count('C') > opponent_history.count('D'):
            return 'C'
        return opponent_history[-1]
    

class Punisher(Player):
    name = 'Punisher'

    '''Starts with cooperation but defects for a set number of rounds when the opponent defects.'''
    
    def __init__(self):
        self.punishment_rounds = 0

    def strategy(self, opponent_history):
        if self.punishment_rounds > 0:
            self.punishment_rounds -= 1
            return 'D'
        if opponent_history and opponent_history[-1] == 'D':
            self.punishment_rounds = 2  # Punish for 2 rounds
            return 'D'
        return 'C'


class Extortioner(Player):
    name = 'Extortioner'

    '''Attempts to exploit the opponent by cooperating only enough to keep them from always defecting.'''

    def strategy(self, opponent_history):
        if not opponent_history or len(opponent_history) % 3 == 0:
            return 'C'
        return 'D'


class Retaliator(Player): # needs work with init method (inheritance bug - use super.()__init__ and change reset function if necessary)
    name = 'Retaliator'

    '''Cooperates until the opponent defects, then retaliates for the same number of rounds'''

    def __init__(self):
        self.retaliation_rounds = 0

    def strategy(self, opponent_history):
        if self.retaliation_rounds > 0:
            self.retaliation_rounds -= 1
            return 'D'
        if opponent_history and opponent_history[-1] == 'D':
            self.retaliation_rounds = 1  # Retaliate for 1 round
            return 'D'
        return 'C'


class Spiteful(Player):
    name = 'Spiteful'

    '''Starts with cooperation but switches to Always Defect after the opponent defects a certain number of times.'''
    
    def __init__(self):
        self.spited = False

    def strategy(self, opponent_history):
        if self.spited:
            return 'D'
        if opponent_history.count('D') >= 3:
            self.spited = True
            return 'D'
        return 'C'
