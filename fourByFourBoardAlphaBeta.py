# This implementation uses alpha beta pruning with a 4x4 board

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
pygame.display.set_caption('Tic Tac Toe Alpha-Beta')
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
        self.squares = np.zeros((MEDIUM_ROWS, MEDIUM_COLUMNS))
        self.empty_squares = self.squares
        self.marked_squares = 0

    def winning_state(self, show=False):
        """
        returns 0 is there is no win
        returns 1 if player 1 wins
        returns 2 if player 2 wins

        """

        # vertical wins
        for col in range(MEDIUM_COLUMNS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] == self.squares[3][col] != 0:
                if show:
                    color = LINE_COLOUR
                    i_pos = (col * MEDIUM_SQUARE_SIZE + MEDIUM_SQUARE_SIZE // 2, 20)
                    f_pos = (col * MEDIUM_SQUARE_SIZE + MEDIUM_SQUARE_SIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, i_pos, f_pos, LINE_WIDTH)
                return self.squares[0][col]

        # horizontal wins
        for row in range(MEDIUM_ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] == self.squares[row][3] != 0:
                if show:
                    color = LINE_COLOUR
                    i_pos = (20, row * MEDIUM_SQUARE_SIZE + MEDIUM_SQUARE_SIZE // 2)
                    f_pos = (WIDTH - 20, row * MEDIUM_SQUARE_SIZE + MEDIUM_SQUARE_SIZE // 2)
                    pygame.draw.line(screen, color, i_pos, f_pos, LINE_WIDTH)
                return self.squares[row][0]

        # diagonal wins
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] == self.squares[3][3] != 0:
            if show:
                color = LINE_COLOUR
                i_pos = (20, 20)
                f_pos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, i_pos, f_pos, LINE_WIDTH)
            return self.squares[1][1]

        if self.squares[3][0] == self.squares[2][1] == self.squares[1][2] == self.squares[0][3] != 0:
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
        for row in range(MEDIUM_ROWS):
            for col in range(MEDIUM_COLUMNS):
                if self.empty_square(row, col):
                    empty_squares.append((row, col))

        return empty_squares

    def full_board(self):
        return self.marked_squares == 16

    def empty_board(self):
        return self.marked_squares == 0


def rand_choice(board):
    empty_squares = board.get_empty_squares()
    index = random.randrange(0, len(empty_squares))
    return empty_squares[index]


class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def minimax(self, board, alpha, beta, maximizing, depth):
        case = board.winning_state()

        if case == 1:
            return 1, None  # eval move
        if case == 2:
            return -1, None
        if board.full_board() or depth == 8:
            return 0, None

        if maximizing:
            max_eval = -math.inf
            best_move = None
            empty_sqrs = board.get_empty_squares()

            for row, col in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)
                ai_eval = self.minimax(temp_board, alpha, beta, False, depth + 1)[0]
                if ai_eval > max_eval:
                    max_eval = ai_eval
                    best_move = (row, col)
                #  Alpha beta pruning being performed here
                alpha = max(alpha, ai_eval)
                if beta <= alpha:
                    break
            return max_eval, best_move

        elif not maximizing:
            min_eval = math.inf
            best_move = None
            empty_sqrs = board.get_empty_squares()

            for row, col in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, self.player)
                ai_eval = self.minimax(temp_board, alpha, beta, True, depth + 1)[0]
                if ai_eval < min_eval:
                    min_eval = ai_eval
                    best_move = (row, col)
                #  Alpha beta pruning being performed here
                beta = min(beta, ai_eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def eval(self, game_board):
        start = t.time()
        if self.level == 0:
            ai_eval = 'random'
            move = rand_choice(game_board)
        else:
            ai_eval, move = self.minimax(game_board, -math.inf, math.inf, False, 0)

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
        pygame.draw.line(screen, LINE_COLOUR, (MEDIUM_SQUARE_SIZE, 0), (MEDIUM_SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (150, 0), (150, HEIGHT),
                         LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (300, 0), (300, HEIGHT),
                         LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (450, 0), (450, HEIGHT),
                         LINE_WIDTH)

        # Horizontal
        pygame.draw.line(screen, LINE_COLOUR, (0, MEDIUM_SQUARE_SIZE), (WIDTH, MEDIUM_SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (0, 150), (WIDTH, 150), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (0, 300), (WIDTH, 300), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (0, 450), (WIDTH, 450), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            husky = pygame.image.load('Images/husky.png')
            husky = pygame.transform.scale(husky, (100, 100))
            husky.convert()

            husky_rect = husky.get_rect()

            husky_rect.center = (col * MEDIUM_SQUARE_SIZE + MEDIUM_SQUARE_SIZE // 2, row * MEDIUM_SQUARE_SIZE + MEDIUM_SQUARE_SIZE // 2)
            screen.blit(husky, husky_rect)
            pygame.draw.rect(screen, BACKGROUND_COLOUR, husky_rect, 1)

        elif self.player == 2:
            cat = pygame.image.load('Images/cat.png')
            cat = pygame.transform.scale(cat, (100, 110))
            cat.convert()

            cat_rect = cat.get_rect()

            cat_rect.center = (col * MEDIUM_SQUARE_SIZE + MEDIUM_SQUARE_SIZE // 2, row * MEDIUM_SQUARE_SIZE + MEDIUM_SQUARE_SIZE // 2)
            screen.blit(cat, cat_rect)
            pygame.draw.rect(screen, BACKGROUND_COLOUR, cat_rect, 1)

    def make_move(self, row, col):
        self.board.mark_square(row, col, self.player)
        self.draw_fig(row, col)
        self.next_player()

    def next_player(self):
        self.player = self.player % 2 + 1

    def reset(self):
        self.__init__()


def main():
    game = Game()
    board = game.board
    ai = game.ai

    # main game loop
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

            if game.board.winning_state() == 2:
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

            if game.board.full_board():
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


            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // MEDIUM_SQUARE_SIZE
                col = pos[0] // MEDIUM_SQUARE_SIZE

                if board.empty_square(row, col) and game.running:
                    game.make_move(row, col)

                if game.player == ai.player and game.running:
                    pygame.display.update()

                    # AI methods
                    row, col = ai.eval(board)
                    game.make_move(row, col)


        pygame.display.update()


main()
