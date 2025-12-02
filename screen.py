
import sudoku_generator
import pygame
from sudoku_generator import SudokuGenerator

class Cell():
    def __init__(self, value, row, col, screen):
        self.value = value
        self.sketched_value = 0
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False
        self.size = 60
        self.x = col * self.size
        self.y = row * self.size
        self.is_given = (value != 0)

    def set_cell_value(self, value):
        self.value=value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), rect, 1)
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

        font = pygame.font.SysFont("Comic Sans", 32)

        if self.value != 0:
            text = font.render(str(self.value), True, (0, 0, 0))
            text_rect = text.get_rect(center=(self.x + self.size / 2, self.y + self.size / 2))
            self.screen.blit(text, text_rect)


class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty

        if difficulty == "easy":
            less = 30
        elif difficulty == "medium":
            less = 40
        else:
            less = 50

        generator = SudokuGenerator(9, less)
        generator.fill_values()
        self.solution = generator.solution_board
        self.original = [row[:] for row in generator.board]

        generator.remove_cells()
        puzzle = generator.board

        self.cells = []
        cell_size = width // 9

        for row in range(9):
            row_cells = []
            for col in range(9):
                cell = Cell(puzzle[row][col], row, col, screen)
                row_cells.append(cell)
            self.cells.append(row_cells)

        self.selected_cell = None

    def draw(self):
        cell_size = self.width // 9
        for i in range(10):
            line_width = 1
            if i % 3 == 0:
                line_width = 3
            pygame.draw.line(self.screen,(0, 0, 0),(0, i * cell_size),(self.width, i * cell_size), line_width)
            pygame.draw.line(self.screen,(0, 0, 0),(i * cell_size, 0),(i * cell_size, self.height),line_width)

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
        cell_size = self.width // 9

        if x < 0 or x > self.width or y < 0 or y > self.height:
            return None

        row = y // cell_size
        col = x // cell_size

        return int(row), int(col)

    def clear(self):
        if self.selected_cell is None:
            return
        row, col = self.selected_cell
        self.cells[row][col].set_cell_value(0)
        self.cells[row][col].set_sketched_value(0)

    def sketch(self, value):
        if self.selected_cell is None:
            return
        row, col = self.selected_cell
        self.cells[row][col].set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell is None:
            return
        row, col = self.selected_cell
        self.cells[row][col].set_cell_value(value)

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