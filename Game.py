from __future__ import division
import axelrod as axl
from TD import *
from DP import *
from MC import *
from Pavlov import *
import matplotlib.pyplot as plt
#import pylab as plt

def main():

    MC = MCLearner()
    TD = TDLearner()
    DP = DPLearner()

    print("1. Play With the Fixed Strategy Player")
    print("2. Play With Itself")
    print("3. Play With Another Types of Player")

    choice = input("which one do you want to choose:")

    if choice == 1:
        playWithFixed(TD, DP, MC)

    elif choice == 2:
        playWithHomo(TD, DP, MC)

    elif choice == 3:
        playWithHete(TD, DP, MC)

    else:
        print("Your Choice is not correct, please choose 1 or 2 or 3")



    #For play with fixed strategy player
    '''for learner in [TD,DP,MC]:
        players = [PAV, learner]
        match = axl.Match(players, turns=10000)
        match.play()
        result = match.scores()
        draw(result, "PAVLOV")

        players = [D, learner]
        match = axl.Match(players, turns=10000)
        match.play()
        result = match.scores()
        draw(result, "Defector")

        players = [C, learner]
        match = axl.Match(players, turns=10000)
        match.play()
        result = match.scores()
        draw(result, "Cooperator")'''



# Tournament With Fixed Guys
def playWithFixed(TD, DP, MC):
    C = axl.Cooperator()
    D = axl.Defector()
    TFT = axl.TitForTat()
    BUL = axl.Bully()
    PAV = Pavlov()
    APAV = axl.APavlov2011()

    for learner in [TD,DP,MC]:
        players = [C, D, TFT, BUL, PAV, APAV, learner]
        tournament = axl.Tournament(players, turns=10000)
        results = tournament.play()

        title = learner.name + " VS Fixed Strategy Players"
        plot = axl.Plot(results)
        p = plot.boxplot(title)
        p.savefig(learner.name)

# homogeneous learners cooperate caculation
def playWithHomo(TD, DP, MC):
    j = 0
    ccPercent = [[0], [0], [0]]
    for learner in [TD, DP, MC]:
        ccCnt = 0
        players = [learner, learner]
        match = axl.Match(players, turns=10000)
        result = match.play()
        # print result
        for i in range(1, 10000):
            if result[i] == ('C', 'C'):
                ccCnt += 1
            ccPercent[j].append(ccCnt / i)
        j = j + 1
        print learner.name
    print ccPercent[0]
    print len(ccPercent[0])
    print ccPercent[1]
    print len(ccPercent[1])
    print ccPercent[2]
    print len(ccPercent[2])
    drawCCPercent(ccPercent, True)

##heterogeneous learners cooperate caculation
def playWithHete(TD, DP, MC):
    ccPercent = [[0], [0], [0]]
    ccCnt = 0
    players = [TD, DP]
    match = axl.Match(players, turns=10000)
    result = match.play()
    # print result
    for i in range(1, 10000):
        if result[i] == ('C', 'C'):
            ccCnt += 1
        ccPercent[0].append(ccCnt / i)

    ccCnt = 0
    players = [TD, MC]
    match = axl.Match(players, turns=10000)
    result = match.play()
    # print result
    for i in range(1, 10000):
        if result[i] == ('C', 'C'):
            ccCnt += 1
        ccPercent[1].append(ccCnt / i)

    ccCnt = 0
    players = [DP, MC]
    match = axl.Match(players, turns=10000)
    result = match.play()
    # print result
    for i in range(1, 10000):
        if result[i] == ('C', 'C'):
            ccCnt += 1
        ccPercent[2].append(ccCnt / i)

    print ccPercent[0]
    print len(ccPercent[0])
    print ccPercent[1]
    print len(ccPercent[1])
    print ccPercent[2]
    print len(ccPercent[2])
    drawCCPercent(ccPercent, False)

    # heat graph
    players = [TD, DP, MC]
    tournament = axl.Tournament(players, turns=10000)
    results = tournament.play()
    plot = axl.Plot(results)
    p = plot.payoff()
    p.savefig("heat graph")


def drawCCPercent(cc, homo):
    if homo == True:
        plot1 = plt.plot(cc[0], 'r', label='TDBot vs. TDBot')
        plot2 = plt.plot(cc[1], 'b', label='DPBot vs. DPBot')
        plot3 = plt.plot(cc[2], 'k', label="MCBot vs. MCBot")
    else:
        plot1 = plt.plot(cc[0], 'r', label='TDBot vs. DPBot')
        plot2 = plt.plot(cc[1], 'b', label='TDBot vs. MCBot')
        plot3 = plt.plot(cc[2], 'k', label="DPBot vs. MCBot")

    plt.title("The Cooperation Rate When Learner Play with Each Other")
    plt.xlabel("Game Iterations")
    plt.ylabel("Cooperation Rate")
    plt.yticks([0.0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0])
    plt.grid(b=True, which='major', color='k', linestyle='dotted')
    plt.legend()

    if homo == True:
        plt.savefig("ccPercent_homo.png")
    else:
        plt.savefig("ccPercent_hete.png")





# For Debug Issues
'''def drawProb(td,dp,mc):
    time = []

    for i in range(1,10000):
        time.append(i)

    plot1 = plt.plot(time, td, 'r', label='TD')
    plot2 = plt.plot(time, dp, 'b', label='DP')
    plot3 = plt.plot(time, mc, 'k', label="MC")

    plt.title("The Probability from the Soft-max Fnction")
    plt.xlabel("Game Iterations")
    plt.ylabel("The Probability of Action from MaxQ")

    plt.legend()

    plt.savefig("Probability.png")


def draw(result, opponent):
    time = []
    player1 = []
    player2 = []
    ytitle=opponent+" Score"
    title="Compete With "+opponent

    for i in range(1,10001):
        time.append(i)
        player1.append(result[i-1][0])
        player2.append(result[i-1][1])

    plt.figure(1)
    plt.subplot(211)
    plt.plot(time, player1, 'r')
    plt.ylabel(ytitle)
    plt.title(title)


    plt.subplot(212)
    plt.plot(time, player2, 'b')
    plt.xlabel("Game Rounds")
    plt.ylabel("My Score")


    plt.show()'''



if __name__ == '__main__':
    main()


