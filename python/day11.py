import sys
import itertools


# PART 1
# Your input is like this:

# ...#......
# .......#..
# ..........
# ...

# First for any column with no #s, add another empty column to the right,
# for any row with no #s, add another empty row below it.
# Then calculate the steps that separates any pair of #s moving only
# horizontally or vertically.
# Finally sum all the steps.

def read_input_into_lines():
    with open('../input/11', 'r', encoding='utf-8') as file:
        return file.readlines()

class World:
    def __init__(self, lines):
        self.grid = set()
        for y, line in enumerate(lines):
            line = line.strip()
            for x, c in enumerate(line):
                if c == '#':
                    self.grid.add((x,y))
        self.x_len = len(lines[0])
        self.y_len = len(lines)

def world():
    return World(read_input_into_lines())

def is_line_empty(w, y):
    for x in range(w.x_len):
        if (x,y) in w.grid:
            return False
    return True

def is_column_empty(w, x):
    for y in range(w.y_len):
        if (x,y) in w.grid:
            return False
    return True

def expand_world(w, expansion_factor=2):
    expansion_factor -= 1
    empty_lines = []
    empty_columns = []
    for y in range(w.y_len-1, -1, -1):
        if is_line_empty(w, y):
            empty_lines.append(y)
    for x in range(w.x_len-1, -1, -1):
        if is_column_empty(w, x):
            empty_columns.append(x)

    # sorted by x, then y
    points = sorted(w.grid, key=lambda p: (p[0], p[1]))
    # print without newline at the end
    for i, (x,y) in enumerate(points):
        for yy in empty_lines:
            if y > yy:
                points[i] = (points[i][0],points[i][1]+expansion_factor)
        for xx in empty_columns:
            if x > xx:
                points[i] = (points[i][0]+expansion_factor,points[i][1])
    w.grid = set(points)

def distance(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

CORRECT_ANSWER_1 = 9918828
def answer_1():
    w = world()
    expand_world(w)
    total = 0
    # list all unordered pairs of points
    for p1,p2 in (itertools.combinations(w.grid, 2)):
        total += distance(p1, p2)
    return total

##########################################################################

# PART 2

# Now instead of expanding from 1 to 2 lines or columns, expand from 1 to 1000000

CORRECT_ANSWER_2 = 692506533832
def answer_2():
    w = world()
    expand_world(w, 1000000)
    total = 0
    # list all unordered pairs of points
    for p1,p2 in (itertools.combinations(w.grid, 2)):
        total += distance(p1, p2)
    return total

##########################################################################

def print_and_test(func, correct_answer=None):
    answer = func()
    if correct_answer:
        assert answer == correct_answer
    print(answer)

if __name__ == "__main__":
    # if no argument, run all answers, otherwise only part 1 or 2
    if len(sys.argv) == 1 or sys.argv[1] == '1':
        print_and_test(answer_1, CORRECT_ANSWER_1)
    if len(sys.argv) == 1 or sys.argv[1] == '2':
        print_and_test(answer_2, CORRECT_ANSWER_2)
    if len(sys.argv) > 1 and sys.argv[1] not in ['1', '2']:
        print('Give 1 or 2 as argument, or no argument at all')
