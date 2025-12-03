import sys
import pygame
from screen import Board

pygame.init()

WINDOW_WIDTH = 540
BOARD_HEIGHT = 540
WINDOW_HEIGHT = 600

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sudoku")

FONT_LARGE = pygame.font.SysFont(None, 48)
FONT_MED = pygame.font.SysFont(None, 32)
FONT_SMALL = pygame.font.SysFont(None, 24)

def draw_text_center(text, font, color, surface, center):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=center)
    surface.blit(surf, rect)

def start_screen():

    easy_rect = pygame.Rect(60, 300, 120, 50)
    medium_rect = pygame.Rect(210, 300, 120, 50)
    hard_rect = pygame.Rect(360, 300, 120, 50)

    while True:
        SCREEN.fill((255, 255, 255))

        draw_text_center("Welcome to Sudoku", FONT_LARGE, (0, 0, 0),
                         SCREEN, (WINDOW_WIDTH // 2, 150))
        draw_text_center("Select Difficulty", FONT_MED, (0, 0, 0),
                         SCREEN, (WINDOW_WIDTH // 2, 220))

        mouse_pos = pygame.mouse.get_pos()


        for rect, label in [(easy_rect, "Easy"),
                            (medium_rect, "Medium"),
                            (hard_rect, "Hard")]:
            color = (200, 200, 200)
            if rect.collidepoint(mouse_pos):
                color = (170, 170, 170)
            pygame.draw.rect(SCREEN, color, rect)
            pygame.draw.rect(SCREEN, (0, 0, 0), rect, 2)
            draw_text_center(label, FONT_SMALL, (0, 0, 0),
                             SCREEN, rect.center)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if easy_rect.collidepoint(event.pos):
                    return "easy"
                if medium_rect.collidepoint(event.pos):
                    return "medium"
                if hard_rect.collidepoint(event.pos):
                    return "hard"

        pygame.display.flip()


def end_screen(won):

    message = "Game Won!" if won else "Game Over :("

    while True:
        SCREEN.fill((255, 255, 255))

        draw_text_center(message, FONT_LARGE, (0, 0, 0),
                         SCREEN, (WINDOW_WIDTH // 2, 200))
        draw_text_center("Press R to Restart", FONT_MED, (0, 0, 0),
                         SCREEN, (WINDOW_WIDTH // 2, 280))
        draw_text_center("Press Esc to Exit", FONT_MED, (0, 0, 0),
                         SCREEN, (WINDOW_WIDTH // 2, 330))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

def game_loop(difficulty):

    board = Board(540, BOARD_HEIGHT, SCREEN, difficulty)


    reset_rect = pygame.Rect(40, 550, 120, 35)
    restart_rect = pygame.Rect(210, 550, 120, 35)
    exit_rect = pygame.Rect(380, 550, 120, 35)

    running = True

    while running:
        SCREEN.fill((255, 255, 255))


        board.draw()


        mouse_pos = pygame.mouse.get_pos()
        for rect, label in [(reset_rect, "Reset"),
                            (restart_rect, "Restart"),
                            (exit_rect, "Exit")]:
            color = (200, 200, 200)
            if rect.collidepoint(mouse_pos):
                color = (170, 170, 170)
            pygame.draw.rect(SCREEN, color, rect)
            pygame.draw.rect(SCREEN, (0, 0, 0), rect, 2)
            draw_text_center(label, FONT_SMALL, (0, 0, 0),
                             SCREEN, rect.center)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if y < BOARD_HEIGHT:

                    clicked = board.click(x, y)
                    if clicked is not None:
                        row, col = clicked
                        board.select(row, col)
                else:

                    if reset_rect.collidepoint(event.pos):
                        board.reset_to_original()
                    elif restart_rect.collidepoint(event.pos):
                        return
                    elif exit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()


            if event.type == pygame.KEYDOWN:

                if pygame.K_1 <= event.key <= pygame.K_9:
                    value = event.key - pygame.K_0
                    board.sketch(value)


                if event.key in (pygame.K_BACKSPACE, pygame.K_DELETE):
                    board.clear()


                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if board.selected_cell is not None:
                        r, c = board.selected_cell
                        cell = board.cells[r][c]
                        if cell.sketched_value != 0:
                            board.place_number(cell.sketched_value)


                if event.key in (pygame.K_UP, pygame.K_DOWN,
                                 pygame.K_LEFT, pygame.K_RIGHT):
                    if board.selected_cell is None:
                        board.select(0, 0)
                    else:
                        r, c = board.selected_cell
                        if event.key == pygame.K_UP and r > 0:
                            r -= 1
                        elif event.key == pygame.K_DOWN and r < 8:
                            r += 1
                        elif event.key == pygame.K_LEFT and c > 0:
                            c -= 1
                        elif event.key == pygame.K_RIGHT and c < 8:
                            c += 1
                        board.select(r, c)


        if board.is_full():

            if board.check_board():
                end_screen(won=True)
            else:
                end_screen(won=False)
            return

        pygame.display.flip()

def main():
    while True:
        difficulty = start_screen()
        game_loop(difficulty)


if __name__ == "__main__":
    main()