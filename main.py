import os, random, time
ranks = ("Ace","2","3","4","5","6","7","8","9","10","Jack","Queen","King")
suits = ("Diamonds","Hearts","Spades","Clubs")
card_deck = {} # dictionary to hold card deck
num_decks = 6
num_players = 0
player_names = []
padding_spaces = 35
class_instances = []
max_hand_size = 0
test_mode = False
player_names_for_test = ["Dealer","Bob","James","Phil","Dale","Jack"]
max_players = 5
dealers_turn = False

# TODO - multiple card decks - how does this work in the real world, i.e., after each game is the whole deck re-shuffled?
# TODO - instead of choosing a random card from the deck, the program should actually "shuffle" the deck and then pull in order
# TODO - wagers
# TODO - keep player names between games
# TODO - split, double down, etc
# TODO - statistics
# TODO - graphics


class Class_player():
  global player_names, class_instances, max_hand_size
  print(player_names)
  def __init__(self, player_number):
    class_instances.append(self)
    if player_number == 0:
      self.name = "Dealer"
      self.str_padding = " " * padding_spaces * 2
    else:
      self.str_padding = " " * padding_spaces * (player_number - 1)
      # get player name
      cl = True
      while cl == True:
        # if other players are already present, show the list of existing player names to the user
        if len(player_names) > 1:
          print("Current player list:")
          skip = True
          for cn in player_names:
            if skip == True:
              skip = False # don't print dealer name
              continue
            print("  Player %s : %s"%(player_names.index(cn), cn))

        # get new player name
        if test_mode == True:
          self.name = player_names_for_test[player_number]
        else:
          self.name = input("Enter player " + str(player_number) + " name: ")
        if len(self.name) > padding_spaces:
          self.name = self.name[0:padding_spaces]
        clear_screen()

        # check to see if another player with the same name already exists (not regarding case sensitivity)
        if self.name == "":
          print("Player name cannot be blank")
          print_newline()
        elif self.name.upper() in (pn.upper() for pn in player_names):
          print("Name already in use. Try again")
          print_newline()
        else:
          cl = False
    player_names.append(self.name)
    self.cards = {} # dictionary to hold players cards
    self.list_card_value_sums = []
    self.has_ace = False
    self.busted = False
    self.player_number = player_number
    self.status = "In play"

  def generate_list_of_sum_of_card_values(self):
    self.list_card_value_sums = []

    # get base sums not counting aces as 11
    card_value_sum = 0
    for value in self.cards.values():
      card_value_sum = card_value_sum + value[0]

    self.list_card_value_sums.append(card_value_sum)

    if self.has_ace == True:
      self.list_card_value_sums.append(card_value_sum + 10)

  def hit(self):
    global max_hand_size
    self.cards.update(self.get_random_card())
    if self.player_number != 0 and len(self.cards) > max_hand_size:
      max_hand_size = len(self.cards)
    self.generate_list_of_sum_of_card_values()

  def get_random_card(self):
    new_card_dict = {}
    random_card_key = random.choice(list(card_deck.keys()))
    random_card_value = card_deck[random_card_key]
    if random_card_value[0] == 1:
      self.has_ace = True
    new_card_dict[random_card_key] = random_card_value
    card_deck[random_card_key][1] = card_deck[random_card_key][1] - 1
    if card_deck[random_card_key][1] == 0: # no more of this card left in the deck (multiple decks)
      card_deck.pop(random_card_key)
    return new_card_dict

  def player_action(self):
    in_play = True
    while in_play == True:
      if 21 in self.list_card_value_sums:
        self.list_card_value_sums = [21]
        self.status = "Blackjack"
        in_play = False
      elif self.list_card_value_sums[0] > 21:
        self.busted = True
        self.status = "Player busted"
        in_play = False
      else:
        print("\n" + self.str_padding + self.name)
        print(self.str_padding + "Choose an action:")
        print(self.str_padding + "1) Hit[Enter]")
        print(self.str_padding + "2) Stand")
        print(self.str_padding + "3) Surrender")
        choice = input(self.str_padding + "Choice: ")
        if choice == "1" or choice == "": # player chose to hit
          self.hit()
        elif choice == "2": # player chose to stand
          self.status = "Player stands"
          if max(self.list_card_value_sums) <= 21:
            self.list_card_value_sums =  [max(self.list_card_value_sums)]
          else:
            self.list_card_value_sums = [min(self.list_card_value_sums)]
          in_play = False
        elif choice == "3":
          self.status = "Player surrendered"
          in_play = False
        else:
          print(self.str_padding + "Invalid selection - Try again")
      show_table()

  def set_player_game_result(self,dealer_sum):
    if self.busted == True or self.status == "Player surrendered":
      None
    else:
      if dealer_sum > 21:
        self.status = "Player wins (dealer busted)"
      elif self.list_card_value_sums[0] > dealer_sum:
        self.status = "You beat the dealer"
      elif self.list_card_value_sums[0] < dealer_sum:
        self.status = "You lost to the dealer"
      elif self.list_card_value_sums[0] == dealer_sum:
        self.status = "You tied the dealer"

