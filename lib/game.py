import json, time
import numpy as np
from numpy.random import randint
from IPython.display import clear_output




def roll_dice(num_dice=2, sides=6):
    return sum([randint(1,sides+1) for _ in range(num_dice)])


class Horse:
    
    def __init__(self, numbers=[2,3], bonus=3, position=None):
        if position:
            self.position = position
        else:
            self.position = 0
        self.position_history = [(0, self.position)]
        self.movement_history = [(0, 0)]
        self.numbers = numbers # if these numbers are rolled move
        self.bonus = bonus # bonus if rolled twice in a row
        self.won = False
        self.placed = False
        self.showed = False
        
    def move(self, n, current_step=None):
        self.position = np.min([self.position + n, MAX_POSITION])
        if not current_step:
            current_step = self.position_history[-1][0] + 1 # Use the step number of the last recorded step in history + 1
        self.position_history.append((current_step, self.position))
        self.movement_history.append((current_step, n))


class Stable:
    
    def __init__(self, horses, positions=None): # takes a dict of 'name':horse pairs
        self.horses = horses
        self.positions = {name:horse.position for name,horse in self.horses.items()}
        self.step = 0
        
    def update(self, roll): 
        self.step += 1
        for name, horse in self.horses.items():
            if roll in horse.numbers:
                num2move = 1
                if horse.movement_history[-1][1] == 1: # If it also moved last time exactly 1 (no back to back bonus moves)
                    num2move += horse.bonus
                horse.move(num2move, self.step)
            else:
                horse.move(0, self.step)
        self.positions = {name:horse.position for name,horse in self.horses.items()} # Don't forget to keep positions helper variable updated!
        
    def check_over(self):
        for _, horse in self.horses.items():
            if horse.position >= MAX_POSITION:
                return True
        return False
    
    def display(self):
        print(f'\n\n{"":<6}' + '___'*(MAX_POSITION+2))
        print(f'{"":<6}' + '|  '*(RED_LINE_POSITION) + '|R ' + '|  '*(MAX_POSITION - RED_LINE_POSITION - 1) + '|FINISH')
        for name, horse in self.horses.items():
            s = f'{name:<6}' + '---'*(horse.position) + name[:2]
            finish_length = 6+3*MAX_POSITION
            print(f"{s[:finish_length] + ' '*(finish_length-len(s))}|{s[finish_length:]}")
        print(f'{"":<6}' + '|  '*(RED_LINE_POSITION) + '|R ' + '|  '*(MAX_POSITION - RED_LINE_POSITION - 1) + '|FINISH')
        print(f'{"":<6}' + '___'*(MAX_POSITION+2))


class ReadySetBetGame:
    
    def __init__(self, stable=None):
        if stable:
            self.stable = stable
            self.step = self.stable.step
        else:
            self.stable = Stable({
                '2/3': Horse(numbers=[2,3], bonus=3),
                '4': Horse(numbers=[4], bonus=3),
                '5': Horse(numbers=[5], bonus=2),
                '6': Horse(numbers=[6], bonus=1),
                '7': Horse(numbers=[7], bonus=0),
                '8': Horse(numbers=[8], bonus=1),
                '9': Horse(numbers=[9], bonus=2),
                '10': Horse(numbers=[10], bonus=3),
                '11/12': Horse(numbers=[11,12], bonus=3),
            })
            self.step = 0
        self.over = False
        self.placement = {}
        self.won = None
        self.placed = None
        self.showed = None
        self.roll_history = []
        self.finish_step = 15
        global MAX_POSITION, RED_LINE_POSITION
        MAX_POSITION = self.finish_step                            
        RED_LINE_POSITION = 10
        
    def play_step(self, visualize=False):
        
        self.step += 1
        
        roll = roll_dice()
        if visualize:
            print('\n')
            print(f'Step:{self.step} Roll: {roll}')
        
        self.stable.update(roll)
        
        if self.stable.check_over():
            self.over = True
        
        if visualize:
            self.stable.display()
    
    
    def determine_placement(self):
        positions = self.stable.positions
        
        current_rank = 1
        self.placement = {}
        self.finish_order = {}
        self.won = []
        self.placed = []
        self.showed = []
        for i in range(MAX_POSITION,-1,-1):
            horses_at_this_position = [name for name, position in positions.items() if position==i]
            
            if horses_at_this_position:
                self.finish_order[current_rank] = horses_at_this_position
                if current_rank == 1: # Win
                    self.won.extend(horses_at_this_position)
                    self.placed.extend(horses_at_this_position)
                    self.showed.extend(horses_at_this_position)
                    for name in horses_at_this_position:
                        self.stable.horses[name].won = True
                elif current_rank == 2: # Place)
                    self.placed.extend(horses_at_this_position)
                    self.showed.extend(horses_at_this_position)
                    for name in horses_at_this_position:
                        self.stable.horses[name].placed = True
                elif current_rank == 3: # Show)
                    self.showed.extend(horses_at_this_position)
                    for name in horses_at_this_position:
                        self.stable.horses[name].showed = True
                current_rank += len(horses_at_this_position)
        
        for place, horse_names in self.finish_order.items():
            for name in horse_names:
                self.placement[name] = place
        
            
            
    def get_log(self):
        log = {
            'total_rolls':self.step,
            'positions':self.stable.positions,
            'finish_order':self.finish_order,
            'placement':self.placement,
            'won':self.won,
            'placed':self.placed,
            'showed':self.showed,
        }
        return log

    
    def get_stable(self):
        return self.stable
    
    def play_game(self, visualize=False, time_step=1, max_steps=1000):
        
        if visualize:
            self.stable.display()
        
        while (not self.over) and self.step < max_steps:
            
            if visualize:
                time.sleep(time_step)
                clear_output(wait=True)
            self.play_step(visualize=visualize)
        
        self.determine_placement()
        
        return self.get_log()
        print('Game Over')




# Betting classes

def get_finish_function(horse_name, finish='won'):
    # finish can be 'won', 'placed', 'showed'.
    # Check log to see if horse did that.
    return lambda log: horse_name in log[finish] 


class Bet:
    def __init__(self, condition, multiplier, loss=0):
        self.condition = condition
        self.multiplier = multiplier
        self.loss = loss
        
    def resolve_bet(self, log, amount):
        if self.condition(log):
            return amount * self.multiplier
        else:
            return self.loss
        
    def __str__(self):
        return f"{self.multiplier}x, {self.loss}"


class BettingBoard:
    def __init__(self, bets=None):
        if bets == None:
            # All the standard bets
            print("Import standard bets")
            self.import_standard_bets()
        else:
            self.bets = bets
            
    def import_bets(self, json):
        self.bets = {}
        for item in json:
            print(item)
            name = item["horse"]
            for finish in ["won","placed","showed"]:
                condition = get_finish_function(name, finish=finish)
                for i, (multiplier, loss) in enumerate(item[finish]):
                    self.bets[f'{name}.{finish}.{i}'] = Bet(condition, multiplier, loss)
        
    def import_standard_bets(self):
        with open('../bets/standard_bets.json','r') as fi:
            self.import_bets(json.load(fi))


def get_expected_payouts(bet_amount, board, logs):
    expected_payouts = {}
    for bet_name, bet in board.bets.items():
        bet_payouts = []
        for i, log in enumerate(logs):
            payout = bet.resolve_bet(log, amount=bet_amount)
            bet_payouts.append(payout)

        avg_payout = np.mean(bet_payouts)
        expected_payouts[bet_name] = avg_payout
    return expected_payouts
