import pygame
from screen import Board


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (250, 70, 22)

pygame.init()
scr_w, scr_h = 460, 600
win = pygame.display.set_mode((scr_w, scr_h))
pygame.display.set_caption("Sudoku")


try:
    bg = pygame.image.load("sudoku.png").convert_alpha()
    bg = pygame.transform.scale(bg, (scr_w, scr_h))
except:
    bg = None


def txt_mid(surf, txt, box, size=30, col=BLACK):
    f = pygame.font.SysFont(None, size)
    t = f.render(str(txt), True, col)
    r = t.get_rect()
    r.center = box.center
    surf.blit(t, r)

scene = "start"
mode = ""
board_obj = None

running = True
while running:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False

        if ev.type == pygame.MOUSEBUTTONDOWN:
            mx, my = ev.pos


            if scene == "start":
                if 43 < mx < 130 and 200 < my < 251:
                    mode = "easy"
                elif 153 < mx < 231 and 200 < my < 251:
                    mode = "medium"
                elif 244 < mx < 322 and 200 < my < 251:
                    mode = "hard"
                if mode:
                    board_obj = Board(460, 460, win, mode)
                    scene = "play"


            elif scene in ("won", "over"):
                exit_btn = pygame.Rect(50, 200, 85, 55)
                if exit_btn.collidepoint(mx, my):
                    running = False


            elif scene == "play" and board_obj:
                cell = board_obj.click(mx, my)
                if cell:
                    board_obj.select(*cell)
                else:

                    reset_out = pygame.Rect(50, 500, 100, 55)
                    restart_out = pygame.Rect(160, 500, 100, 55)
                    exit_out = pygame.Rect(270, 500, 100, 55)

                    if reset_out.collidepoint(mx, my):
                        board_obj.reset_to_original()
                    elif restart_out.collidepoint(mx, my):
                        scene = "start"
                        mode = ""
                        board_obj = None
                    elif exit_out.collidepoint(mx, my):
                        running = False

        if ev.type == pygame.KEYDOWN and scene == "play" and board_obj:
            if ev.key in (pygame.K_1, pygame.K_KP1):
                board_obj.sketch(1)
            elif ev.key in (pygame.K_2, pygame.K_KP2):
                board_obj.sketch(2)
            elif ev.key in (pygame.K_3, pygame.K_KP3):
                board_obj.sketch(3)
            elif ev.key in (pygame.K_4, pygame.K_KP4):
                board_obj.sketch(4)
            elif ev.key in (pygame.K_5, pygame.K_KP5):
                board_obj.sketch(5)
            elif ev.key in (pygame.K_6, pygame.K_KP6):
                board_obj.sketch(6)
            elif ev.key in (pygame.K_7, pygame.K_KP7):
                board_obj.sketch(7)
            elif ev.key in (pygame.K_8, pygame.K_KP8):
                board_obj.sketch(8)
            elif ev.key in (pygame.K_9, pygame.K_KP9):
                board_obj.sketch(9)
            elif ev.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                sel = board_obj.selected_cell
                if sel:
                    r, c = sel
                    val = board_obj.sketch_board[r][c]
                    if val and val in range(1, 10):
                        board_obj.place_number(val)
                        if board_obj.is_full():
                            if board_obj.check_board():
                                scene = "won"
                            else:
                                scene = "over"
            elif ev.key == pygame.K_BACKSPACE:
                sel = board_obj.selected_cell
                if sel:
                    r, c = sel
                    board_obj.sketch_board[r][c] = 0
            elif ev.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                r, c = (0, 0) if board_obj.selected_cell is None else board_obj.selected_cell
                if ev.key == pygame.K_LEFT:
                    board_obj.select(r, max(0, c - 1))
                elif ev.key == pygame.K_RIGHT:
                    board_obj.select(r, min(8, c + 1))
                elif ev.key == pygame.K_UP:
                    board_obj.select(max(0, r - 1), c)
                elif ev.key == pygame.K_DOWN:
                    board_obj.select(min(8, r + 1), c)


    if scene == "start":
        if bg:
            win.blit(bg, (0, 0))
        else:
            win.fill(WHITE)

        txt_mid(win, "Welcome to Sudoku", pygame.Rect(120, 50, 200, 40), 30)
        txt_mid(win, "Select Game Mode:", pygame.Rect(120, 100, 300, 35), 25)

        for i, (txt, x) in enumerate([("EASY", 60), ("MEDIUM", 160), ("HARD", 250)]):
            b = pygame.Rect(x, 210, 65, 35)
            o = pygame.Rect(x-10, 200, 85, 55)
            pygame.draw.rect(win, ORANGE, b)
            pygame.draw.rect(win, BLACK, o, 5)
            txt_mid(win, txt, o, 15)

    elif scene == "play" and board_obj:
        win.fill(WHITE)
        board_obj.draw()

        f = pygame.font.SysFont(None, 26)
        for t, x in [("RESET", 50), ("RESTART", 160), ("EXIT", 270)]:
            rb = pygame.Rect(x + 10, 510, 80, 35)
            ro = pygame.Rect(x, 500, 100, 55)
            pygame.draw.rect(win, ORANGE, rb)
            pygame.draw.rect(win, BLACK, ro, 5)
            rt = f.render(t, True, BLACK)
            rt_r = rt.get_rect(center=ro.center)
            win.blit(rt, rt_r)

    elif scene in ("won", "over"):
        if bg:
            win.blit(bg, (0, 0))
        else:
            win.fill(WHITE)
        msg = "Game Won!" if scene == "won" else "Game Over :("
        txt_mid(win, msg, pygame.Rect(120, 50, 200, 40), 30)

        eo = pygame.Rect(50, 200, 85, 55)
        pygame.draw.rect(win, ORANGE, pygame.Rect(60, 210, 65, 35))
        pygame.draw.rect(win, BLACK, eo, 5)
        txt_mid(win, "EXIT", eo, 15)

    pygame.display.flip()

pygame.quit()
