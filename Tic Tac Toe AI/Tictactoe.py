#-----IMPORT LIBRARIES-----
import pygame
import sys
import math

from values import *

# -----INITIALIZE PYGAME------

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI')
font = pygame.font.Font("OpenSans-Regular.ttf", 74)

def draw_lines():
    pygame.draw.line(screen, WHITE, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, WHITE, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, WHITE, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, WHITE, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, BLACK, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, BLACK, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, WHITE, (int(col * SQUARE_SIZE + SQUARE_SIZE / 2), int(row * SQUARE_SIZE + SQUARE_SIZE / 2)), 
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)

def check_winner():
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            return board[row][0]
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                return None
    return 'Tie'
 
#-------MINIMAX ALGORIHTM WITH ALPHA BETA PRUNING-------
def minimax(board, depth, is_maximizing, alpha, beta):
    result = check_winner()
    if result == 'X':
        return 1
    if result == 'O':
        return -1
    if result == 'Tie':
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] is None:
                    board[row][col] = 'X'
                    eval = minimax(board, depth + 1, False, alpha, beta)
                    board[row][col] = None
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] is None:
                    board[row][col] = 'O'
                    eval = minimax(board, depth + 1, True, alpha, beta)
                    board[row][col] = None
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def best_move():
    best_score = -math.inf
    move = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                board[row][col] = 'X'
                score = minimax(board, 0, False, -math.inf, math.inf)
                board[row][col] = None
                if score > best_score:
                    best_score = score
                    move = (row, col)
    return move

#-------WINNER--------

def display_winner(winner):
    text = ""
    if winner == 'X':
        text = "AI wins!"
    elif winner == 'O':
        text = "Player wins!"
    elif winner == 'Tie':
        text = "It's a tie!"

    label = font.render(text, True, WHITE)
    screen.fill(CHARCOAL)
    screen.blit(label, (WIDTH // 2 - label.get_width() // 2, HEIGHT // 2 - label.get_height() // 2))
    pygame.display.update()

def display_initial_message():
    screen.fill(PINK)
    text = font.render("Play as O", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))  # Centered
    pygame.display.update()
    pygame.time.wait(2000)  # Display message for 2 seconds

def restart():
    global board, player, game_over
    board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]
    player = 'O'
    game_over = False
    screen.fill(BROWN)
    draw_lines()

display_initial_message()
screen.fill(BROWN)
draw_lines()

player = 'O'
game_over = False
board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // SQUARE_SIZE
            mouseY = event.pos[1] // SQUARE_SIZE

            if board[mouseY][mouseX] is None:
                board[mouseY][mouseX] = player
                draw_figures()
                winner = check_winner()
                if winner is None:
                    player = 'X'
                    ai_move = best_move()
                    if ai_move:
                        board[ai_move[0]][ai_move[1]] = player
                        draw_figures()
                        winner = check_winner()
                        if winner is not None:
                            game_over = True
                            display_winner(winner)
                    player = 'O'
                else:
                    game_over = True
                    display_winner(winner)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()

    pygame.display.update()
