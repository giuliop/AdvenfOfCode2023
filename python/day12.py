import sys
import re
import itertools
from collections import defaultdict

# PART 1

# Your input is a series of lines with this format:

# ???.### 1,1,3
# .??..??...?##. 1,1,3
# ...

# '#' indicates an operational spring
# '.' indicates a broken spring
# '?' indicates an unknown spring
# The numbers at the end indicate the counts of continguous opertional springs

# Your task is to determine the number of possible configurations consistent
# with the input. For example, the first line of the input above has only one
# possible configuration, the second line has 10.
# Sum all the possible configurations for all the lines in the input.

def read_input_into_lines():
    """Read the input file and return it as a list of lines stripped of
       leading or trailing whitespace."""
    with open('../input/12', 'r', encoding='utf-8') as file:
        return [line.strip() for line in file.readlines()]

def parse_line(line):
    """Parse a line of the input into a tuple of
           groups, list(counts)
       where a group is a string of consecutive '?' or '#' and
       counts is a list of the counts at the end of the line."""
    group, counts = line.split(' ')
    return group, [int(count) for count in counts.split(',')]

def substitute(group, indexes):
    """Take a group and a list of indexes and return a group with '#' at indexes"""
    return ''.join('#' if i in indexes else char for i, char in enumerate(group))

def valid(group, counts):
    """Take a group and counts of '#' and return True if group matches counts"""
    groupings = re.findall(r"\#+", group)
    return len(groupings) == len(counts) and all(
            len(g) == counts[i] for i, g in enumerate(groupings))

def count_configurations(group, counts):
    """Take a group and counts and return the number of valid configurations"""
    unknown_indexes = [i for i, char in enumerate(group) if char == '?']
    missing = sum(c for c in counts) - group.count('#')
    combinations = itertools.combinations(unknown_indexes, missing)
    return len([c for c in combinations
                if valid(substitute(group, c), counts)])

CORRECT_ANSWER_1 = 7939
def answer_1():
    return sum(count_configurations(*parse_line(line))
               for line in read_input_into_lines())

##########################################################################

# PART 2

# Now expand each group and counts 5 times and recount the configurations.
# When expanding, add a '?' at the end of each group except the last
# So for instance .# 1 would become .#?.#?.#?.#?.# 1,1,1,1,1

# We turn counts into a string of possible consecutive states for a correct
# sequence, that is each char represent a possible state, in this way:
# (1, 3, 2) -> '.#.###.##.'

# In practice we turn each count into a ".###" string and end with a '.'
# The idea is that a '.' state can represent any number of '?' or '.', while
# a '#' state represents a '#'

# We then keep track of the active states and the number of paths to get there,
# processing one char of group at a time.

def count_configurations_2(group, counts):
    """Take a group and counts and return the number of valid configurations"""
    states = generate_states(counts)

    # we keep track of the active states, and the number of configurations so far
    active_states = {0: 1}

    for next_char in group:
        new_active_states = defaultdict(int)
        for state_index, current_count in active_states.items():
            state = states[state_index]
            next_state = states[state_index + 1] if state_index < len(states) - 1 else None
            if next_char == '#':
                if next_state == '#':
                    new_active_states[state_index + 1] += current_count
            elif next_char == '.':
                if state == '.':
                    new_active_states[state_index] += current_count
                elif next_state == '.':     # state == '#'
                    new_active_states[state_index + 1] += current_count
            else:   # next_char == '?'
                if next_state:
                    new_active_states[state_index + 1] += current_count
                if state == '.':
                    new_active_states[state_index] += current_count

        active_states = new_active_states

    return active_states[len(states) - 1] + active_states[len(states) - 2]

def generate_states(counts):
    """Take a list of counts and return a string of possible states"""
    return ''.join('.' + '#' * count for count in counts) + '.'

def expand(group, counts, n=5):
    """Take a group and counts and return an expanded group and counts"""
    return(((group + '?') * n)[:-1], counts * n)

CORRECT_ANSWER_2 = 850504257483930
def answer_2():
    return sum(count_configurations_2(*expand(*parse_line(line)))
               for line in read_input_into_lines())


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