def print_newline():
  print("\n")

def main():
  global dealers_turn
  exit_game = False
  while exit_game == False:
    clear_screen()

    initialize_game()

    # create new class for dealer
    Player_dealer = Class_player(0)

    # create new class for each player
    for i in range(1, num_players + 1):
      cmd_str = "Player_" + str(i) + " = Class_player(" + str(i) + ")"
      exec(cmd_str)

    # generate random card 1 for each player
    for i in range(1, num_players + 1):
      cmd_str = "Player_" + str(i) + ".hit()"
      exec(cmd_str)


    # generate random card 1 for dealer
    Player_dealer.hit()

    # generate random card 2 for each player
    for i in range(1, num_players + 1):
      cmd_str = "Player_" + str(i) + ".hit()"
      exec(cmd_str)

    # generate random card 2 for dealer
    Player_dealer.hit()
    #print(Player_dealer.str_padding + "Dealer :")
    #print(Player_dealer.str_padding + '"Hole" card')

    show_table()
    
    # allow each player to hit or stand
    for i in range(1, num_players + 1):
      cmd_str = "Player_" + str(i) + ".player_action()"
      exec(cmd_str)

    
    # dealers turn
    dealers_turn = True
    Player_dealer.generate_list_of_sum_of_card_values()
    while max(Player_dealer.list_card_value_sums)  < 17:
      Player_dealer.hit()
    dealer_max_sum = max(Player_dealer.list_card_value_sums)
    dealer_min_sum = min(Player_dealer.list_card_value_sums)
    if dealer_min_sum > 21:
      Player_dealer.status = "Dealer busted"
    else:
      Player_dealer.status = "Dealer stands"
      if dealer_max_sum > 21: # determine best final sum for dealer
        Player_dealer.list_card_value_sums = [dealer_min_sum]
      else: # determine best final sum for dealer
        Player_dealer.list_card_value_sums = [dealer_max_sum]

    # get each player's results
    for i in range(1, num_players + 1):
      cmd_str = "Player_" + str(i) + ".set_player_game_result(Player_dealer.list_card_value_sums[0])"
      exec(cmd_str)

    show_table()

    print_newline()
    print("Play again?")
    print("1)Yes(Enter)")
    print("2)No")
    user_input = input("Choice: ")
    if user_input == "2":
      clear_screen()
      print("Thanks for playing Blackjack")
      exit_game = True
    else:
      reset_game()

def reset_game():
  global num_players, player_names, class_instances, max_hand_size, dealers_turn

  for instance in class_instances:
    del instance

  num_players = 0
  player_names = []
  class_instances = []
  max_hand_size = 0
  dealers_turn = False

def initialize_game():
  global num_players
  generate_full_deck()
  #print(card_deck)

  # get number of players
  cl = True
  while cl == True:
    num_players = input("Number of players (max is " + str(max_players) + " - default is 1): ")
    #num_players = 1
    clear_screen()
    try:
      if num_players == "":
        num_players = 1
      num_players = int(num_players)
    except:
      print("Invalid input (not able to convert input to positive whole number)")
    else:
      if num_players > max_players:
        print("Maximum of " + str(max_players) + " players allowed. Try again:")
      elif num_players <= 0:
        print("Only a number greater than 0 is allowed. Try again:")
      elif num_players > 0:
        cl = False

