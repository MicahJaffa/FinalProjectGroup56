import pygame
from sudoku_generator import SudokuGenerator


class Cell:
    def __init__(self, value, row, col, screen, cell_size):
        self.value = value
        self.sketched_value = 0
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False
        self.size = cell_size
        self.x = col * cell_size
        self.y = row * cell_size

        self.is_given = (value != 0)

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)


        if self.selected:
            pygame.draw.rect(self.screen, (255, 255, 200), rect)      # light yellow
            pygame.draw.rect(self.screen, (255, 0, 0), rect, 2)       # red border
        else:
            pygame.draw.rect(self.screen, (255, 255, 255), rect)      # white
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)         # black border

        value_font = pygame.font.SysFont("Arial", 32, bold=True)
        sketch_font = pygame.font.SysFont("Arial", 18)


        if self.value != 0:
            if self.is_given:
                color = (0, 0, 0)
            else:
                color = (20, 60, 200)

            text = value_font.render(str(self.value), True, color)
            text_rect = text.get_rect(center=(self.x + self.size / 2, self.y + self.size / 2))
            self.screen.blit(text, text_rect)


        elif self.sketched_value != 0:
            text = sketch_font.render(str(self.sketched_value), True, (150, 150, 150))
            self.screen.blit(text, (self.x + 5, self.y + 5))


class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty

        if difficulty == "easy":
            removed = 30
        elif difficulty == "medium":
            removed = 40
        else:
            removed = 50

        generator = SudokuGenerator(9, removed)
        generator.fill_values()

        self.solution = [row[:] for row in generator.solution_board]

        generator.remove_cells()
        puzzle = generator.board

        self.original = [row[:] for row in puzzle]


        self.cell_size = self.width // 9

        self.cells = []
        for r in range(9):
            row_cells = []
            for c in range(9):
                cell = Cell(puzzle[r][c], r, c, screen, self.cell_size)
                row_cells.append(cell)
            self.cells.append(row_cells)

        self.selected_cell = None

    def draw(self):
        cell_size = self.cell_size

        for i in range(10):
            line_width = 1
            if i % 3 == 0:
                line_width = 3
            pygame.draw.line(self.screen, (0, 0, 0),
                             (0, i * cell_size),
                             (self.width, i * cell_size),
                             line_width)
            pygame.draw.line(self.screen, (0, 0, 0),
                             (i * cell_size, 0),
                             (i * cell_size, self.height),
                             line_width)

        for row in self.cells:
            for cell in row:
                cell.draw()

    def select(self, row, col):
        if self.selected_cell is not None:
            r, c = self.selected_cell
            self.cells[r][c].selected = False
        self.cells[row][col].selected = True
        self.selected_cell = (row, col)

    def click(self, x, y):
        cell_size = self.cell_size
        if x < 0 or x > self.width or y < 0 or y > self.height:
            return None
        row = y // cell_size
        col = x // cell_size
        return int(row), int(col)

    def clear(self):
        if self.selected_cell is None:
            return
        r, c = self.selected_cell
        cell = self.cells[r][c]
        if cell.is_given:
            return
        cell.set_cell_value(0)
        cell.set_sketched_value(0)

    def sketch(self, value):
        if self.selected_cell is None:
            return
        r, c = self.selected_cell
        cell = self.cells[r][c]
        if cell.is_given:
            return
        cell.set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell is None:
            return
        r, c = self.selected_cell
        cell = self.cells[r][c]
        if cell.is_given:
            return
        cell.set_cell_value(value)

    def reset_to_original(self):
        for r in range(9):
            for c in range(9):
                self.cells[r][c].value = self.original[r][c]
                self.cells[r][c].sketched_value = 0

    def is_full(self):
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def update_board(self):
        board = []
        for r in range(9):
            row = []
            for c in range(9):
                row.append(self.cells[r][c].value)
            board.append(row)
        return board

    def find_empty(self):
        for r in range(9):
            for c in range(9):
                if self.cells[r][c].value == 0:
                    return (r, c)
        return None

    def check_board(self):
        for r in range(9):
            for c in range(9):
                if self.cells[r][c].value != self.solution[r][c]:
                    return False
        return True
