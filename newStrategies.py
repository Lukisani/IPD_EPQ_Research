import random

class Player:
    '''General template for each strategy'''
    name = 'Player'

    classifier = {
        'niceness' : 0,
        'forgiveness' : 0,
        'memory_depth' : 0}

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
        'memory_depth' : 1}

    def strategy(self, opponent_history):
        if not opponent_history:
            return 'C'
        return opponent_history[-1]

def TitForTatThatsHadEnough(Player):
    name = 'TitForTatThatsHadEnough'
    '''Play tit for tat until after 50 rounds, if the number of defections of the '''