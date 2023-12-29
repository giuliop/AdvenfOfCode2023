import sys
from collections import defaultdict


# PART 1

# Your input is a map with the following tiles:

# .        : path
# #        : forest (cannot be crossed)
# v ^ < >  : slope (must continue in direction of slope)

# You start from the single . tile in the top row and must reach the
# single . tile in the bottom row. Never step on the same tile twice.
# What is the longest path you can take?

def read_input_into_lines():
    """Read the input file and return it as a list of lines stripped of
       leading or trailing whitespace."""
    with open('../input/23', 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def get_start_and_end(world):
    """Return the start and end positions in world."""
    start = [(x, 0) for x in range(len(world[0]))
         if world[0][x] == '.'][0]
    end = [(x, len(world) - 1) for x in range(len(world[-1]))
              if world[len(world) - 1][x] == '.'][0]
    return start, end

def is_valid_tile(world, to_pos):
    """Return True if to_pos is a valid step from from_pos in world."""
    x, y = to_pos
    return (0 <= x < len(world[0]) and
            0 <= y < len(world) and
            world[y][x] != '#')

def find_next_steps(world, from_pos):
    """Return a list of all valid neighbours of position in world."""
    x, y = from_pos
    if world[y][x] == '>':
        return [(x + 1, y)]
    if world[y][x] == '<':
        return [(x - 1, y)]
    if world[y][x] == '^':
        return [(x, y - 1)]
    if world[y][x] == 'v':
        return [(x, y + 1)]
    neighbours = [(x + step_x, y + step_y)
                  for step_x, step_y in
                  [(0, 1), (0, -1), (1, 0), (-1, 0)]]
    return [to for to in neighbours if is_valid_tile(world, to)]

class Path:
    """A path has a route (a list of positions) which cannot be empty.
       The last position in the route is the current position.
       It keep track of the visited positions in a set for efficient
       checking"""
    def __init__(self, route):
        self.route = route
        self.visited = set(route)

    def add(self, to):
        self.route.append(to)
        self.visited.add(to)

    def __contains__(self, pos):
        return pos in self.visited

    def clone(self):
        return Path(self.route.copy())

    def current_pos(self):
        return self.route[-1]

    def __len__(self):
        return len(self.route) - 1

    def __repr__(self):
        return f'Path({self.route})'

def find_longest_path(world, start, end):
    """Find the longest path from start to end in world without stepping
       on a tile twice. Return the length of the path."""
    path = Path([start])
    frontier = [path]
    longest_path = path

    while frontier:
        path = frontier.pop()
        if path.current_pos() == end:
            if len(path) > len(longest_path):
                longest_path = path
            continue
        for to in find_next_steps(world, path.current_pos()):
            if to not in path:
                new_path = path.clone()
                new_path.add(to)
                frontier.append(new_path)

    return len(longest_path)

CORRECT_ANSWER_1 = 2186
def answer_1():
    world = read_input_into_lines()
    start, end = get_start_and_end(world)
    return find_longest_path(world, start, end)

##########################################################################

# PART 2

# Now treat all slopes as paths. What is the longest path you can take?

# We will first traverse the world to represent it as a graph with
# vertexes as tiles with multiple paths and edges as the steps between
# them. We will then run the general longest path algorithm.

def find_neighbours(tiles, from_pos):
    """Return a list of all valid neighbours of position in world."""
    x, y = from_pos
    neighbours = [(x + step_x, y + step_y)
                  for step_x, step_y in
                  [(0, 1), (0, -1), (1, 0), (-1, 0)]]
    return [to for to in neighbours if is_valid_tile(tiles, to)]

def get_world_as_graph(tiles, start):
    """Return the world as a tuple (vertexes, edges) where the vertexes
       are start, end, and the tiles with multiple paths around them.
       The edges are a dict of vertex -> list of (vertex, steps)."""
    edges = defaultdict(set)

    frontier = [(start, start)]
    visited = set()
    vertexes = set([start])

    while frontier:
        coming_from, pos = frontier.pop()
        steps = 0 if coming_from == pos else 1
        last_pos = coming_from
        while True:
            if pos in visited:
                break
            visited.add(pos)
            next_steps = [to for to in find_neighbours(tiles, pos)
                          if (to in vertexes and to != last_pos) or to not in visited]
            if len(next_steps) == 1:
                last_pos = pos
                pos = next_steps[0]
                steps += 1
                if pos in vertexes:
                    edges[pos].add((coming_from, steps))
                    edges[coming_from].add((pos, steps))
                    break
            else:
                vertexes.add(pos)
                edges[pos].add((coming_from, steps))
                edges[coming_from].add((pos, steps))
                for to in next_steps:
                    if to not in vertexes:
                        frontier.append((pos, to))
                break

    return edges

class GraphPath:
    """A path has a route (a list of vertexes) which cannot be empty.
       The last position in the route is the current vertex.
       The length of the path is the sum of the weights of the edges
       implicitly defined by the order of the route."""

    def __init__(self, route, steps = 0):
        self.route = route
        self.visited = set(route)
        self.steps = steps

    def add(self, to, steps):
        self.route.append(to)
        self.visited.add(to)
        self.steps += steps

    def __contains__(self, vertex):
        return vertex in self.visited

    def clone(self):
        return GraphPath(self.route.copy(), self.steps)

    def current_vertex(self):
        return self.route[-1]

    def __len__(self):
        return self.steps

    def __repr__(self):
        return f'CondensedPath({self.route})'

def find_longest_path_on_graph(edges, start, end):
    """Find the longest path from start to end in the edges without
       stepping on a tile twice. Return the length of the path."""
    path = GraphPath([start])
    frontier = [path]
    longest_path = path

    while frontier:
        path = frontier.pop()
        if path.current_vertex() == end:
            if len(path) > len(longest_path):
                longest_path = path
            continue
        for to, steps in edges[path.current_vertex()]:
            if to not in path:
                new_path = path.clone()
                new_path.add(to, steps)
                frontier.append(new_path)

    return len(longest_path)

def print_graph(edges):
    """Print the world as a graph."""
    vertexes = list(edges.keys())
    vertexes.sort()
    for v in vertexes:
        print(v, ':', edges[v])

CORRECT_ANSWER_2 = 6802
def answer_2():
    tiles = read_input_into_lines()
    start, end = get_start_and_end(tiles)
    world = get_world_as_graph(tiles, start)
    return find_longest_path_on_graph(world, start, end)

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
