import math
import itertools
import numpy
import copy


def avoids(permutation, pattern):
    if len(permutation) < len(pattern):
        return True
    elif len(permutation) == len(pattern):
        return tuple(numpy.argsort(permutation)) != pattern
    else:
        return all(avoids(tuple(numpy.argsort(sub)), pattern)
                   for sub in itertools.combinations(permutation, len(pattern)))


def avoids_fixed(permutation, pattern, fixed_index):
    if len(permutation) < len(pattern):
        return True
    elif len(permutation) == len(pattern):
        return tuple(numpy.argsort(permutation)) != pattern
    else:
        return all(tuple(numpy.argsort(prefix + (permutation[fixed_index],) + suffix)) != pattern
                   for prefix_length in range(min(fixed_index + 1, len(pattern)))
                   for prefix in itertools.combinations(permutation[:fixed_index], prefix_length)
                   for suffix in
                   itertools.combinations(permutation[fixed_index + 1:], len(pattern) - prefix_length - 1))


def avoiding_permutations(n, pattern):
    return [permutation for permutation in itertools.permutations(range(n)) if avoids(permutation, pattern)]


def valid_sudoku(n, d, row_pattern, column_pattern, board):
    return valid_rows(n, d, row_pattern, column_pattern, board) \
        and valid_columns(n, d, row_pattern, column_pattern, board) \
        and valid_boxes(n, d, row_pattern, column_pattern, board)


def valid_sudoku_cell(n, d, row_pattern, column_pattern, board, cell):
    return valid_row_fixed(n, d, row_pattern, column_pattern, board, cell) \
        and valid_column_fixed(n, d, row_pattern, column_pattern, board, cell) \
        and valid_box(n, d, row_pattern, column_pattern, board, get_box_index(n, d, cell))


def valid_rows(n, d, row_pattern, column_pattern, board):
    return all(valid_row(n, d, row_pattern, column_pattern, board, i) for i in range(n))


def valid_row(n, d, row_pattern, column_pattern, board, i):
    row = [board[i][j] for j in range(n) if board[i][j] is not None]
    return len(row) == len(set(row)) and avoids(tuple(row), row_pattern)


def valid_row_fixed(n, d, row_pattern, column_pattern, board, cell):
    row = [board[cell[0]][j] for j in range(n) if board[cell[0]][j] is not None]
    return len(row) == len(set(row)) and avoids_fixed(tuple(row), row_pattern, cell[1])


def valid_columns(n, d, row_pattern, column_pattern, board):
    return all(valid_column(n, d, row_pattern, column_pattern, board, j) for j in range(n))


def valid_column(n, d, row_pattern, column_pattern, board, j):
    column = [board[i][j] for i in range(n) if board[i][j] is not None]
    return len(column) == len(set(column)) and avoids(tuple(column), column_pattern)


def valid_column_fixed(n, d, row_pattern, column_pattern, board, cell):
    column = [board[i][cell[1]] for i in range(n) if board[i][cell[1]] is not None]
    return len(column) == len(set(column)) and avoids_fixed(tuple(column), column_pattern, cell[0])


def valid_boxes(n, d, row_pattern, column_pattern, board):
    return all(valid_box(n, d, row_pattern, column_pattern, board, k) for k in range(n))


def valid_box(n, d, row_pattern, column_pattern, board, k):
    box = [board[i][j]
           for j in range((k % math.floor(n / d)) * d, ((k % math.floor(n / d)) + 1) * d)
           for i in range(math.floor(k * d / n) * math.floor(n / d), (math.floor(k * d / n) + 1) * math.floor(n / d))
           if board[i][j] is not None]
    return len(box) == len(set(box))


def get_box_index(n, d, cell):
    return math.floor(cell[0] * d / n) * math.floor(n / d) + math.floor(cell[1] / d)


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