def clear_screen():
  os.system('cls') # clear the command window

def generate_full_deck():
  global card_deck
  card_deck = {}
  
  for suit in suits: # suits = ("Diamonds","Hearts","Spade","Clubs")
    for rank in ranks: # ranks = ("Ace","2","3","4","5","6","7","8","9","10","Jack","Queen","King")
      current_card = rank + " of " + suit
      current_value = ranks.index(rank) + 1
      if current_value > 10:
        current_value = 10
      card_deck[current_card] = [current_value,num_decks]

def show_table(): # show the card table / all players
  clear_screen()
  print_deck()
  # TODO - remove these if functionality still exists - global max_hand_size # is global necessary since these are not being edited
  
  # header
  str_padding = get_padding_spaces(2,"")
  print(str_padding + "Blackjack")

  # dealer name
  print("\n" + class_instances[0].str_padding + class_instances[0].name)
  
  # dealer cards
  hole_card_passed = False
  for key in class_instances[0].cards.keys():
    if dealers_turn == False and hole_card_passed == False: # don't show dealer "hole" card if it is not their turn yet
      hole_card_passed = True
      print(class_instances[0].str_padding + '"Hole" card (hidden)')
      continue
    print(class_instances[0].str_padding + key)
    
  # dealer sum(s)
  if dealers_turn == True:
    new_entry = True
    str_sums = ""
    for card_sum in class_instances[0].list_card_value_sums:
      if new_entry == True:
        new_entry = False
        str_sums = class_instances[0].str_padding + "Sum : " + str_sums + str(card_sum)
      else:
        str_sums = str_sums + " or "  + str(card_sum)
    print(str_sums)
  
  # dealer status
  print(class_instances[0].str_padding + class_instances[0].status)
  print_newline()

  # list to hold strings of player cards
  list_str_cards = []
  for i in range(max_hand_size):
    list_str_cards.append("")

  dealer_class_skipped = False
  class_instance_count = 0
  str_names = ""
  str_status = ""
  str_sums = ""
  for instance in class_instances: # iterate through each player class
    # player names
    if dealer_class_skipped == False: # skip dealer class
      dealer_class_skipped = True
      continue
    str_padding = get_padding_spaces(class_instance_count, str_names)
    str_names = str_names + str_padding + instance.name

    # player status
    str_padding = get_padding_spaces(class_instance_count, str_status)
    str_status = str_status + str_padding + instance.status

    # player cards
    curr_cards = instance.cards # current player class cards
    player_card_count = 0
    str_prev = ""
    for card in instance.cards.keys():
      str_padding = get_padding_spaces(class_instance_count, list_str_cards[player_card_count])
      list_str_cards[player_card_count] = list_str_cards[player_card_count] + str_padding + card
      player_card_count = player_card_count + 1

    # player sums
    new_entry = True
    str_player_sum = ""
    for card_sum in instance.list_card_value_sums:
      if new_entry == True:
        new_entry = False
        str_padding = get_padding_spaces(class_instance_count, str_sums)
        str_player_sum = str_padding + "Sum : " + str_player_sum + str(card_sum)
      else:
        str_player_sum = str_player_sum + " or "  + str(card_sum)

    str_sums = str_sums + str_player_sum
    class_instance_count = class_instance_count + 1 # next class instance

  print(str_names)
  for i in range(len(list_str_cards)):
    print(list_str_cards[i])
  print(str_sums)
  print(str_status)

def print_deck():
  for card_key in card_deck.keys():
    if card_deck[card_key][1] < 6:
      print(f"{card_key}  - {card_deck[card_key][1]}")

    
def get_padding_spaces(i, var):
  var = " " * ((i * padding_spaces) - len(var))
  return var


if __name__ == "__main__":
  main()