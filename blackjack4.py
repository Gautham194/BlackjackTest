import matplotlib.pyplot as plt
import numpy as np
import random as rd
import time

standoncount = [0] * 22
hitoncount = [0] * 22
standonloss = [0] * 22
hitonloss = [0] * 22
wincount = 0
start_time = time.time()

# Set number of games played
game_count = 5000
current_game = 0

while current_game < game_count:
    current_game += 1

    card_list = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
    card_count = [24] * 13  # Simulates standard 6 packs


    # Rules
    # Dealer stands on 17. If A can be 11, it IS 11. No splitting currently. 21 is 21, no special Blackjacks.
    # If Draw, counts as House win.

    # Function that 'deals' a card from a six deck pile. Incorporates probability drop.
    def deal(Player, List=card_list, Counts=card_count):
        cycler = True
        while cycler:
            pull = rd.randrange(0, 13)
            if Counts[pull] > 0:
                Player.append(List[pull])
                Counts[pull] -= 1
                cycler = False
            else:
                continue


    # Takes cards and assigns values. Sums values - assumes A is 11 when possible.
    def hand_total(Player):
        total = 0
        for i in Player:
            if str(i) in 'KQJ':
                total += 10
            if str(i) is 'A' and total > 10:
                total += 1
            if str(i) is 'A' and total <= 10:
                total += 11
            elif str(i) not in 'KQJA':
                total += int(i)
        return total

    # Set Parameters for individual game - i.e. hands played before shuffle
    round_count = 20
    #player1_init = []
    #player1_final = []
    standon = [0] * 22
    hiton = [0] * 22
    current_round = 0
    player_wins = 0

    while current_round < round_count:
        current_round += 1
        dealer = []             # Stores cards held by dealer and player
        player1 = []
        # dealer_prog = []
        p1_prog = []            # Stores score increment for Player 1

        deal(dealer)            # Initial Deal
        deal(player1)
        deal(dealer)
        deal(player1)

        #dealer_dealt = hand_total(dealer)      #Inital Deal - Potential use for future analysis
        #player_dealt = hand_total(player1)

        dealer_value = hand_total(dealer)
        p1_value = hand_total(player1)

        # dealer_prog.append(dealer_value)
        p1_prog.append(p1_value)

        while hand_total(player1) < 21:
            deal(player1)
            p1_prog.append(hand_total(player1))
            if hand_total(player1) <= 21:
                p1_value = hand_total(player1)

        while hand_total(dealer) < 17:
            deal(dealer)
            # dealer_prog.append(hand_total(dealer))
            if hand_total(dealer) <= 21:
                dealer_value = hand_total(dealer)

        if p1_value > dealer_value:
            player_wins += 1
            #player1_final.append(p1_value)
            standon[p1_value] += 1
            if len(p1_prog) > 1 and p1_value != min(p1_prog):
                hitonvalue = p1_prog[p1_prog.index(p1_value) - 1]
                if hitonvalue < 21:
                    hiton[hitonvalue] += 1

        if p1_value <= dealer_value:
            standonloss[p1_value] += 1
            if p1_value != min(p1_prog):
                hitonlossvalue = p1_prog[p1_prog.index(p1_value) - 1]
                if hitonlossvalue < 21:
                    hitonloss[hitonlossvalue] += 1

    wincount += player_wins
    standoncount = [x + y for x, y in zip(standoncount, standon)]
    hitoncount = [x + y for x, y in zip(hitoncount, hiton)]

print(wincount, standoncount, hitoncount)
print("--- %s seconds ---" % (time.time() - start_time))

xvals = [i for i in range(22)]
neg_hiton = [-i for i in hitoncount]
plt.bar(xvals, standoncount, label='Winning Hands')
plt.bar(xvals, neg_hiton, label='Hit to Win')
plt.legend(loc='best')
plt.show()
neg_hitonloss = [-i for i in hitonloss]
plt.bar(xvals, standonloss, label='Losing Hands')
plt.bar(xvals, neg_hitonloss, label='Hit into Loss')
plt.legend(loc='best')
plt.show()
plt.bar(xvals, hitoncount, label = 'Win on Hit')
plt.bar(xvals, neg_hitonloss, label = 'Loss on Hit')
plt.legend(loc='best')
plt.show()
