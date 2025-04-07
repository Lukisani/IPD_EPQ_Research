import random
import math

class Player:
    '''Base player class'''
    name = 'Player'
    classifier = {'niceness': 0, 'forgiveness': 0, 'memory_depth': 0}
    
    def __init__(self):
        self.history = []
        self.score = 0

    def strategy(self, opponent_history):
        raise NotImplementedError()

    def reset(self):
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

# 1. Tit For Tat (Anatol Rapoport) :cite[6]
class TitForTat(Player):
    name = "Tit For Tat"
    classifier = {'niceness': 1, 'forgiveness': 1, 'memory_depth': 1}
    
    def strategy(self, opponent_history):
        return 'C' if not opponent_history else opponent_history[-1]

# 2. Tideman and Chieruzzi (Gradual Retaliator)
class TidemanChieruzzi(Player):
    name = "Tideman & Chieruzzi"
    classifier = {'niceness': 0.5, 'forgiveness': 0.7, 'memory_depth': float('inf')}
    
    def __init__(self):
        super().__init__()
        self.retaliation_length = 0
        self.retaliating = False
        self.fresh_start_round = -20

    def strategy(self, opponent_history):
        current_round = len(opponent_history)
        if self._fresh_start_conditions(opponent_history, current_round):
            self._reset_fresh_start(current_round)
            return 'C'
        if self.retaliating:
            self.retaliation_length -= 1
            if self.retaliation_length <= 0:
                self.retaliating = False
            return 'D'
        if opponent_history and opponent_history[-1] == 'D':
            if len(opponent_history) == 1 or opponent_history[-2] != 'D':
                self.retaliation_length += 1
                self.retaliating = True
                return 'D'
        return 'C'

    def _fresh_start_conditions(self, opponent_history, current_round):
        return (self.score - sum(1 for h in opponent_history if h == 'D') >= 10 and
                (not opponent_history or opponent_history[-1] != 'D') and
                current_round - self.fresh_start_round >= 20)

    def _reset_fresh_start(self, current_round):
        self.fresh_start_round = current_round
        self.retaliation_length = 0
        self.retaliating = False

# 3. Nydegger (Weighted History) :cite[2]
class Nydegger(Player):
    name = "Nydegger"
    classifier = {'niceness': 0.7, 'forgiveness': 0.6, 'memory_depth': 3}
    
    def strategy(self, opponent_history):
        if len(opponent_history) < 3:
            return 'C'
        weights = [0.5, 0.3, 0.2]  # Recent moves weighted more
        score = sum(w * (1 if m == 'D' else 0) 
                   for w, m in zip(weights, opponent_history[-3:]))
        return 'D' if score > 0.5 else 'C'

# 4. Grofman (Complex Conditional) :cite[4]
class Grofman(Player):
    name = "Grofman"
    classifier = {'niceness': 1, 'forgiveness': 0.8, 'memory_depth': 7}
    
    def strategy(self, opponent_history):
        round_num = len(opponent_history)
        if round_num < 2:
            return 'C'
        if round_num < 7:  # First 7 rounds
            return opponent_history[-1]
        # After 7 rounds: cooperate if both did same last move
        return 'C' if opponent_history[-1] == self.history[-1] else 'D'

# 5. Shubik (Escalating Trigger) :cite[1]
class Shubik(Player):
    name = "Shubik"
    classifier = {'niceness': 1, 'forgiveness': 0, 'memory_depth': float('inf')}
    
    def __init__(self):
        super().__init__()
        self.triggered = False
        self.defection_count = 0

    def strategy(self, opponent_history):
        if self.triggered:
            return 'D'
        if opponent_history and opponent_history[-1] == 'D':
            self.defection_count += 1
            if self.defection_count >= 3:  # 3 defections trigger permanent D
                self.triggered = True
        return 'C'

# 6. Stein and Rapoport (Probabilistic Tit For Tat) :cite[4]
class SteinRapoport(Player):
    name = "Stein & Rapoport"
    classifier = {'niceness': 0.95, 'forgiveness': 0.8, 'memory_depth': 1}
    
    def strategy(self, opponent_history):
        if not opponent_history:
            return 'C' if random.random() > 0.05 else 'D'
        if opponent_history[-1] == 'D':
            return 'D' if random.random() > 0.1 else 'C'
        return 'C'

