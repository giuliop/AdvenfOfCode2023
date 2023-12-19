import sys
from collections import defaultdict


# PART 1

# Your input is a list of lines like these:

# R 6 (#70c710)
# D 5 (#0dc571)

# Each line is a command to dig a trench of a certain length in a certain
# direction, and to fill it with a certain color. The colors are given as
# hexadecimal RGB values. The directions are given as one of the four
# cardinal directions, R(ight), L(eft), U(p), or D(own).

# Dig the trenches and then dig the interior of the border marked by the
# trenched. Each trench or interior "cell" is one cubic meter.
# Sum the total cubic meters.

def read_input_into_lines():
    """Read the input file and return it as a list of lines stripped of
       leading or trailing whitespace."""
    with open('../input/18', 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]


def move(pos, direction, length):
    """Return the coordinates of the end of a trench of the given length
       starting from the given position in the given direction."""
    x, y = pos
    if direction == 'R':
        return (x + length, y)
    if direction == 'L':
        return (x - length, y)
    if direction == 'U':
        return (x, y - length)
    if direction == 'D':
        return (x, y + length)
    raise ValueError(f'Unknown direction: {direction}')

def dig_border(commands):
    """Take a list of (direction, length) tuples to dig the trenches and return
       the border as a set of (x,y) with (0,0) starting point, +x to the right,
       +y down"""
    border = set()
    current_pos = (0, 0)
    border.add(current_pos)
    for cmd in commands:
        direction, length = cmd
        for _ in range(int(length)):
            next_pos = move(current_pos, direction, 1)
            border.add(next_pos)
            current_pos = next_pos
    return border

outside = set()
def flood_fill(x, y, min_x, max_x, min_y, max_y, border):
    """Mark cells outside the border and return a set of external cells"""
    if x < min_x or x > max_x or y < min_y or y > max_y:
        return
    if (x, y) in border:
        return
    if (x, y) in outside:
        return
    outside.add((x, y))
    frontier = set()
    frontier.add((x, y))
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while frontier:
        x, y = frontier.pop()
        for dx, dy in directions:
            if (x + dx, y + dy) in border:
                continue
            if (x + dx, y + dy) in outside:
                continue
            if x + dx < min_x or x + dx > max_x or y + dy < min_y or y + dy > max_y:
                continue
            outside.add((x + dx, y + dy))
            frontier.add((x + dx, y + dy))

def mark_outside_cells(border, min_x, max_x, min_y, max_y):
    """Return the set of external cells"""
    for x in range(min_x, max_x + 1):
        flood_fill(x, min_y, min_x, max_x, min_y, max_y, border)
        flood_fill(x, max_y, min_x, max_x, min_y, max_y, border)
    for y in range(min_y, max_y + 1):
        flood_fill(min_x, y, min_x, max_x, min_y, max_y, border)
        flood_fill(max_x, y, min_x, max_x, min_y, max_y, border)
    return outside

CORRECT_ANSWER_1 = 41019
def answer_1():
    commands = [(cmd[0], cmd[1]) for cmd in
                (cmd.split() for cmd in read_input_into_lines())]
    border = dig_border(commands)
    min_x = min(pos[0] for pos in border)
    max_x = max(pos[0] for pos in border)
    min_y = min(pos[1] for pos in border)
    max_y = max(pos[1] for pos in border)
    external = mark_outside_cells(border, min_x, max_x, min_y, max_y)
    len_internal = (max_x - min_x + 1) * (max_y - min_y + 1) - len(border) - len(external)
    return len(border) + len_internal


##########################################################################

# PART 2

# Now consider only the hexadecimal part of the input which is not a color
# but actually encodes the instrucions. The first 5 hex digits are the distance
# to dig the trench, the last hex digit is the direction:
# 0 : R, 1 : D, 2 : L, 3 : U
# e.g., #70c710 = R 461937

def parse_hex(command):
    """Return the direction and length encoded in the given command string"""
    hex_str = command.split()[-1][2:-1]
    direction = hex_str[-1]
    if direction == '0':
        direction = 'R'
    elif direction == '1':
        direction = 'D'
    elif direction == '2':
        direction = 'L'
    elif direction == '3':
        direction = 'U'

    length = int(hex_str[:-1], 16)
    return direction, length

def mark_border(commands):
    """Take a list of (direction, length) tuples to dig the trenches and return
       a tuple of:
       1) the length of the border
       2) a list of border vertices as (start, end) tuples."""
    start = (0, 0)
    border_length = 0
    vertices = [start]
    for cmd in commands:
        direction, move_length = cmd
        border_length += move_length
        end = move(start, direction, move_length)
        vertices.append(end)
        start = end
    return border_length, vertices

def calculate_area(vertices):
    """Take a list of (x, y) vertices of a polygon and return its area"""
    return 0.5 * abs(sum(x1 * y2 - x2 * y1 for ((x1, y1), (x2, y2)) in
                        zip(vertices, vertices[1:] + vertices[:1])))

CORRECT_ANSWER_2 = 96116995735219
def answer_2():
    # We will use the shoelace formula to calculate the area of the polygon
    # defined by the border segments and Pick's theorem to calculate the
    # number of internal cells.

    # Shoelace formula to calculate area of polgon defined by sequce of points:
    # A = 1/2 * abs(sum(x_i * y_i+1 - x_i+1 * y_i))

    # Pick's theorem that relates area A, number of internal cells I and number of
    # points on the border B: A = I + B/2 - 1

    commands = [parse_hex(cmd) for cmd in read_input_into_lines()]
    border_len, border_vertices = mark_border(commands)
    area = calculate_area(border_vertices)
    internal = area - border_len / 2 + 1
    return int(border_len + internal)

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
