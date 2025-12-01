import pygame, copy
from sudoku_generator import SudokuGenerator

class Cell():
    def __init__(self, value, row, col, screen, sketch=0):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketch = sketch
        self.selected = False
        self.font = pygame.font.SysFont(None, 40)
        self.small_font = pygame.font.SysFont(None, 24)

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketch = value

    def draw(self):
        CELL_SIZE = getattr(self, "cell_size", 50)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        GRAY = (150, 150, 150)
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(self.screen, (255, 255, 255), rect)
        outline_color = RED if getattr(self, "selected", False) else BLACK
        pygame.draw.rect(self.screen, outline_color, rect, 2)

        if self.value not in (0, None):
            number_surface = self.font.render(str(self.value), True, BLACK)
            number_rect = number_surface.get_rect(center=rect.center)
            self.screen.blit(number_surface, number_rect)
        elif self.sketch not in (0, None):
            sketch_surface = self.small_font.render(str(self.sketch), True, GRAY)
            sketch_rect = sketch_surface.get_rect()
            sketch_rect.topleft = (x + 5, y + 3)
            self.screen.blit(sketch_surface, sketch_rect)


class Board():
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.cell_size = self.width // 9
        self.screen = screen
        self.difficulty = difficulty
        self.font = pygame.font.SysFont(None, 40)
        self.small_font = pygame.font.SysFont(None, 24)

        self.numberRemoved = 0
        self.play_board = []
        self.selected_cell = None
        self.sketch_board = []

        if self.difficulty == "easy":
            self.numberRemoved = 30
        elif self.difficulty == "medium":
            self.numberRemoved = 40
        else:
            self.numberRemoved = 50

        generator = SudokuGenerator(9, self.numberRemoved)
        generator.fill_values()

        self.solution = copy.deepcopy(generator.get_board())

        generator.remove_cells()

        self.original_board = copy.deepcopy(generator.get_board())
        self.play_board = copy.deepcopy(generator.get_board())


        self.cells = []
        for i in range(9):
            row_list = []
            for j in range(9):
                cell = Cell(self.play_board[i][j], i, j, self.screen)
                cell.cell_size = self.cell_size
                row_list.append(cell)
            self.cells.append(row_list)


        rows = 9
        cols = 9
        self.sketch_board =[]
        for i in range(rows):
            row_list = []
            for j in range(cols):
                row_list.append(0)
            self.sketch_board.append(row_list)


    def draw(self):
        BLACK = (0, 0, 0)
        rows = 9
        cols = 9
        CELL_SIZE = self.cell_size
        board_pixel_width = cols * CELL_SIZE
        board_pixel_height = rows * CELL_SIZE
        for i in range(rows):
            for j in range(cols):
                cell = self.cells[i][j]
                cell.value = self.play_board[i][j]
                cell.sketch = self.sketch_board[i][j]
                if self.selected_cell is not None:
                    sel_r, sel_c = self.selected_cell
                    cell.selected = (sel_r == i and sel_c == j)
                else:
                    cell.selected = False
                cell.draw()
        for i in range(rows + 1):
            thickness = 4 if i % 3 == 0 else 1
            y = i * CELL_SIZE
            pygame.draw.line(self.screen, BLACK, (0, y), (board_pixel_width, y), thickness)
        for j in range(cols + 1):
            thickness = 4 if j % 3 == 0 else 1
            x = j * CELL_SIZE
            pygame.draw.line(self.screen, BLACK, (x, 0), (x, board_pixel_height), thickness)
        return

    def select(self, row, col):
        if row < 0 or row > 8 or col < 0 or col > 8:
            return
        self.selected_cell = (row, col)

    def click(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            col = x // self.cell_size
            row = y // self.cell_size
            return (int(row), int(col))
        return None

    def clear(self):
        if self.selected_cell is None:
            return
        row, col = self.selected_cell

        if self.original_board[row][col] == 0:
            self.play_board[row][col] = 0
            self.sketch_board[row][col] = 0
            self.cells[row][col].set_cell_value(0)
            self.cells[row][col].set_sketched_value(0)

    def sketch(self, value):
        if not self.selected_cell:
            return
        row, col = self.selected_cell
        if self.original_board[row][col] == 0:
            self.sketch_board[row][col] = value

    def place_number(self, value):
        if not self.selected_cell:
            return
        row, col = self.selected_cell
        if self.original_board[row][col] == 0:
            self.play_board[row][col] = value
            self.sketch_board[row][col] = 0

    def reset_to_original(self):
        self.play_board = copy.deepcopy(self.original_board)

        rows = 9
        cols = 9
        self.sketch_board = []
        for i in range(rows):
            current_row = []
            for j in range(cols):
                current_row.append(0)
            self.sketch_board.append(current_row)

        for i in range(9):
            for j in range(9):
                self.cells[i][j].value = self.play_board[i][j]
                self.cells[i][j].sketch = 0

        self.selected_cell = None

    def is_full(self):
        for i in range(len(self.play_board)):
            for num in self.play_board[i]:
                if num == 0:
                    return False
        return True

    def update_board(self):
        new_board = []
        for r in range(9):
            row = []
            for c in range(9):
                row.append(self.cells[r][c].value)
            new_board.append(row)
        self.play_board = new_board
        return new_board

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.play_board[i][j] == 0:
                    z = (i, j)
                    return z
        return None

    def check_board(self):
        return self.play_board == self.solution
