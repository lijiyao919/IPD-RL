from axelrod import Actions, Player, init_args


C, D = Actions.C, Actions.D


class Pavlov(Player):

    name = 'Pavlov'
    classifier = {
        'memory_depth': 1,  # Four-Vector = (1.,0.,1.,0.)
        'stochastic': False,
        'makes_use_of': set(),
        'long_run_time': False,
        'inspects_source': False,
        'manipulates_source': False,
        'manipulates_state': False
    }

    def receive_match_attributes(self):
        (R, P, S, T) = self.match_attributes["game"].RPST()
        self.payoff_matrix = {C: {C: R, D: S}, D: {C: T, D: P}}

    def find_reward(self, opponent):
        """
        Finds the reward gained on the last iteration
        """
        opp_prev_action = opponent.history[-1]
        self_prev_action = self.history[-1]
        return self.payoff_matrix[self_prev_action][opp_prev_action]

    def strategy(self, opponent):
        """This is the actual strategy"""
        # First move


        if not self.history:
            return C
        # React to the opponent's last move
        reward = self.find_reward(opponent)
        if reward < 3:
            if self.history[-1] == C:
                return D
            else:
                return C
        else:
            return self.history[-1]