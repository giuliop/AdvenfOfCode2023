import sys
from collections import defaultdict

# PART 1

# Your puzzle input ia a list of lines like this:

# 1,0,1~1,2,1

# Each line is a pair of x,y,z coordinates, separated by a tilde, representing
# the two ends of a brick made of cubes.
# First, let bricks "fall" down, until they reach z=1 (z=0 is the floor) or are
# supported by another brick. Then count the bricks that could be removed without
# any bricks falling further down.

def segments_intersect(s1, s2):
    """Return True if line segments 's1' and 's2' intersect"""

    def orientation(p, q, r):
        """Calculate the orientation of ordered triplet (p, q, r).
        Returns 0 if collinear, 1 if clockwise, 2 if counterclockwise."""
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # Collinear
        return 1 if val > 0 else 2  # Clock or counterclock

    def on_segment(p, q, r):
        """Check if point q lies on line segment 'pr'"""
        if (min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and
            min(p[1], r[1]) <= q[1] <= max(p[1], r[1])):
            return True
        return False

    p1, q1 = s1
    p2, q2 = s2

    # Four orientations needed for general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if o1 != o2 and o3 != o4:
        return True

    # Special Cases
    # p1, q1, and p2 are collinear and p2 lies on segment p1q1
    if o1 == 0 and on_segment(p1, p2, q1):
        return True
    # p1, q1 and p2 are collinear and q2 lies on segment p1q1
    if o2 == 0 and on_segment(p1, q2, q1):
        return True
    # p2, q2 and p1 are collinear and p1 lies on segment p2q2
    if o3 == 0 and on_segment(p2, p1, q2):
        return True
    # p2, q2 and q1 are collinear and q1 lies on segment p2q2
    if o4 == 0 and on_segment(p2, q1, q2):
        return True

    return False  # Doesn't fall in any of the above cases

class Cube:
    def __init__(self, coord):
        x,y,z  = [int(c) for c in coord]
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f'({self.x},{self.y},{self.z})'

class Brick:
    def __init__(self, c1, c2) -> None:
        """c1 and c2 are the two ends of the brick"""
        lowend, highend = sorted([c1, c2], key=lambda cube: cube.z)
        self.lowend = lowend
        self.highend = highend

    def __repr__(self) -> str:
        return f'({self.lowend}, {self.highend})'

    @classmethod
    def from_line(cls, line):
        """Parse a line into a brick (a pair of coordinates)"""
        left, right = line.split('~')
        lowend = Cube(int(x) for x in left.split(','))
        highend = Cube(int(x) for x in right.split(','))
        return cls(lowend, highend)

    def supports(self, other):
        """Return True if this brick supports the other brick"""
        if self.highend.z != other.lowend.z - 1:
            return False
        return segments_intersect(((self.lowend.x, self.lowend.y),
                                      (self.highend.x, self.highend.y)),
                                     ((other.lowend.x, other.lowend.y),
                                      (other.highend.x, other.highend.y)))

def read_input_into_lines():
    """Read the input file and return it as a list of lines stripped of
       leading or trailing whitespace."""
    with open('../input/22', 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def get_bricks_by_highest_z():
    """Return a dict z: list of bricks with highest z-coordinate z"""
    bricks = defaultdict(list)
    for line in read_input_into_lines():
        brick = Brick.from_line(line)
        bricks[brick.highend.z].append(brick)
    return bricks

def let_fall(bricks):
    """Let bricks fall down until reaching z=1 or suppor by another brick,
       and return the count of fallen blocks.
       The function modifies the bricks dict."""
    fallen = set()
    brick_list = []
    for brick_sublist in bricks.values():
        brick_list.extend(brick_sublist)
    # order brick_list by lowest z-coordinate, that is by brick.lowend.z
    brick_list.sort(key=lambda brick: brick.lowend.z)
    for b in brick_list:
        for z in range(b.lowend.z-1, 0, -1):
            if any(below_brick.supports(b) for below_brick in bricks[z]):
                break
            bricks[b.highend.z].remove(b)
            b.lowend.z -= 1
            b.highend.z -= 1
            bricks[b.highend.z].append(b)
            fallen.add(b)
    return len(fallen)

def get_supported_bricks(bricks, brick):
    """Return the bricks that are supported by brick"""
    max_z = max(bricks.keys())
    return [b for z in range(brick.highend.z + 1, max_z + 1)
              for b in bricks[z]
            if b.lowend.z == brick.highend.z+1 and brick.supports(b)]

def get_removable(bricks):
    """Count the bricks that could be removed without any bricks falling further down"""
    removable = set()
    for z in bricks.keys():
        for brick in bricks[z]:
            supported_bricks = get_supported_bricks(bricks, brick)
            # we need the brick to not support any brick above it or to have
            # another brick supporting that brick above
            if (not supported_bricks or
                all(any(another_brick.supports(b)
                        for another_brick in bricks[z] if another_brick != brick)
                    for b in supported_bricks)):
                removable.add(brick)
    return removable

CORRECT_ANSWER_1 = 401
def answer_1():
    bricks = get_bricks_by_highest_z()
    let_fall(bricks)
    return len(get_removable(bricks))

##########################################################################

# PART 2

# Now, for each brick, determine how many other bricks would fall if that
# brick were removed and sum those numbers.

def count_falling(supporting, supported_by, removed_brick):
    """Count the bricks that would fall removing brick"""
    fallen = {removed_brick}
    to_process = {removed_brick}
    while to_process:
        b = to_process.pop()
        for supported_brick in supporting[b] if b in supporting else []:
            if all(b in fallen for b in supported_by[supported_brick]):
                fallen.add(supported_brick)
                to_process.add(supported_brick)
    return len(fallen) - 1

CORRECT_ANSWER_2 = 63491
def answer_2():
    bricks = get_bricks_by_highest_z()
    let_fall(bricks)

    supporting = {}
    for z in bricks.keys():
        for brick in bricks[z]:
            supported = get_supported_bricks(bricks, brick)
            if supported:
                supporting[brick] = get_supported_bricks(bricks, brick)

    supported_by = {}
    for brick in supporting:
        for supported_brick in supporting[brick]:
            supported_by.setdefault(supported_brick, []).append(brick)

    return sum(count_falling(supporting, supported_by, removed_brick)
               for z in bricks.keys() for removed_brick in bricks[z])

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
