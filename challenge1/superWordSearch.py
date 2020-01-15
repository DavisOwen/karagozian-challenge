#!/usr/bin/env python
import sys

"""
Usage:

./superWordSearch.py input_file.txt

where input_file.txt has the example format specified in the instructions
"""


class Coordinates(object):
    """
    Object that keeps track of a given (x, y)
    coordinate and handles the incremental movement
    of the coordinate to the next grid location. Also
    handles whether we are allowed to wrap around the grid
    or not
    """
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1),
            (1, -1), (-1, 1), (-1, -1)]

    def __init__(self, coord, bounds, wrap):
        self.start_coord = coord
        self.coord = coord
        self.dir_idx = -1
        self.wrap = wrap
        self.bounds = bounds

    def next_direction(self):
        self.dir_idx += 1
        self.coord = self.start_coord
        if self.dir_idx >= len(self.dirs):
            return False
        return True

    def increment(self):
        x, y = self.coord
        dx, dy = self.dirs[self.dir_idx]
        n, m = self.bounds
        new_x = x + dx
        new_y = y + dy
        if wrap:
            if new_x > n - 1:
                new_x = 0
            elif new_x < 0:
                new_x = n - 1
            if new_y > m - 1:
                new_y = 0
            elif new_y < 0:
                new_y = m - 1
        elif new_x > n - 1 or new_x < 0 or new_y > m - 1 or new_y < 0:
            return False
        self.coord = (new_x, new_y)
        if self.coord == self.start_coord:
            return False
        return self.coord

    def get_start_coord(self):
        return self.start_coord


def find_end_path(grid, letters, coord):
    """
    Given a string, check if the first letter exists
    in the next coordinate position, then recursively
    check for the rest of the string. Returns the coord
    location of the last letter or False if not found
    """
    letter = letters[0]
    new_coord = coord.increment()
    if new_coord and grid[new_coord[0]][new_coord[1]] == letter:
        if len(letters) <= 1:
            return new_coord
        return find_end_path(grid, letters[1:], coord)
    return False


def find_word(grid, word, letter_map):
    """
    Finds a single word on the grid
    and returns coordinate or 'NOT FOUND'
    """
    first = word[0]
    # find each instance of the first letter
    # in the grid and search through all possible
    # paths to see if the word exists
    # if none of the paths work for the first letter,
    # there is no need to search through the rest of the
    # letteres
    if first in letter_map:
        for coord in letter_map[first]:
            while coord.next_direction():
                end = find_end_path(grid, word[1:], coord)
                if end:
                    return (coord.get_start_coord(), end)
    return 'NOT FOUND'


def find_words(grid, words, wrap):
    """
    Iterates through each word and, if found,
    prints its coordinates or, if not found,
    prints 'NOT FOUND'
    """
    letter_map = {}
    # iterate through grid and store
    # every location of each letter in a
    # hash map
    n = len(grid)
    m = len(grid[0])
    for i in range(n):
        for j in range(m):
            coord = Coordinates((i, j), (n, m), wrap)
            if grid[i][j] not in letter_map:
                letter_map[grid[i][j]] = [coord]
            else:
                letter_map[grid[i][j]].append(coord)
    for word in words:
        print(find_word(grid, word, letter_map))


# read input file
filename = sys.argv[1]
input_file = open(filename, 'r')
n_m = input_file.readline().split()
n = int(n_m[0])
m = int(n_m[1])
grid = []
row = 0
while row < n:
    line = input_file.readline().strip()
    grid.append(line)
    row += 1
wrap_option = input_file.readline().strip()
wrap = False
if wrap_option == "WRAP":
    wrap = True
elif wrap_option == "NO_WRAP":
    wrap = False
else:
    print('Incorrect option given')
    sys.exit(0)
num_words = int(input_file.readline())
words = []
for i in range(num_words):
    word = input_file.readline().strip()
    words.append(word)

# run program
find_words(grid, words, wrap)
