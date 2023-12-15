import sys


# PART 1

# Your input is a sequence of multiline patterns such as this (separated
# by a blank line):
#   #.##..##.
#   ..#.##.#.
#   ##......#
#   ##......#
#   ..#.##.#.
#   ..##..##.
#   #.#.##.#.

# Find vertical or horizontal lines of reflection, that is lines that separate
# simmetrical subpatterns (ignoring the extra lines or columns).
# There is at most one vertical and one horizontal line of reflection in each pattern.
# Add up the number of columns to the left of each vertical line of reflection,
# then to that add 100 multiplied by the number of rows above each horizontal
# line of reflection.

def read_input_into_patterns():
    """Read the input file and return it as a list of lines stripped of
       leading or trailing whitespace."""
    with open('../input/13', 'r', encoding='utf-8') as file:
        patterns = file.read().split('\n\n')
        patterns = [pattern.split('\n') for pattern in patterns]
        patterns[-1] = patterns[-1][:-1]
        return patterns

def same_columns(pattern, i, j):
    """Return True if the columns i and j of the pattern are the same."""
    # print(i, j)
    for row in pattern:
        if row[i] != row[j]:
            return False
    return True

def count_vertical_lines(pattern):
    """Return the number of columns left of vertical lines that separate simmetrical
       subpatterns. We identify lines by the index of the column to the left of
       them."""
    for i in range(len(pattern[0]) - 1):
        # print("i: ", i)
        max_columns_left = i+1
        max_columns_right = len(pattern[0])-i-1
        # half_width * 2 is the number of columns to consider for the reflection
        half_width =  min(max_columns_left, max_columns_right)
        # print("half_width: ", half_width)
        # print("range: ", i+1-half_width, i+1)
        if all(same_columns(pattern, j, half_width+i-ii)
               for ii, j in enumerate(range(i+1-half_width, i+1))):
            return i + 1
    return 0

def same_rows(pattern, i, j):
    """Return True if the rows i and j of the pattern are the same."""
    return pattern[i] == pattern[j]

def count_horizontal_lines(pattern):
    """Return the number of rows above horizontal lines that separate simmetrical
       subpatterns. We identify lines by the index of the row above them."""
    for i in range(len(pattern) - 1):
        # print("i: ", i)
        max_rows_above = i+1
        max_rows_below = len(pattern)-i-1
        # half_height * 2 is the number of rows to consider for the reflection
        half_height =  min(max_rows_above, max_rows_below)
        # print("half_height: ", half_height)
        # print("range: ", i+1-half_height, i+1)
        if all(same_rows(pattern, j, half_height+i-ii)
               for ii, j in enumerate(range(i+1-half_height, i+1))):
            return i + 1
    return 0


CORRECT_ANSWER_1 = 34821
def answer_1():
    return sum(count_vertical_lines(pattern) + 100 * count_horizontal_lines(pattern)
               for pattern in read_input_into_patterns())

##########################################################################

# PART 2

# Now you need to find new lines of reflections is each pattern after changing
# exactly one character (the "smudge") in each pattern. You will find one new
# line of reflection in each pattern

def diffs_by_columns(pattern, i, j):
    """Return the number of differences between columns i and j of the pattern
       (stopping if 2 differences are found)"""
    diffs = 0
    for row1, row2 in zip(pattern, pattern):
        if row1[i] != row2[j]:
            diffs += 1
            if diffs == 2:
                break
    return diffs

def count_vertical_lines_with_smudge(pattern):
    """Return the number of columns left of vertical lines that separate simmetrical
       subpatterns with one smudge.
       We identify lines by the index of the column to the left of them."""
    # first check for new vertical lines of reflection
    for i in range(len(pattern[0]) - 1):
        max_columns_left = i+1
        max_columns_right = len(pattern[0])-i-1
        half_width =  min(max_columns_left, max_columns_right)
        total_diffs = 0
        for ii, j in enumerate(range(i+1-half_width, i+1)):
            diffs = diffs_by_columns(pattern, j, half_width+i-ii)
            total_diffs += diffs
            if  total_diffs > 2:
                break
        if total_diffs == 1:
            return i +1
    return 0

def diffs_by_rows(pattern, i, j):
    """Return the number of differences between rows i and j of the pattern
       (stopping if 2 differences are found)"""
    diffs = 0
    for c1, c2 in zip(pattern[i], pattern[j]):
        if c1 != c2:
            diffs += 1
            if diffs == 2:
                break
    return diffs


def count_horizontal_lines_with_smudge(pattern):
    """Return the number of rows above horizontal lines that separate simmetrical
       subpatterns with one smudge.
       We identify lines by the index of the row above them."""
    for i in range(len(pattern) - 1):
        max_rows_above = i+1
        max_rows_below = len(pattern)-i-1
        half_height =  min(max_rows_above, max_rows_below)
        total_diffs = 0
        for ii, j in enumerate(range(i+1-half_height, i+1)):
            diffs = diffs_by_rows(pattern, j, half_height+i-ii)
            total_diffs += diffs
            if  total_diffs > 2:
                break
        if total_diffs == 1:
            return i +1
    return 0

CORRECT_ANSWER_2 = 36919
def answer_2():
    return sum(count_vertical_lines_with_smudge(pattern) +
               100 * count_horizontal_lines_with_smudge(pattern)
           for pattern in read_input_into_patterns())

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
