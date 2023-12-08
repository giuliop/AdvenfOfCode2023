import sys
import math
from collections import defaultdict
from functools import reduce

# PART 1

# Your input has this format:
# LLR

# AAA = (BBB, BBB)
# BBB = (AAA, ZZZ)
# ZZZ = (ZZZ, ZZZ)

# The first line is a series of left, right instructions
# The other lines represent a starting node and the nodes you reach
# be going left or right from that node

# Count how many steps you take to go from AAA to ZZZ following the instructions.
# The instructions repeat indefintely until you reach ZZZ.

def read_input():
    with open('../input/8', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    instructions = lines[0].strip()
    nodes = lines[2:]
    nodes = {key: value for key, value in (parse_node(node) for node in nodes)}
    return instructions, nodes

def parse_node(node_string):
    """Parse a string `AAA = (BBB, BBB)` into a a tuple AAA, (BBB, BBB)"""
    key = node_string[:3]
    left = node_string[7:10]
    right = node_string[12:15]
    return key, (left, right)

CORRECT_ANSWER_1 = 11911
def answer_1():
    instructions, nodes = read_input()
    next_node = 'AAA'
    count_steps = 0
    while True:
        instruction = instructions[count_steps % len(instructions)]
        if instruction == 'L':
            next_node = nodes[next_node][0]
        else:
            next_node = nodes[next_node][1]
        if next_node == 'ZZZ':
            return count_steps + 1
        count_steps += 1

##########################################################################

# PART 2

# Now you need to simultaneously start from all nodes ending in 'A' and
# continue until all paths reach nodes ending in 'Z'. Count how many steps
# you need to take to reach this state.

def is_end_node(node):
    return node[-1] == 'Z'

def is_start_node(node):
    return node[-1] == 'A'

class Cycle:
    def __init__(self):
        self.steps_to_cycle = None      # steps to start the cycle
        self.steps_to_end_node = []     # steps to reach an end node
        self.length = None              # length of the cycle

def cycle(start_node, instructions, nodes):
    """Detect a cycle and return it"""

    c = Cycle()
    count_steps = 0
    next_node = start_node
    visited_configurations = defaultdict(list)

    while True:
        instruction = instructions[count_steps % len(instructions)]
        next_configuration = (next_node, instruction)

        # we have a cycle if we have visited this configuration before
        # and the number of steps since we last visited it is a multiple
        # of the number of instructions
        for steps in visited_configurations[next_configuration]:
            if (count_steps - steps) % len(instructions) == 0:
                c.length = count_steps - steps
                c.steps_to_cycle = count_steps - c.length
                return c

        visited_configurations[next_configuration].append(count_steps)

        if instruction == 'L':
            next_node = nodes[next_node][0]
        else:
            next_node = nodes[next_node][1]
        if is_end_node(next_node):
            c.steps_to_end_node.append(count_steps + 1)

        count_steps += 1

def lcm(a, b):
    """Return the least common multiple of a and b"""
    return abs(a * b) // math.gcd(a, b)

def lcm_of_list(numbers):
    """Return the least common multiple of a list of numbers"""
    return reduce(lcm, numbers)

def minimum_steps(cycles):
    """Return the minimum number of steps to reach an end node for all cycles"""
    # This is a simplification of the Chinese remainder theorem which
    # would be the general solution to this problem.
    # The gods of the Advent put us in the simplied case :)
    if all(c.steps_to_end_node[0] == c.length for c in cycles):
        return lcm_of_list([c.steps_to_end_node[0] for c in cycles])

    # Implement the general solution
    # https://en.wikipedia.org/wiki/Chinese_remainder_theorem
    raise NotImplementedError

CORRECT_ANSWER_2 = 10151663816849
def answer_2():
    instructions, nodes = read_input()
    start_nodes = [node for node in nodes if is_start_node(node)]
    cycles = [cycle(node, instructions, nodes) for node in start_nodes]
    return minimum_steps(cycles)

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
