from player import Player
import parameters
import evaluator
from deck import Deck


class Texas_holdem:
    def __init__(self):
        self.deck = Deck()
        self.board = []
        self.pot = 0
        self.players = []
        self.players_this_round = []
        self.round_nr = 0
        self.deal_nr = 0
        self.big_blind_id = 0
        self.reset()

    def reset(self, input_players=[]):
        self.deck.reset_deck()
        self.board = []
        self.pot = 0
        self.round_nr = 0
        self.deal_nr = 0
        self.big_blind_id = 0
        self.players_this_round = []
        self.players = []
        if len(input_players) <= 1:
            for i in range(parameters.NR_OF_PLAYERS):
                self.players.append(
                    Player(i, str(i), parameters.START_CHIPS, self.deck.draw_card(), self.deck.draw_card()))
        else:
            for p in input_players:
                p.chips = parameters.START_CHIPS
                p.hand = [self.deck.draw_card(), self.deck.draw_card()]
                self.players.append(p)
        self.players[0].blind = 1
        self.players[1].blind = 2

    def get_board_card_by_index(self, index):
        if len(self.board) > index:
            return self.board[index]
        return None

    def new_round(self):
        if len(self.players) > 1:
            self.players_this_round = []
            self.deal_nr = 0
            self.round_nr += 1
            self.deck.reset_deck()
            self.board = []
            self.pot = 0
            for i, p in enumerate(self.players):
                self.players_this_round.append(p)
                blind_value = 0
                p.bet = 0
                if p.blind == 2:
                    blind_value = min(parameters.BIG_BLIND, p.chips)
                elif p.blind == 1:
                    blind_value = min(parameters.SMALL_BLIND, p.chips)
                self.pot += blind_value
                p.bet += blind_value
                p.chips -= blind_value
                p.give_hand(self.deck.draw_card(), self.deck.draw_card())
            for p in self.players:
                if p.blind == 2:
                    p.blind = 1
                    next_p = self.get_next_player(p, self.players_this_round)
                    next_p.blind = 2
                    self.big_blind_id = next_p.id_value
                    if len(self.players_this_round) > 2:
                        self.get_previous_player(p).blind = 0

    def dealer_step(self):
        if self.deal_nr == 0:
            # Deal 3 cards
            self.board.append(self.deck.draw_card())
            self.board.append(self.deck.draw_card())
            self.board.append(self.deck.draw_card())
        if self.deal_nr == 1:
            # Deal 1 card
            self.board.append(self.deck.draw_card())
        if self.deal_nr == 2:
            # Deal 1 card
            self.board.append(self.deck.draw_card())
        self.deal_nr += 1

    def who_wins(self):
        if len(self.players_this_round) == 0:
            print("ERROR!")
            return None
        elif len(self.players_this_round) == 1:
            self.deal_pot([self.players_this_round[0]])
            return self.players_this_round[0]
        player_score_map = []
        for player in self.players_this_round:
            player_score_map.append([evaluator.evaluate(self.fetch_cards_for_player(player)), player])
        player_score_map.sort(key=lambda x: x[0], reverse=True)
        top_score = player_score_map[0][0]
        top_players = [player_score_map[0][1]]
        counter = 1
        while counter < len(self.players_this_round) and player_score_map[counter][0] == top_score:
            top_players.append(player_score_map[counter][1])
            counter += 1
        self.deal_pot(top_players)
        return top_players

    def find_players_from_id(self, id_values):
        players_from_id = []
        for p in self.players:
            for value in id_values:
                if p.id_value == value:
                    players_from_id.append(p)
        return players_from_id

    def find_players_from_id_in_list(self, id_value, list_of_players):
        for p in list_of_players:
            if p.id_value == id_value:
                return p
        return None

    def find_player_from_id(self, id_value):
        for p in self.players:
            if p.id_value == id_value:
                return p
        return None

    def clear_players(self):
        for p in self.players:
            if p.chips <= 0:
                self.players.remove(p)

    def deal_pot(self, top_players):
        # One of these players wins
        if len(top_players) == 1:
            top_players[0].chips += self.pot
            self.pot = 0
        elif len(top_players) != 0:
            split = int(self.pot / len(top_players))
            for p in top_players:
                p.chips += split
            self.pot = 0

    def fetch_cards_for_player(self, player):
        cards = []
        for card in self.board:
            cards.append(card)
        cards.append(player.hand[0])
        cards.append(player.hand[1])
        return cards

    def get_player_after_big_blind(self):
        for i, p in enumerate(self.players_this_round):
            if p.id_value > self.big_blind_id:
                return p
        return self.players_this_round[0]

    def get_next_player(self, current_player, player_array):
        index = current_player.id_value
        for i, p in enumerate(player_array):
            if p.id_value > index:
                return p
        return player_array[0]

    def get_previous_player(self, current_player):
        index = current_player.id_value
        prev_p = None
        while prev_p is None:
            index -= 1
            if index < 0:
                index = len(self.players_this_round) - 1
            prev_p = self.find_players_from_id_in_list(index, self.players_this_round)
        return prev_p

    def all_pleased(self, current_bet):
        if len(self.players_this_round) == 1:
            return True
        for p in self.players_this_round:
            if p.bet < current_bet:
                return False
        return True

    def find_max_bet(self):
        max_bet = 999999999  # Just a randomly selected high number
        for p in self.players_this_round:
            if p.chips != 0 and p.chips < max_bet:
                max_bet = p.chips
        return max(max_bet, 0)

    def betting(self, current_bet):
        current_player = None
        max_bet = self.find_max_bet()
        betting_counter = 0
        while not self.all_pleased(current_bet) or betting_counter < len(self.players_this_round):
            betting_counter += 1
            if current_player is None:
                current_player = self.get_player_after_big_blind()
            else:
                print("går her...", max_bet)
                current_player = self.get_next_player(current_player, self.players_this_round)
            new_bet = self.decide_action(current_bet, max_bet, current_player)
            if new_bet is not None:
                current_bet = new_bet
            max_bet = self.find_max_bet()

    def decide_action(self, current_bet, max_bet, p):
        allowed_actions = 2
        if p.bet == current_bet:
            allowed_actions = 3
        bet = p.make_decision(current_bet, max_bet, self.pot, self.board, allowed_actions)
        bet = min(bet, p.chips)
        if bet >= 0:
            p.bet += bet
        if bet <= -1 or p.bet < current_bet:
            print(p.name, "folding...", "current bet", current_bet)
            # Fold
            p.bet = -1
            self.players_this_round.remove(p)
            return None
        else:
            p.chips -= bet
            self.pot += bet
            print(p.name, "betting ", bet, "in total", p.bet, "current bet", current_bet, )
            return p.bet

    def play_one_step(self, logger=False):
        if len(self.players) == 1:
            print("We have a winner! Rounds played: " + str(self.round_nr))
            return
        if len(self.players_this_round) <= 1:
            self.new_round()
            return
        self.betting(parameters.BIG_BLIND)
        self.dealer_step()
        if self.deal_nr == 4 or len(self.players_this_round) == 1:
            if logger:
                print("Pot: ", self.pot, " - board: ", self.board)
            self.who_wins()
            self.clear_players()
            if len(self.players) == 1:
                print("We have a winner! Rounds played: " + str(self.round_nr))
                return
            self.new_round()