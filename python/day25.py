import sys
import copy
import random
from collections import defaultdict


# PART 1

# Your input is a list of lines like this:

# jqt: rhn xhk nvd

# The 'words' represent parts of a machine.
# Each line has a part, followed by a colon, followed by a list of
# other parts connected to it by a wire.
# Find the three wires you need to disconnect to partition all parts in
# two separate, disconnected groups.
# Multiply the size of these two groups to get the answer.

def read_input_into_lines():
    """Read the input file and return it as a list of lines stripped of
       leading or trailing whitespace."""
    with open('../input/25', 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def parse_line(line):
    """Parse a line into a part and a list of connected parts."""
    part, connected_parts = line.split(': ')
    return part, connected_parts.split(' ')

def build_graph(lines):
    """Build a graph from the input lines as a dict of
       vertex -> set of connected vertexes."""
    graph = {}
    for line in lines:
        part, connected_parts = parse_line(line)
        graph[part] = connected_parts
    for line in lines:
        part, connected_parts = parse_line(line)
        for connected_part in connected_parts:
            if connected_part not in graph:
                graph[connected_part] = []
            if part not in graph[connected_part]:
                graph[connected_part].append(part)
    return graph

def contract(graph, u, v):
    """Merge the nodes u and v into a single node and remove self-loops"""
    for node in graph[v]:
        if node != u:
            graph[u].append(node)
            graph[node].append(u)
        graph[node].remove(v)
    graph[u] = [node for node in graph[u] if node != u]
    del graph[v]

def kargers_algorithm(graph):
    """Return a tuple of three elements:
       1. the cut (count of edges between the two groups)
       2. the number of vertices in the first group
       3. the number of vertices in the second group"""
    local_graph = copy.deepcopy(graph)
    vertices = list(local_graph.keys())
    vertices_count = {vertex: 1 for vertex in vertices}

    while len(vertices) > 2:
        u = random.choice(vertices)
        v = random.choice(local_graph[u])
        contract(local_graph, u, v)
        vertices = list(local_graph.keys())
        vertices_count[u] += vertices_count[v]

    remaining_vertices = list(local_graph.keys())
    return (len(local_graph[remaining_vertices[0]]),
            vertices_count[remaining_vertices[0]],
            vertices_count[remaining_vertices[1]])

CORRECT_ANSWER_1 = 592171
def answer_1():
    graph = build_graph(read_input_into_lines())
    while True:
        cut, group1, group2 = kargers_algorithm(graph)
        if cut == 3:
            return group1 * group2

##########################################################################

# PART 2

# No part 2 for day 25, this is the last day of the Advent of Code 2023!

CORRECT_ANSWER_2 = None
def answer_2():
    print('No part 2 for day 25, this is the last day of the Advent of Code 2023!')

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
