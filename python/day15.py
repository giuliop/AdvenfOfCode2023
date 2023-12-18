import sys
from collections import defaultdict

# PART 1

# Your input is one line of comma-separated characters.
# You need to run the HASH algorithm (described below) on each group of characters
# and sum the results.
# The HASH algorithm is as follows:
#   1. Start from 0
#   2. Sum the ASCII value of next character
#   3. Multiply by 17
#   4. Take the remainder of dividing by 256
#   5. Repeat from step 2 for each character

def generate_groups():
    """Read the input file into a string and return a generator of groups of
       characters splitting on commas."""
    with open('../input/15', 'r', encoding='utf-8') as file:
        return (group for group in file.read().strip().split(','))

def hash_algo(group):
    """Run the HASH algorithm on a group of characters."""
    value = 0
    for char in group:
        value = ( (value + ord(char)) * 17 ) % 256
    return value

CORRECT_ANSWER_1 = 513158
def answer_1():
    return sum(hash_algo(group) for group in generate_groups())

##########################################################################

# PART 2

# Your input is a series of instructions of two forms, as in these two examples:
#   rn=1
#   rn-

# The characters at the beginning are "lens labels" and if given as input to the HASH
# algorithm will produce a number between 0 and 255, identifying one of 256 "boxes".

# The label=n form means to add [label n] to the resulting box. If there is already
# that label in the box, replace the value.

# The label- form means to remove [label] from the box, maintaining the order of
# the other labels (oldest first).

# Process all your instructions and then add up all the "focusing power" of the
# lenses (labels). The focusing power of a lens is found by multiplying together:
# (1 + box numnber) * (position of label in box, starting from 1) * (value of label)

# label : [box number, position in box, value]
labels = {}

# box : [length of box, set(labels)]
boxes = {}

def focusing_power(label):
    """Calculate the focusing power of a label."""
    box, position, value = labels[label]
    return (1 + box) * position * value

CORRECT_ANSWER_2 = 200277
def answer_2():
    for instruction in generate_groups():
        if '=' in instruction:
            label, value = instruction.split('=')
            value = int(value)
            if label in labels:
                labels[label][2] = value
            else:
                box = hash_algo(label)
                if box not in boxes:
                    boxes[box] = [1, set([label])]
                else:
                    boxes[box][0] += 1
                    boxes[box][1].add(label)
                labels[label] = [box, boxes[box][0], value]
        else:   # - in instruction
            label = instruction[:-1]
            if label in labels:
                box = labels[label][0]
                position = labels[label][1]
                del labels[label]
                boxes[box][0] -= 1
                boxes[box][1].remove(label)
                for label in boxes[box][1]:
                    if labels[label][1] > position:
                        labels[label][1] -= 1
    return sum(focusing_power(label) for label in labels)

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
