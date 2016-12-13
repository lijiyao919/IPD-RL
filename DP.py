from __future__ import division
from axelrod import Actions, Player, random_choice
from collections import OrderedDict
import random
from math import *


C, D = Actions.C, Actions.D


class DPLearner(Player):
    name = 'DPBot'
    memory_length = 1

    def __init__(self):

        super(DPLearner, self).__init__()

        self.history = []
        self.classifier['stochastic'] = True
        self.score = 0
        self.Q = OrderedDict()
        self.Nsa = OrderedDict()
        self.Nsas = OrderedDict()
        self.prev_state = None
        self.prev_action = None
        #self.alpha = lambda n: 1. / (1 + n)
        self.gamma = 0.9
        self.n = 1
        self.prob = []

    def receive_match_attributes(self):
        (R, P, S, T) = self.match_attributes["game"].RPST()
        self.payoff_matrix = {C: {C: R, D: S}, D: {C: T, D: P}}

    def find_state(self, opponent):
        if self.prev_action != None:
            return ''.join(opponent.history[-self.memory_length:])+self.prev_action
        else:
            return ''.join(opponent.history[-self.memory_length:])

    def find_reward(self, opponent):
        if self.prev_action == None or len(opponent.history) == 0:
            return 0
        else:
            opp_prev_action = opponent.history[-1]
            return self.payoff_matrix[self.prev_action][opp_prev_action]

    def strategy(self, opponent):
        """Runs a qlearn algorithm while the tournament is running."""
        state = self.find_state(opponent)
        reward = self.find_reward(opponent)
        if (state not in self.Q) and state != '':
            self.Q[state] = {C: 0, D: 0}
            self.Nsa[state] = {C: 0, D: 0}
            self.Nsas[state]= { C:{'CD':0, 'CC':0, 'DD':0, 'DC':0}, D:{'CD':0, 'CC':0, 'DD':0, 'DC':0} }
        if self.prev_state != None and self.prev_state != '':
            self.perform_learning(self.prev_state, state, self.prev_action, reward)
        action = self.select_action(state)
        self.prev_state = state
        self.prev_action = action
        self.n += 1
        return action

    def perform_learning(self, prev_state, state, prev_action, reward):
        Q, Nsa, Nsas = self.Q, self.Nsa, self.Nsas
        gamma=self.gamma
        T=0.0

        Nsa[prev_state][prev_action] = Nsa[prev_state][prev_action] + 1
        Nsas[prev_state][prev_action][state] = Nsas[prev_state][prev_action][state] + 1

        #print Nsa.items()
        #print Nsas.items()

        for a in [C, D]:
            sum=0.0

            for s1 in ['CD', 'CC', 'DD', 'DC']:
                if s1 in Q:
                    if Q[s1][D] > Q[s1][C]:
                        maxQ = Q[s1][D]
                    else:
                        maxQ = Q[s1][C]
                else:
                    maxQ = 0.0


                if Nsa[state][a] != 0:
                    T = Nsas[state][a][s1] / Nsa[state][a]
                else:
                    T = 0.0

                sum=sum+T*maxQ
            Q[state][a] = reward + gamma*sum
        #print("n=", self.n)
        #print state
        #print Q.items()
        #print Nsa.items()
        #print Nsas.items()



    def boltzman(self, state, action):
        t=20*(0.999**(self.n))
        if t > 0.2:
            p =  exp(self.Q[state][action]/t) / (exp(self.Q[state][C]/t)+exp(self.Q[state][D]/t))
        else:
            p=1
        return p

    def select_action(self, state):
        if state == '':
            return random_choice()

        if self.Q[state][D] > self.Q[state][C]:
            action = D
        else:
            action = C

        rnd_num = random.random()
        p = self.boltzman(state, action)
        self.prob.append(p)
        # print ("p=",p)
        if rnd_num < p:
            return action
        else:
            # print "random choice"
            return random_choice()

    def reset(self):
        """
        Resets scores and history
        """
        Player.reset(self)
        self.Q = OrderedDict()
        self.Nsa = OrderedDict()
        self.Nsas = OrderedDict()
        self.prev_state = None
        self.prev_action = None
        self.n = 1
        self.prob = []