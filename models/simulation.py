import random
import pandas as pd

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = self._get_value()

    def _get_value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11  # Treated as 11 by default (soft)
        else:
            return int(self.rank)

    def __str__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    def __init__(self, num_decks=1):
        self.cards = []
        self._build_deck(num_decks)
        random.shuffle(self.cards)

    def _build_deck(self, num_decks):
        suits = ['♠', '♥', '♦', '♣']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(suit, rank) for _ in range(num_decks) for suit in suits for rank in ranks]

    def deal(self):
        if len(self.cards) < 10:  # Reshuffle if fewer than 10 cards remain
            self._build_deck(1)
            random.shuffle(self.cards)
            print("\n--- Reshuffling deck ---\n")
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == 'A':
            self.aces += 1
        self._adjust_for_ace()

    def _adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10  # Treat Ace as 1 instead of 11
            self.aces -= 1

    def __str__(self):
        return ', '.join(map(str, self.cards))
    
    def __len__(self):
        return len(self.cards)
    
    def __getitem__(self, index):
        return self.cards[index]
    
#strategy: pd.DataFrame
class BlackjackSimulation:
    def __init__(self, num_rounds=10):  # Reduced default for readability
        self.num_rounds = num_rounds
        self.deck = Deck(num_decks=6)
        self.results = {'Player': 0, 'Dealer': 0, 'Push': 0} # map used to track outcome of hands

    def _get_action(self, strategy, phand_value, dealer_upcard):
        idx1 = str(phand_value)
        if 'A' in  idx1:
            idx1 = 'A'
        idx2 = self._get_dealer_index(dealer_upcard.value)
        action = strategy.loc[idx1, idx2]
        return action   
    
    def _get_dealer_index(self, dealer_upcard_value):
        match dealer_upcard_value:
            case 2:
                return 'col1'
            case 3:
                return 'col2'
            case 4:
                return 'col3'
            case 5:
                return 'col4'
            case 6:
                return 'col5'
            case 7:
                return 'col6'
            case 8:
                return 'col7'
            case 9:
                return 'col8'
            case 10:
                return 'col9'
            case 11:
                return 'col10'
            case _:
                return 'invalid card'
             
    def _player_turn(self, player_hand, strategy: pd.DataFrame, dealer_upcard):
        """Returns string that determines the action the player will do"""
        print(f"\nPlayer's hand: {player_hand} (Value: {player_hand.value})")
        print(f"Dealer's upcard: {dealer_upcard}")
        
        while True:
            # Hard totals
            if len(player_hand)==2 and player_hand.aces==1 and player_hand.value < 21:
                print("In aces and 2 cards")
                if str(player_hand[0]).find('A') != -1:
                    idx1 = 'A' + ',' + str(player_hand[1])
                    idx2 = idx2 = self._get_dealer_index(dealer_upcard.value)
                    print(f"idx1 = {idx1}, idx2 = {idx2}")
                    action = strategy.loc[idx1,idx2]
                    print(action)
                    return action  
                    # I put idx2 assignment in both branches for readibility but maybe it would be better to put it outside the if else
                else:
                    idx1 = 'A' + ',' + str(player_hand[0])
                    idx2 = self._get_dealer_index(dealer_upcard.value)
                    print(f"idx1 = {idx1}, idx2 = {idx2}")
                    action = strategy.loc[idx1,idx2]
                    print(action)
                    return action    
            elif len(player_hand)==2 and player_hand[0]==player_hand[1]:
                print("in 2 cards and cards are equal")
                idx1=str(player_hand[0]) + ',' + str(player_hand[1])
                idx2=self._get_dealer_index(dealer_upcard.value)
                print(f"idx1 = {idx1}, idx2 = {idx2}")
                action = strategy.loc[idx1,idx2]
                print(action)
                return action
            
            if player_hand.value > 17:
                    if player_hand.value==21 and len(player_hand)==2:
                        return 'BJ'
                    else:
                        return 'S'
            elif player_hand.value < 8: 
                    return 'H'
            else:
                return self._get_action(strategy, player_hand.value, dealer_upcard)
            '''
            if player_hand.value >= 17:
                print("Player strategy: Stand (≥17)")
                return 'stand'
            elif player_hand.value <= 11:
                print("Player strategy: Hit (≤11)")
                return 'hit'
            # Soft totals
            elif player_hand.aces > 0 and player_hand.value == 17 and dealer_upcard in [7, 8, 9, 10, 'J', 'Q', 'K', 'A']:
                print("Player strategy: Hit (Soft 17 vs dealer 7-A)")
                return 'hit'
            elif player_hand.aces > 0 and player_hand.value <= 17:
                print("Player strategy: Hit (Soft ≤17)")
                return 'hit'
            # Dealer-dependent decisions
            elif player_hand.value == 12 and dealer_upcard in [2, 3, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']:
                print("Player strategy: Hit (12 vs dealer 2-3 or 7-A)")
                return 'hit'
            elif 13 <= player_hand.value <= 16 and dealer_upcard in [7, 8, 9, 10, 'J', 'Q', 'K', 'A']:
                print(f"Player strategy: Hit ({player_hand.value} vs dealer 7-A)")
                return 'hit'
            else:
                print(f"Player strategy: Stand ({player_hand.value} vs dealer {dealer_upcard})")
                return 'stand'
            '''
    def _dealer_turn(self, dealer_hand):
        """Dealer hits on soft 17"""
        print(f"\nDealer's turn: {dealer_hand} (Value: {dealer_hand.value})")
        while dealer_hand.value < 17 or (dealer_hand.value == 17 and dealer_hand.aces > 0):
            new_card = self.deck.deal()
            dealer_hand.add_card(new_card)
            print(f"Dealer hits: {new_card} → {dealer_hand} (Value: {dealer_hand.value})")
        if dealer_hand.value > 21:
            print("Dealer busts!")
        else:
            print(f"Dealer stands at {dealer_hand.value}")

    def _determine_winner(self, player_hand, dealer_hand):
        print("\n--- Final Hands ---")
        print(f"Player: {player_hand} (Value: {player_hand.value})")
        print(f"Dealer: {dealer_hand} (Value: {dealer_hand.value})")

        if player_hand.value > 21:
            print("Result: Player busts! Dealer wins.")
            return 'Dealer'
        elif dealer_hand.value > 21:
            print("Result: Dealer busts! Player wins.")
            return 'Player'
        elif player_hand.value > dealer_hand.value:
            print("Result: Player wins!")
            return 'Player'
        elif dealer_hand.value > player_hand.value:
            print("Result: Dealer wins!")
            return 'Dealer'
        else:
            print("Result: Push (Tie)")
            return 'Push'

    def run_simulation(self, strategy: pd.DataFrame):
        print(f"=== Starting {self.num_rounds} rounds of Blackjack ===\n")
        # main loop
        for round_num in range(1, self.num_rounds + 1):
            print(f"\n=== Round {round_num}/{self.num_rounds} ===")
            player_hand = Hand()
            dealer_hand = Hand()

            # Deal initial cards
            player_hand.add_card(self.deck.deal()) 
            dealer_hand.add_card(self.deck.deal())
            player_hand.add_card(self.deck.deal())
            dealer_hand.add_card(self.deck.deal())

            print(f"\nInitial deal:")
            print(f"Player: {player_hand.cards[0]}, {player_hand.cards[1]} (Value: {player_hand.value})")
            print(f"Dealer: {dealer_hand.cards[0]}, ?")

            # Player's turn 
            while True:
                action = self._player_turn(player_hand, strategy, dealer_hand.cards[0])
                print(f"Action -> {action}")
                if action == 'BJ':
                    print("Player got blackjack")
                    break
                elif action == 'H':
                    new_card = self.deck.deal()
                    player_hand.add_card(new_card)
                    print(f"Player hits: {new_card} → {player_hand} (Value: {player_hand.value})")
                    if player_hand.value > 21:
                        print("Player busts!")
                        break
                elif action == 'D':
                    new_card = self.deck.deal()
                    player_hand.add_card(new_card)
                    print(f"Player doubles: {new_card} -> {player_hand} (Value: {player_hand.value})")
                    break
                elif action == 'Y':
                    print("TODO: implement splitting")
                    break
                else:
                    print("Player stands.")
                    break

            # Dealer's turn (if player didn't bust)
            if player_hand.value <= 21:
                self._dealer_turn(dealer_hand)

            # Determine winner
            result = self._determine_winner(player_hand, dealer_hand)
            self.results[result] += 1

            print("\n=== End of Round ===")

    def print_summary(self):
        total = sum(self.results.values())
        print("\n=== Simulation Summary ===")
        print(f"Total rounds: {total}")
        print(f"Player wins: {self.results['Player']} ({self.results['Player']/total:.1%})")
        print(f"Dealer wins: {self.results['Dealer']} ({self.results['Dealer']/total:.1%})")
        print(f"Pushes: {self.results['Push']} ({self.results['Push']/total:.1%})")

# Run simulation

'''
def main():
    sim = BlackjackSimulation()
    sim.run_simulation()

    
    hand = Hand()
    card1 = Card('♠', '4')
    card2 = Card('♠', '9')
    hand.add_card(card1)
    hand.add_card(card2)

    print(hand[0])
    


if __name__=="__main__":
    main()
'''    