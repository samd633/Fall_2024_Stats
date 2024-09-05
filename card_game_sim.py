import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

class Card:
    def __init__(self):
        self.card = self.gen_card()
        self.suit = self.gen_suit()
        self.value = self.calc_value()

    def gen_card(self):
        cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"]
        len_cards = len(cards)
        rand_int = np.random.randint(low = 0, high = len_cards)
        card = cards[rand_int]

        return card

    def gen_suit(self):
        suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
        len_suit = len(suits)
        rand_int = np.random.randint(low = 0, high = len_suit)
        suit = suits[rand_int]

        return suit
    
    def calc_value(self):
        if(type(self.card) == int):
            value = 0.75
        elif(self.card == "A" and self.suit == "Clubs"):
            value = 25
        elif(self.card == "A" and self.suit != "Clubs"):
            value = 5
        else:
            value = 3
        
        return value

    def get_card_and_value(self):
        card_suit = f"{self.card}_{self.suit}"

        return card_suit, self.value

class PlayGame:
    def __init__(self, n_hands, buy_in):
        self.n_hands = n_hands
        self.buy_in = buy_in
    
    def draw(self):
        card, value = Card().get_card_and_value()

        return card, value
    
    def get_all_draws(self):
        cards = []
        values = []
        winnings = []

        for i in range(0, self.n_hands):
            card, value = self.draw()
            winning = (value - self.buy_in)
            
            cards.append(card)
            values.append(value)
            winnings.append(winning)

        return cards, values, winnings

class CardGameSim:
    def __init__(self, n_sims, n_hands, buy_in):
        self.n_sims = n_sims
        self.n_hands = n_hands
        self.buy_in = buy_in
        self.result = self.run_sim()

    def run_sim(self):
        result = np.full(shape = (self.n_sims, self.n_hands), fill_value = 0.0)
        
        for sim in range(0, self.n_sims):
            cards, values, winnings = PlayGame(n_hands = self.n_hands, buy_in = self.buy_in).get_all_draws()
            cml_winnings = np.cumsum(winnings)

            result[sim, ] = cml_winnings

        return(result)
    
    def get_result_hist(self):
        vals = self.result[:, self.n_hands - 1]
        avg_val = np.mean(vals)
        positive_return = vals > 0
        perct_positive_return = np.sum(positive_return)/len(vals)

        msg1 = f"Average return: {avg_val}"
        msg2 = f"Percent of trials with positive return: {perct_positive_return}"

        print(msg1)
        print(msg2)

        plt.hist(vals, density = True, bins = 30)
        plt.xlabel('Cml Winnings')
        plt.ylabel('Probability of Outcome')
        plt.show()


CardGameSim(n_sims = 1_000_000, n_hands = 20, buy_in = 2).get_result_hist()