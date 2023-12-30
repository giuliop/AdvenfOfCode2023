import sys
from sympy import symbols, Eq, solve

# PART 1

# You input is a list of lines like this:

# 19, 13, 30 @ -2,  1, -2

# Each line represens a hailstone, the first three numbers are the
# x, y, z coordinates of the hailstone, and the last three numbers
# are the velocity in each direction.

# Determine how many intersection of haistones path will occur in the
# future in a test area of x and y positions from 200000000000000 and
# 400000000000000 included. Ignore the z axis.

def line_intersection(p1, p2, p3, p4):
    """Calculate the intersection point of two lines, each defined by two points
       (p1, p2) and (p3, p4) respectively. Each point is a tuple (x,y).
       Return the intersection point (or null if the lines are either parallel
       or coincident, and a message among: 'coincident', 'parallel', 'intersect'."""
    # Calculate slopes
    dx1 = p2[0] - p1[0]
    dy1 = p2[1] - p1[1]
    dx2 = p4[0] - p3[0]
    dy2 = p4[1] - p3[1]

    # Check if lines are parallel (including possibility of being the same line)
    if dx1 * dy2 == dy1 * dx2:
        # Check if they are the same line (coincident)
        A1, B1, C1 = dy1, -dx1, dx1*p1[1] - dy1*p1[0]
        A2, B2, C2 = dy2, -dx2, dx2*p3[1] - dy2*p3[0]
        if A1*C2 == A2*C1 and B1*C2 == B2*C1:
            return None, 'coincident'
        return None, 'parallel'

    # Calculate the intersection point
    d = dx1 * dy2 - dy1 * dx2
    x = ((p2[0]*p1[1] - p1[0]*p2[1])*dx2 - dx1*(p4[0]*p3[1] - p3[0]*p4[1])) / d
    y = ((p2[0]*p1[1] - p1[0]*p2[1])*dy2 - dy1*(p4[0]*p3[1] - p3[0]*p4[1])) / d
    return (x, y), 'intersect'

class Hailstone:
    def __init__(self, x, y, z, vx, vy, vz):
        self.x, self.y, self.z = x, y, z
        self.vx, self.vy, self.vz = vx, vy, vz

    def __repr__(self):
        return f'Hailstone({self.x}, {self.y}, {self.z}, {self.vx}, {self.vy}, {self.vz})'

    def position(self):
        return (self.x, self.y, self.z)

    def velocity(self):
        return (self.vx, self.vy, self.vz)

    @classmethod
    def from_line(cls, line):
        pos, vel = line.split('@')
        x, y, z = [int(n) for n in pos.strip().split(', ')]
        vx, vy, vz = [int(n) for n in vel.strip().split(', ')]
        return cls(x, y, z, vx, vy, vz)

    def line(self):
        """Return the line that the hailstone will follow, as a tuple of two points"""
        return (self.x, self.y), (self.x + self.vx, self.y + self.vy)

def read_input_into_lines():
    """Read the input file and return it as a list of lines stripped of
       leading or trailing whitespace."""
    with open('../input/24', 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def valid_point(x, y, stone):
    """Return true if the point (x, y) is in the future of the stone.
       Assume the x,y lies in the line of the stone."""
    return (x - stone.x) * stone.vx >= 0 and (y - stone.y) * stone.vy >= 0

def valid_intersection(intersection, stone_1, stone_2,
                       min_xy=200000000000000, max_xy=400000000000000):
    """Return true if the intersection point is in the future of both stones.
       Assume the intersection lies in the line of both stones.
       min_xy and max_xy are the limits of the test area."""
    x, y = intersection
    if x < min_xy or x > max_xy or y < min_xy or y > max_xy:
        return False
    return valid_point(x, y, stone_1) and valid_point(x, y, stone_2)

def will_collide(stone_1, stone_2):
    """Return true if the two stones will collide in the future."""
    intersection, status = line_intersection(*stone_1.line(), *stone_2.line())
    if status == 'parallel':
        return False
    if status == 'intersect':
        return valid_intersection(intersection, stone_1, stone_2)
    if status == 'coincident':
        True

CORRECT_ANSWER_1 = 20963
def answer_1():
    stones = [Hailstone.from_line(line) for line in read_input_into_lines()]
    collisions = 0
    for i, stone_1 in enumerate(stones):
        for stone_2 in stones[i+1:]:
            if will_collide(stone_1, stone_2):
                collisions += 1
    return collisions

##########################################################################

# PART 2

# Now consider the z axis as well. You need to create another stone with
# coordinates and velocities of your choice, so that it will hit in its
# path all the other stones. Collisions do not affect the velocity or
# position of the stones.
# Return the sum of the x, y and z coordinates of starting position of
# the stone.

# To determine position and velocity of the new stone we need to find 6
# unknowns (x, y, z, vx, vy, vz).
# To make the stone hit another stone, we need to find a solution to the
# following system of equations:
# x1 + vx1 * t = x2 + vx2 * t
# y1 + vy1 * t = y2 + vy2 * t
# z1 + vz1 * t = z2 + vz2 * t
# where t is the time at which the stones collide.
# These are 3 equations with 7 unknowns, the six unknowns of the new stone
# plus t. By adding a similar system for another point, we add three more
# equations and one unknown (the new t).
# So with three points we can have a system of 9 equations and 9 unknowns,
# and find a solution for the new stone.


CORRECT_ANSWER_2 = 999782576459892
def answer_2():
    stones = [Hailstone.from_line(line) for line in read_input_into_lines()]
    stone_1, stone_2, stone_3 = stones[0], stones[1], stones[2]
    x1, y1, z1 = stone_1.position()
    vx1, vy1, vz1 = stone_1.velocity()
    x2, y2, z2 = stone_2.position()
    vx2, vy2, vz2 = stone_2.velocity()
    x3, y3, z3 = stone_3.position()
    vx3, vy3, vz3 = stone_3.velocity()

    x, y, z, vx, vy, vz, t1, t2, t3 = symbols('x y z vx vy vz t1 t2 t3')
    eq1 = Eq(x + vx * t1, x1 + vx1 * t1)
    eq2 = Eq(y + vy * t1, y1 + vy1 * t1)
    eq3 = Eq(z + vz * t1, z1 + vz1 * t1)
    eq4 = Eq(x + vx * t2, x2 + vx2 * t2)
    eq5 = Eq(y + vy * t2, y2 + vy2 * t2)
    eq6 = Eq(z + vz * t2, z2 + vz2 * t2)
    eq7 = Eq(x + vx * t3, x3 + vx3 * t3)
    eq8 = Eq(y + vy * t3, y3 + vy3 * t3)
    eq9 = Eq(z + vz * t3, z3 + vz3 * t3)

    solution = solve([eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9],
                     [x, y, z, vx, vy, vz, t1, t2, t3])

    return sum(solution[0][0:3])



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
