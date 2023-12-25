import sys
import numpy as np


# PART 1

# your input is world map of '#' and '.' characters.
# '#' is a rock cell, you cannot traverse those. '.' is empty space
# You start from the empty space marked 'S' and can move north, south,
# east or west. How many cells can you reach making exactly 64 steps?


def read_input_into_lines():
    """Read the input file and return it as a list of lines stripped of
       leading or trailing whitespace."""
    with open('../input/21', 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def is_valid_step(world, x, y):
    if x < 0 or y < 0 or x >= len(world[0]) or y >= len(world):
        return False
    return world[y][x] != '#'

def get_valid_steps(world, x, y):
    return [(x,y) for (x,y) in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
            if is_valid_step(world, x, y)]

def get_start(world):
    for y, line in enumerate(world):
        for x, char in enumerate(line):
            if char == 'S':
                return (x,y)
    raise ValueError('No start found')

def traverse_world(world, max_steps, start, steps_f=get_valid_steps):
    """Traverese the world starting from start and return a dict of
       cell:steps pairs for all cells reachable in max_steps steps."""
    frontier = [start]
    visited = {start: 0}
    for i in range(1, max_steps + 1):
        if not frontier:
            break
        new_frontier = []
        for x, y in frontier:
            for step in steps_f(world, x, y):
                if step not in visited:
                    visited[step] = i
                    new_frontier.append(step)
                elif visited[step] > i:
                    visited[step] = i
        frontier = new_frontier
    return visited

def count_reachable_cells(world, max_steps, start, steps_f=get_valid_steps):
    mod = max_steps % 2
    visited = traverse_world(world, max_steps, start, steps_f)
    return sum(1 for x in visited.values() if x % 2 == mod)

CORRECT_ANSWER_1 = 3814
def answer_1():
    world = read_input_into_lines()
    start = get_start(world)
    max_steps = 64
    return count_reachable_cells(world, max_steps, start)

##########################################################################

# PART 2

# Now the map extends infintely in all directions. How many cells can you
# reach making exactly 26501365 steps?

# The task is made easier by the fact that S is in the center of the map and sits
# on an empty row and column. The map is also a square of length 131 so you need
# 65 steps to go from start (center) to a vertical or horizontal edge.
# The max number of steps is 26501365 and 26501365 = 202300 * 131 + 65, so
# imagining no obstacles, you could reach any cell in a diamond shape that extends
# quadraticly from the center. Given f(steps) = count of cells reachable in steps,
# you can calculate f(n * 131 + 65) at n = 0, 1, 2 and then from these three points
# you can calculate the quadratic function that fits them. Then you can calculate
# f(202300 * 131 + 65) to find the answer. Given the particular shape of the map,
# this ideal solution luckily works.

def is_valid_step_infinite(world, x, y):
    n = len(world)
    x = (x % n + n) % n
    y = (y % n + n) % n
    return world[y][x] != '#'

def get_valid_steps_infinite(world, x, y):
    return [(x,y) for (x,y) in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
            if is_valid_step_infinite(world, x, y)]

def find_quadratic(a, b, c):
    """Given three points (x, y) return the coefficients of the quadratic"""
    # Matrix with x values
    X = np.array([[a[0]**2, a[0], 1],
                  [b[0]**2, b[0], 1],
                  [c[0]**2, c[0], 1]])

    # Y values
    Y = np.array([a[1], b[1], c[1]])

    # Solve for a, b, c
    coef = np.linalg.solve(X, Y)
    return coef

def quadratic_value(coef, x):
    """Given coefficients of quadratic and x, return the value of the quadratic"""
    a, b, c = coef
    return a * x**2 + b * x + c

CORRECT_ANSWER_2 = 632257949158206
def answer_2():
    world = read_input_into_lines()
    start = get_start(world)
    max_steps = 26501365
    n = max_steps // len(world)   # 202300
    rest = max_steps % len(world) # 65
    # given f(steps) = count of cells reachable in steps,
    # calculate f(n * 131 + 65) at n = 0, 1, 2
    a = count_reachable_cells(world, 0 * len(world) + rest, start,
                              steps_f=get_valid_steps_infinite)
    b = count_reachable_cells(world, 1 * len(world) + rest, start,
                              steps_f=get_valid_steps_infinite)
    c = count_reachable_cells(world, 2 * len(world) + rest, start,
                              steps_f=get_valid_steps_infinite)
    coef = find_quadratic((0, a), (1, b), (2, c))
    res = quadratic_value(coef, n)
    return int(res)

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
