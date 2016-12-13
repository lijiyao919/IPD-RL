from __future__ import division
from axelrod import Actions, Player, random_choice
from collections import OrderedDict
import random
from math import *

C, D = Actions.C, Actions.D


class MCLearner(Player):

    name = 'MCBot'
    classifier = {
        'memory_depth': float('inf'),  # Long memory
        'stochastic': True,
        'makes_use_of': set(["game"]),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }
    memory_length = 1

    def __init__(self):

        super(MCLearner, self).__init__()

        self.history = []
        self.classifier['stochastic'] = True
        self.score = 0
        self.S = OrderedDict()
        self.Q = OrderedDict()
        self.Nsa = OrderedDict()
        self.Esa = OrderedDict()
        self.R = 0
        self.prev_state = None
        self.prev_action = None
        #self.alpha = lambda n: 1. / (1 + n)
        #self.action_selection_parameter = 0.05
        self.n = 1
        self.prob = []

        for state in ['CD', 'CC', 'DC', 'DD']:
            self.S[state] = {C: 0, D: 0}
            self.Q[state] = {C: 0, D: 0}
            self.Nsa[state] = {C: 0, D: 0}
            self.Esa[state] = {C: 0, D: 0}



    def receive_match_attributes(self):
        (R, P, S, T) = self.match_attributes["game"].RPST()
        self.payoff_matrix = {C: {C: R, D: S}, D: {C: T, D: P}}

    def find_reward(self, opponent):
        if self.prev_action == None or len(opponent.history) == 0:
            return 0
        else:
            opp_prev_action = opponent.history[-1]
            return self.payoff_matrix[self.prev_action][opp_prev_action]

    def find_state(self, opponent):
        if self.prev_action != None:
            return ''.join(opponent.history[-self.memory_length:])+self.prev_action
        else:
            return ''.join(opponent.history[-self.memory_length:])


    def strategy(self, opponent):
        """Runs a qlearn algorithm while the tournament is running."""
        state = self.find_state(opponent)
        reward = self.find_reward(opponent)
        #print("state= ", state)

        self.R = self.R + reward
        if self.prev_state != None and self.prev_state != '' and self.prev_state != 'C' and self.prev_state != 'D':
            self.Nsa[self.prev_state][self.prev_action] = self.Nsa[self.prev_state][self.prev_action] + 1
            self.Esa[self.prev_state][self.prev_action] = self.Esa[self.prev_state][self.prev_action] + 1

            if self.n % 10 == 0:
                for sta in ['CD', 'CC', 'DC', 'DD']:
                    for act in ['C','D']:
                        proportion = self.Esa[sta][act]/10
                        #print("proporttion=", proportion)
                        self.S[sta][act] = self.S[sta][act] + proportion*self.R
                        if self.Nsa[sta][act] != 0:
                            self.Q[sta][act] = self.S[sta][act]/self.Nsa[sta][act]
                        else:
                            self.Q[sta][act] = 0
                for state in ['CD', 'CC', 'DC', 'DD']:
                    self.Esa[state] = {C: 0, D: 0}
                self.R=0

        #print self.Q.items()
        action = self.select_action(state)
        #print action
        self.prev_state = state
        self.prev_action = action
        self.n+=1
        return action


    def boltzman(self, state, action):
        t=20*(0.999**(self.n))

        if t > 0.2:
            p =  exp(self.Q[state][action]/t) / (exp(self.Q[state][C]/t)+exp(self.Q[state][D]/t))
        else:
            p=1
        return p

    def select_action(self, state):
        if state == '' or state == 'C' or state == 'D':
            return random_choice()


        if self.Q[state][D] > self.Q[state][C]:
            action = D
        else:
            action = C

        rnd_num = random.random()
        p=self.boltzman(state, action)
        self.prob.append(p)
        #print ("p=",p)
        if rnd_num < p:
            return action
        else:
            #print "random choice"
            return random_choice()





    def reset(self):
        """
        Resets scores and history
        """
        Player.reset(self)
        self.S = OrderedDict()
        self.Q = OrderedDict()
        self.Nsa = OrderedDict()
        self.Esa = OrderedDict()
        self.R = 0
        self.prev_state = None
        self.prev_action = None
        self.n = 1
        self.prob = []

        for state in ['CD', 'CC', 'DC', 'DD']:
            self.S[state] = {C: 0, D: 0}
            self.Q[state] = {C: 0, D: 0}
            self.Nsa[state] = {C: 0, D: 0}
            self.Esa[state] = {C: 0, D: 0}



