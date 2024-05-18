from data import Player, Pile, Card

sample_hand = Pile()
sample_hand.add(Card('clubs',11))
sample_hand.add(Card('diamonds',11))
sample_hand.add(Card('hearts',11))
sample_hand.add(Card('hearts',11)) 
sample_hand.add(Card('hearts',11))

def game():

    print("Welcome to Euchre!")
    players = [
        Player(Pile(), 0, 0, "pigly"), 
        Player(Pile(), 1, 0, "oinker"), 
        Player(Pile(), 0, 0, "hamlet"), 
        Player(Pile(), 1, 0, "pigalina")
    ]

    score = [0, 0]
    
    while all(x < 10 for x in score):
        print("Starting a new game!")
        print("Scores are:", score)
        dealer = players[0]
        faceup = set_up(dealer, players)
        caller, trump = bidding(dealer, players, faceup)

        if(caller.team == dealer.team and caller != dealer):
            players.remove(dealer)

        team_tricks = tricktaking(caller, trump, players)
        score_diff = scoring(team_tricks, players, caller, dealer)
        for i in range(len(score)):
            score[i] += score_diff[i]

def set_up(dealer, players):

    deck = Pile.make_deck()

    for player in players:
        for i in range (0, 5):
            player.hand.add(deck.pick(-1))

    return deck.pick(-1)



# returns the caller player, the trump suit
def bidding(dealer, players, faceup):
    
    print("Face up card is " + str(faceup))
    print("Dealer is " + dealer.name)

    players = rotate_to(dealer, players)

    # first round of bidding on faceup
    for player in players[1:]:
        print(player.name + " do you want to call up " + dealer.name + " to pick up " + str(faceup) + "? ")

        if(player.team == dealer.team):
            print("Beware, you and the dealer are on the same team. If you call up the dealer, you are forced to go alone") 
        
        if(yes_no("y/n: ")):
            return (player, faceup.suit)

    print("No one has called the dealer up. You may now call any suit")

    for player in players:
       ans = get_input_call(player.name + " what suit do you call it? You may also pass")


def tricktaking(caller, trump, players):
    for _ in range(5):
        winner = play_trick(trump, players)
        rotate_to(winner, players)

    team_tricks = [0, 0]
    for player in players:
        team_tricks[player.team] += player.trick_count

    return team_tricks

def scoring(team_tricks, players, caller, dealer):
    score_diff = [0, 0]

    if team_tricks[caller.team] == 5:
        score_diff[caller.team] = 4 if len(players) == 3 else 2
    elif team_tricks[caller.team] >= 3:
        score_diff[caller.team] = 1
    else:
        score_diff[1 - caller.team] = 2

    return score_diff

def play_trick(trump, players):
    """Players[0] is the leader. Returns the player who won the trick."""
    middle = Pile()
    lead = None
    for player in players:
        card = choose_card(players.hand, lead)
        lead = card.suit if lead is None else lead
        middle.add(card)

    winning_card = middle.maximum(trump, middle.cards[0].suit)
    winner_index = middle.find_index(winning_card)
    players[winner_index].trick_count += 1

    return players[winner_index]
            
def rotate_to(element, lst):
    if element not in lst:
        raise ValueError(f"error `{element}' not found in lst '{lst}'")
    index = lst.index(element)
    return lst[index:] + lst[:index]

def choose_card(hand, lead_suit, trump):
    print("Here is your hand " + (str(card) for card in hand))
    ans = input("Please return the card you want to select, starting at index 0")

def valid_play(hand, index, lead_suit, trump):
    if hand.cards[index].follows_suit(lead_suit, trump):
        return True

    if not any(card.follows_suit(lead_suit, trump) for card in hand.cards):
        return True

    return False
    
    
def yes_no(msg : str):
    while True:
        res = input(msg).lower().strip()
        if res != 'y' and res != 'n':
            print("invalid input, please respond with y/n")
        else:
            return res == 'y'
        
if '__main__' == __name__:
    game() 
