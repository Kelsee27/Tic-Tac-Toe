import copy
import math
import sys
import random
import time as t

import numpy as np
import pygame

from constants import *

# Game setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BACKGROUND_COLOUR)
FPS = 2.5


class WinSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(WinSprite, self).__init__()
        self.images = [pygame.image.load('Images/Small_winner.png'),
                       pygame.image.load('Images/Med_winner.png'),
                       pygame.image.load('Images/Big_winner.png')]
        self.index = 0
        self.rect = pygame.Rect(0, 0, 600, 600)

    def update(self):
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        self.index += 1


class TieSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(TieSprite, self).__init__()
        self.images = [pygame.image.load('Images/Small_tie.png'),
                       pygame.image.load('Images/Med_tie.png'),
                       pygame.image.load('Images/Big_tie.png')]
        self.index = 0
        self.rect = pygame.Rect(0, 0, 600, 600)

    def update(self):
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
        self.index += 1


class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS, COLUMNS))
        self.empty_squares = self.squares
        self.marked_squares = 0

    def winning_state(self, show=False):
        """
        returns 0 is there is no win
        returns 1 if player 1 wins
        returns 2 if player 2 wins

        """

        # vertical wins
        for col in range(COLUMNS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = LINE_COLOUR
                    i_pos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, 20)
                    f_pos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, i_pos, f_pos, LINE_WIDTH)
                return self.squares[0][col]

        # horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = LINE_COLOUR
                    i_pos = (20, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    f_pos = (WIDTH - 20, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    pygame.draw.line(screen, color, i_pos, f_pos, LINE_WIDTH)
                return self.squares[row][0]

        # diagonal wins
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = LINE_COLOUR
                i_pos = (20, 20)
                f_pos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, i_pos, f_pos, LINE_WIDTH)
            return self.squares[1][1]

        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = LINE_COLOUR
                i_pos = (20, HEIGHT - 20)
                f_pos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, i_pos, f_pos, LINE_WIDTH)
            return self.squares[1][1]

        return 0

    def mark_square(self, row, column, player):
        self.squares[row][column] = player
        self.marked_squares += 1

    def empty_square(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_squares(self):
        empty_squares = []
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.empty_square(row, col):
                    empty_squares.append((row, col))

        return empty_squares

    def full_board(self):
        return self.marked_squares == 9

    def empty_board(self):
        return self.marked_squares == 0


class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def rand_choice(self, board):
        empty_squares = board.get_empty_squares()
        index = random.randrange(0, len(empty_squares))
        return empty_squares[index]

    def minimax(self, board, maximizing):
        case = board.winning_state()

        if case == 1:
            return 1, None  # eval move
        if case == 2:
            return -1, None
        if board.full_board():
            return 0, None

        if maximizing:
            max_eval = -math.inf
            best_move = None
            empty_sqrs = board.get_empty_squares()

            for row, col in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)
                ai_eval = self.minimax(temp_board, False)[0]
                if ai_eval > max_eval:
                    max_eval = ai_eval
                    best_move = (row, col)
            return max_eval, best_move

        elif not maximizing:
            min_eval = math.inf
            best_move = None
            empty_sqrs = board.get_empty_squares()

            for row, col in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, self.player)
                ai_eval = self.minimax(temp_board, True)[0]
                if ai_eval < min_eval:
                    min_eval = ai_eval
                    best_move = (row, col)
            return min_eval, best_move

    def eval(self, game_board):
        start = t.time()
        if self.level == 0:
            ai_eval = 'random'
            move = self.rand_choice(game_board)
        else:
            ai_eval, move = self.minimax(game_board, False)

        end = t.time()
        print(f'AI has chosen to mark the square in position {move}')
        print(f'Eval = {ai_eval}')
        print(f'Eval Time = {round(end - start, 7)}\n')

        return move


class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.running = True
        self.show_lines()

    def show_lines(self):
        screen.fill(BACKGROUND_COLOUR)
        # Vertical
        pygame.draw.line(screen, LINE_COLOUR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (WIDTH - SQUARE_SIZE, 0), (WIDTH - SQUARE_SIZE, HEIGHT), LINE_WIDTH)

        # Horizontal
        pygame.draw.line(screen, LINE_COLOUR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (0, HEIGHT - SQUARE_SIZE), (WIDTH, HEIGHT - SQUARE_SIZE), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            bee = pygame.image.load('Images/bee.png')
            bee.convert()

            bee_rect = bee.get_rect()

            bee_rect.center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
            screen.blit(bee, bee_rect)
            pygame.draw.rect(screen, BACKGROUND_COLOUR, bee_rect, 1)

        elif self.player == 2:
            flower = pygame.image.load('Images/flower.png')
            flower.convert()

            flower_rect = flower.get_rect()

            flower_rect.center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
            screen.blit(flower, flower_rect)
            pygame.draw.rect(screen, BACKGROUND_COLOUR, flower_rect, 1)

    def make_move(self, row, col):
        self.board.mark_square(row, col, self.player)
        self.draw_fig(row, col)
        self.next_player()

    def next_player(self):
        self.player = self.player % 2 + 1

    def is_over(self):
        return self.board.winning_state(show=True) != 0 or self.board.full_board()

    def reset(self):
        self.__init__()


def main():
    game = Game()
    board = game.board
    ai = game.ai

    # main loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                if event.key == pygame.K_0:
                    ai.level = 0

                if event.key == pygame.K_1:
                    ai.level = 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQUARE_SIZE
                col = pos[0] // SQUARE_SIZE

                if board.empty_square(row, col) and game.running:
                    game.make_move(row, col)

                    if game.is_over():
                        game.running = False
                        tie_sprite = TieSprite()
                        tie_group = pygame.sprite.Group(tie_sprite)
                        clock = pygame.time.Clock()
                        loop = 1
                        background = screen.copy()
                        while loop:
                            for e in pygame.event.get():
                                if e.type == pygame.KEYDOWN:
                                    tie_sprite.kill()
                                    game.reset()
                                    board = game.board
                                    ai = game.ai
                                    background = screen.copy()
                                    loop = 0
                                elif e.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()

                            screen.blit(background, (0, 0))
                            tie_group.update()
                            tie_group.draw(screen)
                            pygame.display.flip()
                            clock.tick(FPS)

                if game.player == ai.player and game.running:
                    pygame.display.update()

                    # AI methods
                    row, col = ai.eval(board)
                    game.make_move(row, col)

                    if game.is_over():
                        game.running = False
                        my_sprite = WinSprite()
                        my_group = pygame.sprite.Group(my_sprite)
                        clock = pygame.time.Clock()
                        loop = 1
                        background = screen.copy()
                        while loop:
                            for e in pygame.event.get():
                                if e.type == pygame.KEYDOWN:
                                    my_sprite.kill()
                                    game.reset()
                                    board = game.board
                                    ai = game.ai
                                    background = screen.copy()
                                    loop = 0
                                elif e.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()

                            screen.blit(background, (0, 0))
                            my_group.update()
                            my_group.draw(screen)
                            pygame.display.flip()
                            clock.tick(FPS)

        pygame.display.update()


main()