def print_avoiding_sudoku_solutions(n, d, row_pattern, column_pattern, puzzle, start_from=None):
    if start_from:
        solution = start_from
        row_index = max(
            i for i in range(n) if any(solution[i][j] is not None and puzzle[i][j] is None for j in range(n)))
        col_index = max(j for j in range(n) if solution[row_index][j] is not None and puzzle[row_index][j] is None)
        cell = [row_index, col_index]
    else:
        solution = copy.deepcopy(puzzle)

        if not valid_sudoku(n, d, row_pattern, column_pattern, solution):
            print("Invalid starting board!")
            return

        cell = next_cell(n, d, puzzle, [-1, n - 1])
        solution[cell[0]][cell[1]] = 0

    solutions = []

    try:
        while True:
            if valid_sudoku_cell(n, d, row_pattern, column_pattern, solution, cell):
                if next_cell(n, d, puzzle, cell) is None:
                    solutions += [copy.deepcopy(solution)]
                    print('Found new solution:')
                    for row in solution:
                        print(str(row) + ',')
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
                        print(f'All {len(solutions)} solutions found!')
                        for solution in solutions:
                            print('')
                            for row in solution:
                                print(str(row) + ',')
                            print('\n')
                        return
                    else:
                        cell = previous_cell(n, d, puzzle, cell)
    except:
        print('Last checked board:')
        for row in solution:
            print(str(row) + ',')
        print('\n')


def main():
    print_avoiding_sudoku_solutions(6, 3, (0,1,2,3), (0,1,2,3),
                                    [[None,None,None,None,None,5   ],
                                     [None,1   ,None,None,None,None],
                                     [None,None,2   ,None,None,None],
                                     [None,None,None,None,4   ,None],
                                     [0   ,None,None,None,None,None],
                                     [None,None,None,3   ,None,None]])

    # print_avoiding_sudoku_solutions(9, 3, (4,3,2,1,0), (4,3,2,1,0),
    #                                 [[None,None,2   ,0   ,None,5   ,None,6   ,None],
    #                                  [None,5   ,None,None,None,None,None,None,None],
    #                                  [None,None,None,None,None,None,None,None,3   ],
    #                                  [None,None,3    ,4  ,None,8   ,None,None,None],
    #                                  [None,None,None,None,7   ,None,1   ,None,None],
    #                                  [None,0   ,8   ,None,None,None,6   ,None,None],
    #                                  [None,None,None,None,8   ,None,None,1   ,2   ],
    #                                  [4   ,2   ,None,None,None,6   ,None,None,5   ],
    #                                  [8   ,None,None,None,5   ,None,None,None,None]])

    # print_avoiding_sudoku_solutions(9, 3, (0,1,2,3,4), (0,1,2,3,4),
    #                                 [[None,None,6   ,8   ,None,3   ,None,2   ,None],
    #                                  [None,3   ,None,None,None,None,None,None,None],
    #                                  [None,None,None,None,None,None,None,None,5   ],
    #                                  [None,None,5    ,4  ,None,0   ,None,None,None],
    #                                  [None,None,None,None,1   ,None,7   ,None,None],
    #                                  [None,8   ,0   ,None,None,None,2   ,None,None],
    #                                  [None,None,None,None,0   ,None,None,7   ,6   ],
    #                                  [4   ,6   ,None,None,None,2   ,None,None,3   ],
    #                                  [0   ,None,None,None,3   ,None,None,None,None]])

    # print_avoiding_sudoku_solutions(9, 3, (0, 1, 2, 3), (0, 1, 2, 3),
    #                                 [[None, None, None, None, None, None, None, None, None],
    #                                  [None, None, None, None, None, None, None, None, None],
    #                                  [None, None, None, None, None, None, None, None, None],
    #                                  [None, None, None, None, None, None, None, None, None],
    #                                  [None, None, None, None, None, None, None, None, None],
    #                                  [None, None, None, None, None, None, None, None, None],
    #                                  [None, None, None, None, None, None, None, None, None],
    #                                  [None, None, None, None, None, None, None, None, None],
    #                                  [None, None, None, None, None, None, None, None, None]],
    #                                 start_from=[[0, 1, 8, 7, 6, 5, 4, 3, 2],
    #                                             [2, 4, 3, 0, 8, 1, 7, 6, 5],
    #                                             [7, 5, 6, 4, 2, 3, 0, 8, 1],
    #                                             [5, 3, 2, 1, 0, 7, 6, 4, 8],
    #                                             [4, 0, 7, 8, 5, 2, 1, 3, None],
    #                                             [None, None, None, None, None, None, None, None, None],
    #                                             [None, None, None, None, None, None, None, None, None],
    #                                             [None, None, None, None, None, None, None, None, None],
    #                                             [None, None, None, None, None, None, None, None, None]])


if __name__ == '__main__':
    main()
