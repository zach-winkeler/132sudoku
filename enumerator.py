import math
import itertools
import numpy


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


def print_avoiding_sudoku(n, d, row_pattern, column_pattern):
    permutations = avoiding_permutations(n, row_pattern)
    print(f'{len(permutations)} permutations generated!')

    row_indices = [0, 1] + (n - 2) * [None]
    row = 1
    found = []

    while True:
        # print(f"Checking {row_indices}")
        if valid_sudoku(n, d, permutations, row_indices, column_pattern):
            if row == n - 1:
                print('')
                for row_index in row_indices:
                    print(permutations[row_index])
                print('\n')
                found += [(permutations[row_index] for row_index in row_indices)]
            else:
                row += 1
                row_indices[row] = 0
                continue
        while True:
            if row_indices[row] < len(permutations) - 1:
                row_indices[row] += 1
                if row == 0:
                    print('.', end='')
                break
            elif row == 0:
                print('')
                print(f'All {len(found)} sudokus found')
                return
            else:
                row_indices[row] = None
                row -= 1


def valid_sudoku(n, d, permutations, row_indices, column_pattern):
    return valid_columns(n, d, permutations, row_indices, column_pattern) \
        and valid_boxes(n, d, permutations, row_indices)


def valid_columns(n, d, permutations, row_indices, column_pattern):
    return all(valid_column(n, d, permutations, row_indices, column_pattern, j) for j in range(n))


def valid_column(n, d,  permutations, row_indices, column_pattern, j):
    column = [permutations[row_indices[i]][j] for i in range(n) if row_indices[i] is not None]
    return len(column) == len(set(column)) and avoids(tuple(column), column_pattern)


def valid_boxes(n, d, permutations, row_indices):
    return all(valid_box(n, d, permutations, row_indices, k) for k in range(n))


def valid_box(n, d, permutations, row_indices, k):
    box = [permutations[row_indices[i]][j]
           for j in range((k % math.floor(n / d)) * d, ((k % math.floor(n / d)) + 1) * d)
           for i in range(math.floor(k * d / n) * math.floor(n / d), (math.floor(k * d / n) + 1) * math.floor(n / d))
           if row_indices[i] is not None]
    return len(box) == len(set(box))


def main():
    print_avoiding_sudoku(6, 3, (0,2,1,3), (0,2,1,3))


if __name__ == '__main__':
    main()
