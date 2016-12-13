from axelrod import Actions, Player, random_choice
from collections import OrderedDict
import random
from math import *

C, D = Actions.C, Actions.D


class TDLearner(Player):

    name = 'TDBot'
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

        super(TDLearner, self).__init__()

        self.history = []
        self.classifier['stochastic'] = True
        self.score = 0
        self.Q = OrderedDict()
        self.Nsa = OrderedDict()
        self.prev_state = None
        self.prev_action = None
        #self.Ne = 15
        #self.Rplus = 10
        self.alpha = lambda n: 1. / (1 + n)
        self.gamma = 0.9
        self.n = 1
        self.prob = []


    def receive_match_attributes(self):
        (R, P, S, T) = self.match_attributes["game"].RPST()
        self.payoff_matrix = {C: {C: R, D: S}, D: {C: T, D: P}}

    def strategy(self, opponent):
        """Runs a qlearn algorithm while the tournament is running."""
        state = self.find_state(opponent)
        reward = self.find_reward(opponent)
        if (state not in self.Q) and state != '':
            self.Q[state] = {C: 0, D: 0}
            self.Nsa[state] = {C: 0, D: 0}
        self.perform_q_learning(self.prev_state, state, self.prev_action, reward)
        action = self.select_action(state)
        self.prev_state = state
        self.prev_action = action
        #print("final action: ", action)
        return action

    def boltzman(self, state, action):
        t=20*(0.999**(self.n))
        self.n +=1
        #print("n=",self.n)
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
        p=self.boltzman(state, action)
        self.prob.append(p)
        #print ("p=",p)
        if rnd_num < p:
            return action
        else:
            #print "random choice"
            return random_choice()


    def find_state(self, opponent):
        """
        Finds the my_state (the opponents last n moves +
        its previous proportion of playing C) as a hashable state
        """
        #prob = '{:.1f}'.format(opponent.cooperations)
        if self.prev_action != None:
            return ''.join(opponent.history[-self.memory_length:])+self.prev_action
        else:
            return ''.join(opponent.history[-self.memory_length:])


    def perform_q_learning(self, prev_state, state, pre_action, reward):
        """
        Performs the qlearning algorithm
        """
        Q, Nsa = self.Q, self.Nsa
        alpha, gamma = self.alpha, self.gamma
        if prev_state != None and prev_state != '':
            Nsa[prev_state][pre_action] = Nsa[prev_state][pre_action] + 1
            maxQ = max(Q[state][action] for action in [C,D])
            Q[prev_state][pre_action] = Q[prev_state][pre_action] + alpha(Nsa[prev_state][pre_action])*(reward + gamma*maxQ-Q[prev_state][pre_action])
            #print Q.items()
            #print Nsa.items()


    def find_reward(self, opponent):
        """
        Finds the reward gained on the last iteration
        """
        if self.prev_action == None or len(opponent.history) == 0:
            return 0
        else:
            opp_prev_action = opponent.history[-1]
            return self.payoff_matrix[self.prev_action][opp_prev_action]

    def reset(self):
        """
        Resets scores and history
        """
        Player.reset(self)
        self.Q = OrderedDict()
        self.Nsa = OrderedDict()
        self.prev_state = None
        self.prev_action = None
        self.n = 1
        self.prob = []



