import pygame
from pygame.locals import *
import game
import parameters
import time
from player import Player, Other_player, Call_player
from ai import My_AI

white = (255, 64, 64)
green = (51, 204, 51)
dim = (1150, 750)
img_dim = (150, 217)
running = 1

# Players to play with GUI
input_players = [My_AI(0, "P1", 0, None, None), My_AI(1, "P2", 0, None, None), My_AI(2, "P3", 0, None, None)]


def get_card_image(card):
    if card is not None:
        file_path = 'img/' + parameters.CARD_VALUE[card[1] - 2] + '_of_' + parameters.CARD_TYPE[card[0]] + '.png'
        img = pygame.image.load(file_path)
        img = pygame.transform.scale(img, (img_dim[0], img_dim[1]))
        return img
    return None


def main():
    g = game.Texas_holdem()
    g.reset(input_players)
    pygame.init()
    screen = pygame.display.set_mode((dim[0], dim[1]))
    screen.fill(green)
    pygame.display.set_caption('Texas Holdem')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(green)

    screen.blit(background, (0, 0))
    pygame.display.flip()

    player_cards_pos = [[(200, dim[1] - img_dim[1]), (200 + img_dim[0], dim[1] - img_dim[1])],
                        [(200, 0), (200 + img_dim[0], 0)],
                        [(dim[0] - 2 * img_dim[0], 270), (dim[0] - img_dim[0], 270)]]
    player_text_pos = [[(10, dim[1] - img_dim[1]), (10, dim[1] - img_dim[1] + 30), (10, dim[1] - img_dim[1] + 60)],
                       [(10, 0), (10, 30), (10, 60)],
                       [(dim[0] - 2 * img_dim[0], 170), (dim[0] - 2 * img_dim[0], 200), (dim[0] - 2 * img_dim[0], 230)]]
    font = pygame.font.Font(None, 34)

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        screen.fill(green)
        cards = [g.get_board_card_by_index(0), g.get_board_card_by_index(1), g.get_board_card_by_index(2),
                 g.get_board_card_by_index(3), g.get_board_card_by_index(4)]
        if cards[0] is not None:
            screen.blit(get_card_image(cards[0]), (0, img_dim[1] + 50))
        if cards[1] is not None:
            screen.blit(get_card_image(cards[1]), (img_dim[0], img_dim[1] + 50))
        if cards[2] is not None:
            screen.blit(get_card_image(cards[2]), (2 * img_dim[0], img_dim[1] + 50))
        if cards[3] is not None:
            screen.blit(get_card_image(cards[3]), (3 * img_dim[0], img_dim[1] + 50))
        if cards[4] is not None:
            screen.blit(get_card_image(cards[4]), (4 * img_dim[0], img_dim[1] + 50))
        text_pot = font.render("Pot: " + str(g.pot), 1, (10, 10, 10))
        screen.blit(text_pot, (10, 220))

        for i, p in enumerate(g.players):
            text_p1 = font.render("Chips: " + str(p.chips), 1, (10, 10, 10))
            screen.blit(text_p1, player_text_pos[i][0])
            text_t2 = font.render("Bet: " + str(p.bet), 1, (10, 10, 10))
            screen.blit(text_t2, player_text_pos[i][1])
            text_t3 = font.render("Name: " + str(p.name), 1, (10, 10, 10))
            screen.blit(text_t3, player_text_pos[i][2])
            if p.bet >= 0:
                screen.blit(get_card_image(p.hand[0]), player_cards_pos[i][0])
                screen.blit(get_card_image(p.hand[1]), player_cards_pos[i][1])

        pygame.display.flip()

        # Do game stuff...
        g.play_one_step()

        time.sleep(parameters.ANIMATION_SPEED)


if __name__ == '__main__': main()