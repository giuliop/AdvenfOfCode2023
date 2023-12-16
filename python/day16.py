import sys


# PART 1

# Yuor input shows a world map like this:

# |...\....
# |.-.\.....
# .....|-...
# ........|.
# ..........
# .........\

# A beam of light starts at the top left corner travelling right.
# It moves across the map accourding to the following rules:
#
# .     : continues in the same direction
#
# \ , / : turns 90 degrees according to its direction and the inclination of the symbol
#         (e.g., rightward-moving beam and / mirror: continue upward in the mirror's column,
#          rightward-moving beam and \ mirror: continue downward from the mirror's column)
#
# - , | : if beam same direction, continues, otherwise splits in two beans in the directions
#         of the symbols
#

# Let the beam propagate and then count the number of cells traversed by it.

def read_input_into_lines():
    """Read the input file and return it as a list of lines stripped of
       leading or trailing whitespace."""
    with open('../input/16', 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

class World:
    def __init__(self, grid):
        self.grid = grid
        self.x_len = len(grid[0])
        self.y_len = len(grid)

    def get_type(self, pos):
        x, y = pos
        return self.grid[y][x]

    def valid_pos(self, pos):
        x, y = pos
        return 0 <= x < self.x_len and 0 <= y < self.y_len

def build_world_from_input():
    lines = read_input_into_lines()
    return World(lines)

def next_steps(pos, dirs, w):
    """Return a list of tuple with the next cell and direction of the beam
       given the current cell, direction and grid."""
    x, y = pos
    cell_type = w.get_type(pos)

    steps = []

    if ( cell_type == '.' or
        (cell_type == '-' and (dirs in {(1, 0), (-1, 0)} )) or
        (cell_type == '|' and (dirs in {(0, 1), (0, -1)}))
    ):
        steps.append( ((x + dirs[0], y + dirs[1]), dirs) )

    elif cell_type == '\\':
        steps.append( ((x + dirs[1], y + dirs[0]), (dirs[1], dirs[0])) )

    elif cell_type == '/':
        steps.append( ((x - dirs[1], y - dirs[0]), (-dirs[1], -dirs[0])) )

    elif cell_type == '-':
        steps.append( ((x + 1, y), (1, 0)) )
        steps.append( ((x - 1, y), (-1, 0)) )

    elif cell_type == '|':
        steps.append( ((x, y + 1), (0, 1)) )
        steps.append( ((x, y - 1), (0, -1)) )

    return [(pos, dir) for pos, dir in steps if w.valid_pos(pos)]


def count_activated(w, start_step):
    """Traverse the world w and starting the beam from start_step and return the
       number of cells activated by the beam."""
    start, dirs = start_step
    frontier = [(start, dirs)]
    traversed = set()  # set of (cell, dir) tuples

    while frontier:
        pos, dirs = frontier.pop()
        traversed.add((pos, dirs))
        steps = next_steps(pos, dirs, w)
        for step in steps:
            if step not in traversed:
                frontier.append(step)

    return len({pos for pos, _ in traversed})

CORRECT_ANSWER_1 = 8901
def answer_1():
    w = build_world_from_input()
    start_step=((0, 0), (1, 0))
    return count_activated(w, start_step)

##########################################################################

# PART 2

# Now you can start the beam from any cell of the border going in the opposite
# direction of the border. If starting from a corner, you can choose either of the
# two possible directions.

# Find the maximum number of cells traversed by the beam when starting from any
# cell of the border.

CORRECT_ANSWER_2 = 9064
def answer_2():
    w = build_world_from_input()
    start_steps = []
    for x in range(w.x_len):
        start_steps.append(((x, 0), (0, 1)))
        start_steps.append(((x, w.y_len - 1), (0, -1)))
    for y in range(w.y_len):
        start_steps.append(((0, y), (1, 0)))
        start_steps.append(((w.x_len - 1, y), (-1, 0)))

    # find the maximum number of traversed cells
    return max(count_activated(w, step) for step in start_steps)


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