# 7. Grudger (Friedman) :cite[6]
class Grudger(Player):
    name = "Grudger"
    classifier = {'niceness': 1, 'forgiveness': 0, 'memory_depth': float('inf')}
    
    def strategy(self, opponent_history):
        return 'D' if 'D' in opponent_history else 'C'

# 8. Davis (Limited Retaliation) :cite[2]
class Davis(Player):
    name = "Davis"
    classifier = {'niceness': 1, 'forgiveness': 0.5, 'memory_depth': 10}
    
    def __init__(self):
        super().__init__()
        self.retaliation_count = 0

    def strategy(self, opponent_history):
        if self.retaliation_count > 0:
            self.retaliation_count -= 1
            return 'D'
        if opponent_history and opponent_history[-1] == 'D':
            self.retaliation_count = 10  # Retaliate for 10 rounds
            return 'D'
        return 'C'

# 9. Graaskamp (Adaptive Probability) :cite[4]
class Graaskamp(Player):
    name = "Graaskamp"
    classifier = {'niceness': 0.3, 'forgiveness': 0.7, 'memory_depth': 10}
    
    def strategy(self, opponent_history):
        if len(opponent_history) < 10:
            return 'C'
        coop_rate = sum(1 for m in opponent_history[-10:] if m == 'C')/10
        return 'C' if random.random() < coop_rate else 'D'

# 10. Downing (Bayesian Estimator) :cite[1]
class Downing(Player):
    name = "Downing"
    classifier = {'niceness': 0.5, 'forgiveness': 0.6, 'memory_depth': float('inf')}
    
    def __init__(self):
        super().__init__()
        self.opponent_coop_prob = 0.5

    def strategy(self, opponent_history):
        if not opponent_history:
            return 'C'
        # Update cooperation probability estimate
        history_len = len(opponent_history)
        self.opponent_coop_prob = sum(1 for m in opponent_history if m == 'C')/history_len
        return 'C' if self.opponent_coop_prob > 0.5 else 'D'

# 11. Feld (Adaptive Threshold) :cite[4]
class Feld(Player):
    name = "Feld"
    classifier = {'niceness': 0.6, 'forgiveness': 0.4, 'memory_depth': 5}
    
    def __init__(self):
        super().__init__()
        self.threshold = 0.5

    def strategy(self, opponent_history):
        if len(opponent_history) < 5:
            return 'C'
        recent_defections = sum(1 for m in opponent_history[-5:] if m == 'D')
        self.threshold = min(0.8, max(0.2, recent_defections/5))
        return 'C' if random.random() < self.threshold else 'D'

# 12. Joss (Stochastic Tit For Tat) :cite[6]
class Joss(Player):
    name = "Joss"
    classifier = {'niceness': 0.9, 'forgiveness': 0.8, 'memory_depth': 1}
    
    def strategy(self, opponent_history):
        if not opponent_history:
            return 'C'
        if random.random() < 0.1:  # 10% chance to defect
            return 'D'
        return opponent_history[-1]

# 13. Tullock (Cooperation Rate Mirror) :cite[1]
class Tullock(Player):
    name = "Tullock"
    classifier = {'niceness': 0.5, 'forgiveness': 0.5, 'memory_depth': float('inf')}
    
    def strategy(self, opponent_history):
        if not opponent_history:
            return 'C'
        coop_rate = sum(1 for m in opponent_history if m == 'C')/len(opponent_history)
        return 'C' if coop_rate >= 0.5 else 'D'

# 14. Anonymous (Adaptive Probability) :cite[4]
class Anonymous(Player):
    name = "Anonymous"
    classifier = {'niceness': 0.3, 'forgiveness': 0.7, 'memory_depth': 10}
    
    def __init__(self):
        super().__init__()
        self.p_coop = 0.3

    def strategy(self, opponent_history):
        if len(opponent_history) % 10 == 0 and len(opponent_history) > 0:
            # Update probability every 10 rounds
            recent_coop = sum(1 for m in opponent_history[-10:] if m == 'C')
            self.p_coop = max(0.3, min(0.7, recent_coop/10 + 0.1*random.random()))
        return 'C' if random.random() < self.p_coop else 'D'

# 15. Random :cite[6]
class RandomPlayer(Player):
    name = "Random"
    classifier = {'niceness': 0.5, 'forgiveness': 0.5, 'memory_depth': 0}
    
    def strategy(self, opponent_history):
        return random.choice(['C', 'D'])