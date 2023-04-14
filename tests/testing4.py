# Testing AI vs. AI with a 5 x 5 board

import copy
import math
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


class Board:
    def __init__(self):
        self.squares = np.zeros((LARGE_ROWS, LARGE_COLUMNS))
        self.empty_squares = self.squares
        self.marked_squares = 0

    def winning_state(self, show=False):
        """
        returns 0 is there is no win
        returns 1 if player 1 wins
        returns 2 if player 2 wins

        """

        # vertical wins
        for col in range(LARGE_COLUMNS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] == self.squares[3][col] \
                    == self.squares[4][col] != 0:
                if show:
                    color = LINE_COLOUR
                    i_pos = (col * LARGE_SQUARE_SIZE + LARGE_SQUARE_SIZE // 2, 20)
                    f_pos = (col * LARGE_SQUARE_SIZE + LARGE_SQUARE_SIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, i_pos, f_pos, LINE_WIDTH)
                return self.squares[0][col]

        # horizontal wins
        for row in range(LARGE_ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] == self.squares[row][3] \
                    == self.squares[row][4] != 0:
                if show:
                    color = LINE_COLOUR
                    i_pos = (20, row * LARGE_SQUARE_SIZE + LARGE_SQUARE_SIZE // 2)
                    f_pos = (WIDTH - 20, row * LARGE_SQUARE_SIZE + LARGE_SQUARE_SIZE // 2)
                    pygame.draw.line(screen, color, i_pos, f_pos, LINE_WIDTH)
                return self.squares[row][0]

        # diagonal wins
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] == self.squares[3][3] == self.squares[4][4] != 0:
            if show:
                color = LINE_COLOUR
                i_pos = (20, 20)
                f_pos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, i_pos, f_pos, LINE_WIDTH)
            return self.squares[1][1]

        if self.squares[4][0] == self.squares[3][1] == self.squares[2][2] == self.squares[1][3] == self.squares[0][4] != 0:
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
        for row in range(LARGE_ROWS):
            for col in range(LARGE_COLUMNS):
                if self.empty_square(row, col):
                    empty_squares.append((row, col))

        return empty_squares

    def full_board(self):
        return self.marked_squares == 25

    def empty_board(self):
        return self.marked_squares == 0


class AI:
    def __init__(self, level=1, player=1 or 2):
        self.level = level
        self.player = player

    def minimax(self, board, alpha, beta, maximizing, depth):
        case = board.winning_state()

        if case == 1:
            return 1, None  # eval move
        if case == 2:
            return -1, None
        if board.full_board() or depth == 10:
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

    def eval(self, game_board, player):
        self.player = player

        start = t.time()
        if player == 1:
            ai_eval, move = self.minimax(game_board, -math.inf, math.inf, True, 0)
        else:
            ai_eval, move = self.minimax(game_board, -math.inf, math.inf, False, 0)

        end = t.time()
        print(f'Player:{player} has chosen to mark the square in position {move}')
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
        pygame.draw.line(screen, LINE_COLOUR, (LARGE_SQUARE_SIZE, 0), (LARGE_SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (120, 0), (120, HEIGHT),
                         LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (240, 0), (240, HEIGHT),
                         LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (360, 0), (360, HEIGHT),
                         LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (480, 0), (480, HEIGHT),
                         LINE_WIDTH)

        # Horizontal
        pygame.draw.line(screen, LINE_COLOUR, (0, LARGE_SQUARE_SIZE), (WIDTH, LARGE_SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (0, 120), (WIDTH, 120), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (0, 240), (WIDTH, 240), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (0, 360), (WIDTH, 360), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (0, 480), (WIDTH, 480), LINE_WIDTH)

    def draw_fig(self, row, col):
        if self.player == 1:
            husky = pygame.image.load('/Users/kelseecarmichael/PycharmProjects/TicTacToe/Images/husky.png')
            husky = pygame.transform.scale(husky, (100, 100))
            husky.convert()

            husky_rect = husky.get_rect()

            husky_rect.center = (
                col * LARGE_SQUARE_SIZE + LARGE_SQUARE_SIZE // 2, row * LARGE_SQUARE_SIZE + LARGE_SQUARE_SIZE // 2)
            screen.blit(husky, husky_rect)
            pygame.draw.rect(screen, BACKGROUND_COLOUR, husky_rect, 1)

        elif self.player == 2:
            cat = pygame.image.load('/Users/kelseecarmichael/PycharmProjects/TicTacToe/Images/cat.png')
            cat = pygame.transform.scale(cat, (100, 100))
            cat.convert()

            cat_rect = cat.get_rect()

            cat_rect.center = (
                col * LARGE_SQUARE_SIZE + LARGE_SQUARE_SIZE // 2, row * LARGE_SQUARE_SIZE + LARGE_SQUARE_SIZE // 2)
            screen.blit(cat, cat_rect)
            pygame.draw.rect(screen, BACKGROUND_COLOUR, cat_rect, 1)

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
    game_count = 0
    game_limit = 5
    player1_wins = 0
    player2_wins = 0
    tie_games = 0

    # main game loop
    while game_count != game_limit:
        for event in pygame.event.get():
            if game.is_over():
                print("\n---------------------------New Game----------------------------\n")
                game.reset()
                board = game.board
                ai = game.ai
                game_count += 1

            elif game.player == 1 and game.running:
                pygame.display.update()

                # AI methods
                row, col = ai.eval(board, 1)
                game.make_move(row, col)

                if game.board.winning_state() == 1:
                    player1_wins += 1

                elif game.board.full_board():
                    tie_games += 1

            elif game.player == 2 and game.running:
                pygame.display.update()

                # AI methods
                row, col = ai.eval(board, 2)
                game.make_move(row, col)

                if game.board.winning_state() == 2:
                    player2_wins += 1

        # Print out final results at the end of testing loop
        if game_count == game_limit:
            print(f'Player 1 wins: {player1_wins}\nPlayer 2 wins: {player2_wins}\nTie games: {tie_games}')

        pygame.display.update()


main()
