import math
import itertools
import numpy
import copy


def avoids(permutation, pattern):
    if len(permutation) < len(pattern):
        return True
    elif len(permutation) == len(pattern):
        return permutation != pattern
    else:
        # print(f"Checking {permutation}")
        return all(avoids(tuple(numpy.argsort(sub)), pattern)
                   for sub in itertools.combinations(permutation, len(pattern)))


def avoiding_permutations(n, pattern):
    return [permutation for permutation in itertools.permutations(range(n)) if avoids(permutation, pattern)]


def valid_sudoku(n, d, row_pattern, column_pattern, board):
    return valid_rows(n, d, row_pattern, column_pattern, board) \
        and valid_columns(n, d, row_pattern, column_pattern, board) \
        and valid_boxes(n, d, row_pattern, column_pattern, board)


def valid_rows(n, d, row_pattern, column_pattern, board):
    return all(valid_row(n, d, row_pattern, column_pattern, board, i) for i in range(n))


def valid_row(n, d, row_pattern, column_pattern, board, i):
    row = [board[i][j] for j in range(n) if board[i][j] is not None]
    return len(row) == len(set(row)) and avoids(tuple(row), row_pattern)


def valid_columns(n, d, row_pattern, column_pattern, board):
    return all(valid_column(n, d, row_pattern, column_pattern, board, j) for j in range(n))


def valid_column(n, d, row_pattern, column_pattern, board, j):
    column = [board[i][j] for i in range(n) if board[i][j] is not None]
    return len(column) == len(set(column)) and avoids(tuple(column), column_pattern)


def valid_boxes(n, d, row_pattern, column_pattern, board):
    return all(valid_box(n, d, row_pattern, column_pattern, board, k) for k in range(n))


def valid_box(n, d, row_pattern, column_pattern, board, k):
    box = [board[i][j]
           for j in range((k % math.floor(n / d)) * d, ((k % math.floor(n / d)) + 1) * d)
           for i in range(math.floor(k * d / n) * math.floor(n / d), (math.floor(k * d / n) + 1) * math.floor(n / d))
           if board[i][j] is not None]
    return len(box) == len(set(box))


def previous_cell(n, d, puzzle, cell):
    if cell[1] > 0:
        possible = [cell[0], cell[1] - 1]
    elif cell[0] > 0:
        possible = [cell[0] - 1, n - 1]
    else:
        return None

    if puzzle[possible[0]][possible[1]] is None:
        return possible
    else:
        return previous_cell(n, d, puzzle, possible)


def next_cell(n, d, puzzle, cell):
    if cell[1] < n - 1:
        possible = [cell[0], cell[1] + 1]
    elif cell[0] < n - 1:
        possible = [cell[0] + 1, 0]
    else:
        return None

    if puzzle[possible[0]][possible[1]] is None:
        return possible
    else:
        return next_cell(n, d, puzzle, possible)


def print_avoiding_sudoku_solutions(n, d, row_pattern, column_pattern, puzzle):
    solution = copy.deepcopy(puzzle)
    cell = [-1, n - 1]
    solutions = []

    while True:
        if valid_sudoku(n, d, row_pattern, column_pattern, solution):
            if next_cell(n, d, puzzle, cell) is None:
                solutions += [copy.deepcopy(solution)]
                print('Found new solution:')
                for row in solution:
                    print(row)
                print('\n')
            else:
                cell = next_cell(n, d, puzzle, cell)
                solution[cell[0]][cell[1]] = 0
                continue
        while True:
            if solution[cell[0]][cell[1]] < n - 1:
                solution[cell[0]][cell[1]] += 1
                break
            else:
                solution[cell[0]][cell[1]] = None
                if previous_cell(n, d, puzzle, cell) is None:
                    print('All solutions found!')
                    for solution in solutions:
                        print('')
                        for row in solution:
                            print(row)
                        print('\n')
                    return
                else:
                    cell = previous_cell(n, d, puzzle, cell)


def main():
    print_avoiding_sudoku_solutions(6, 3, (0, 1, 2, 3), (0, 1, 2, 3),
                                    [[None, None, None, None, None, None],
                                     [None, None, 0, 1, None, None],
                                     [None, 1, None, None, 4, None],
                                     [None, 5, None, None, 1, None],
                                     [None, None, 1, 0, None, None],
                                     [None, None, None, None, None, None]])


if __name__ == '__main__':
    main()
