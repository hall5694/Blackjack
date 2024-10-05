# blackjack
blackjack game - portfolio project for Nucamp - Python fundamentals


  100524
card_deck_ordered is a dictionary that is generated holding the ordered card deck, i.e., {"Ace of Diamonds":[1,6], "2 of Diamonds":[2,6], ...},    {card_description string:[card_value int, num_of_cards = num_of_decks], ...}
card_deck_shuffled is now added to reflect the real life scenario where the dealer shuffles the deck (in this case card_deck_ordered) and puts the shuffled deck in the shoe, and then pulling from the front of the deck
card_deck_shuffled data type is a list of dictionaries, e.g. [{"Ace of Diamonds":1],{"10 of Spades":10]]     [{card_1_description string:card_1_value int]}, {card_2_description string:card_2_value int]},....]
the function shuffle_deck was added to simulate shuffling the deck. shuffle_deck removes a random card card_deck_ordered and puts it in card_deck_shuffled
the function get_card performs was added to simulate the dealer drawing a card from the front of the shoe and giving it to a player or themselves

