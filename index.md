# Abstract
This Work considers a reinforcement learning (RL) agent in the Iterated Prisoner’s Dilemma (IPD). We have implemented RL with three different kinds of methods : Dynamic Programming(DP), Temporal-Difference(TD) and Monte Carlo (MC) respectively. The purpose of the work is to test the performance of such various types of RL agents. We hope that RL agent may adjust its strategy to do the best response when it competes with a fixed strategy player, on the other hand, RL agent is also expected to elicit cooperation when it plays with itself or other RL agents, which is the best way to achieve more utility for himself.


# Problem Description
Two players play Prisoner's Dilemma more than once in succession and they can remember previous actions of their opponent and choose their strategy accordingly, but they do not exactly know when the iterated games would be over. Both players are trying to maximize their own utility. 

## Rules of Prisoner’s Dilemma
* If both players confess (Defect), they both will be sentence to 4 years respectively. Other words, both of them can earn utility for 1 respectively
* If one player confess (Defect) but the other remain silence (Cooperate), the player who confess will be free whereas the other will be punished for 5 years. Other words, the player who defect may earns 5 utility while the player who cooperate  gets nothing
* If both players remain silent (Cooperate), they both will be sentence to 2 years respectively. Other words, both of them can earn utility for 3 respectively
![Fig1](https://github.com/lijiyao919/IPD-RL/blob/master/picture/prison.png)

# Method
Reinforcement Learning is learning how to map situations to actions so as to maximize the reward signal from the environment. As Figure shown below, agent perceives Reward and State value and constructs its own internal state by reshaping the external state from environment. Then the internal state and the reward value are used to update the value of Q table by three different types of method: Dynamic Programming(DP), Temporal Difference(TD) and Monte Carlo(MC) respectively.  In the Action Selection, there is an exploration and exploitation problem. Boltzmann Distribution is used as a soft-max function to calculate the probability that determine whether agent should choose action of max𝑄 or a random action
![Fig2](https://raw.githubusercontent.com/lijiyao919/Figure/master/RL.png)

* **Dynamic Programming** (**DP**): This method is supposed to know the model of the environment. It Uses the future estimation (future Q value) to update current knowledge of the state (current Q value), which can be used to choose action in the future.
* **Temporal Difference** (**TD**): This method do not need to know the model of the environment. It used the present knowledge(present Q value) to update the past experience (previous Q value), which can be used to choose action in future.
* **Monte Carlo** (**MC**): This method do not need to know the model of the environment. It learns knowledge (the Q values )from the samples of each playout, and uses such knowledge to choose its action.


# Results
In all of the experiments below, TDBot, DPBot and MCBot represents RL Agents implemented by TD, DP and MC separately. The discount rate of all RL agents is set as 0.9. The temperature function of Boltzmann Distribution is t=20·〖0.999〗^𝑛 where n is the number of iterated games. The learning rate of the TDBot is decreasing as the iteration number goes up.

First of all, 3 tournaments that use Robin-Round style are held to test each RL Agent playing with 6 other Fixed Strategy Players. In the tournament, each of the two players play 10000 rounds in one match  and the Robin-Round repeats 30 times. Figures below show each player’s mean score and its distribution in every tournament separately. 
![fsp-td](https://github.com/lijiyao919/IPD-RL/blob/master/picture/TDBot.png)
![fsp-dp](https://github.com/lijiyao919/IPD-RL/blob/master/picture/DPBot.png)
![fsp-mc](https://github.com/lijiyao919/IPD-RL/blob/master/picture/MCBot.png)

Secondly, the homogeneous RL Agents matches are held. Here homogeneous means the agent plays with itself, so matches are TD vs. TD, DP vs. DP and MC vs. MC. Every two of the agent play 10000 times in each match. The bar chart below shows how many times can converge  to cooperation in 100 matches. The line graph shows the cooperation rate per iteration in a match that converge to cooperation. 
![homo](https://github.com/lijiyao919/IPD-RL/blob/master/picture/homo.png)


At last, heterogenous RL Agents matches are held. Heterogeneous here means agents implement their RL with different methods. So matches are TD vs. DP, TD vs. MC and DP vs. MC. The line graph below shows the cooperation rate per iteration in all matches. Also, tournament (10000 iterations for one match, the robin-round repeat 30 times)is also held between heterogenous RL agents. The payoff graph is shown as a heap graph.
![heter](https://github.com/lijiyao919/IPD-RL/blob/master/picture/heter.png)

# Conclusion
* All three types of RL agents learned to play optimally against the Fixed Strategy Agents. Playing against Fixed Strategy Agents is analogous to learning in a single agent environment, because Fixed Strategy Agents does not learn.
* Cooperation could be elicited when RL agent plays with itself. This is mainly because they share the same learning mechanism.
* Cooperation seldom emerged in experiments when different types of RL agents since agents use a different decision scheme.
* In the tournament among heterogeneous RL Agents, DPBot and MCBot are apparently weaker than TDBot. The reason might be the transitional model of DPBot cannot predict the true environment precisely in a non-stationary environment and  the samples of MCBot are relatively isolated in episode.

# Reference 
* R.Axelrod. The Evolution of Cooperation. Basic Books, New York, 1984
* Sutton, R.S and Barto, A.G Reinforcement learning: An introduction. MIT Press,   Cambridge, Massachusetts, 1998
* Stuart J. Russell, Peter Norvig. Artificial Intelligence: A Modern Approach (Third ed.). Prentice Hall. 2010
* Axelrod-Python Package: https://github.com/Axelrod-Python/Axelrod











