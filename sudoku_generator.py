import math
import random

"""
SudokuGenerator for 9x9 Sudoku boards.

Adapted from the GeeksforGeeks article:
"Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal.
"""


class SudokuGenerator:
    '''
    create a sudoku board - initialize class variables and set up the 2D board
    This should initialize:
        self.row_length     - the length of each row
        self.removed_cells  - the total number of cells to be removed
        self.board          - a 2D list of ints to represent the board
        self.box_length     - the square root of row_length

    Parameters:
        row_length is the number of rows/columns of the board (always 9 for this project)
        removed_cells is an integer value - the number of cells to be removed

    Return:
        None
    '''

    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.box_length = int(math.sqrt(row_length))
        self.board = [[0 for _ in range(row_length)] for _ in range(row_length)]

    '''
    Returns a 2D python list of numbers which represents the board
    '''

    def get_board(self):
        return self.board

    # Displays the board to the console (useful for debugging)
    def print_board(self):
        for row in self.board:
            print(" ".join(str(num) for num in row))

    '''
    Determines if num is contained in the specified row of the board
    If num is already in the specified row, return False. Otherwise, return True
    '''

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    '''
    Determines if num is contained in the specified column of the board
    If num is already in the specified col, return False. Otherwise, return True
    '''

    def valid_in_col(self, col, num):
        for row in self.board:
            if row[col] == num:
                return False
        return True

    '''
    Determines if num is contained in the 3x3 box specified on the board
    If num is in the specified box starting at (row_start, col_start), return False.
    Otherwise, return True
    '''

    def valid_in_box(self, row_start, col_start, num):
        for r in range(row_start, row_start + self.box_length):
            for c in range(col_start, col_start + self.box_length):
                if self.board[r][c] == num:
                    return False
        return True

    '''
    Determines if it is valid to enter num at (row, col) in the board.
    Checks row, column, and 3x3 box.
    '''

    def is_valid(self, row, col, num):
        if not self.valid_in_row(row, num):
            return False
        if not self.valid_in_col(col, num):
            return False
        row_start = row - (row % self.box_length)
        col_start = col - (col % self.box_length)
        if not self.valid_in_box(row_start, col_start, num):
            return False
        return True

    '''
    Fills the specified 3x3 box with values 1–9 without repetition
    '''

    def fill_box(self, row_start, col_start):
        nums = list(range(1, self.row_length + 1))
        random.shuffle(nums)
        idx = 0
        for r in range(self.box_length):
            for c in range(self.box_length):
                self.board[row_start + r][col_start + c] = nums[idx]
                idx += 1

    '''
    Fills the three boxes along the main diagonal of the board
    '''

    def fill_diagonal(self):
        for i in range(0, self.row_length, self.box_length):
            self.fill_box(i, i)

    '''
    Fills the remaining cells of the board after diagonal boxes
    (backtracking algorithm — provided)
    '''

    def fill_remaining(self, row, col):
        if col >= self.row_length and row < self.row_length - 1:
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row / self.box_length) * self.box_length:
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    '''
    Constructs a full Sudoku solution by filling diagonal boxes then remaining cells.
    Also stores a copy as self.solution_board for checking correctness later.
    '''

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)
        self.solution_board = [row[:] for row in self.board]

    '''
    Removes the appropriate number of cells from the board by setting values to 0.
    Avoids removing the same cell more than once.
    '''

    def remove_cells(self):
        removed = 0
        while removed < self.removed_cells:
            row = random.randint(0, self.row_length - 1)
            col = random.randint(0, self.row_length - 1)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                removed += 1
        return self.board


'''
generate_sudoku(size, removed)
Given size (9) and number of cells to remove, this creates a SudokuGenerator,
fills values, removes cells, and returns the puzzle board.
'''


def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    sudoku.remove_cells()
    return sudoku.get_board()
