import sys


# PART 1

# each line of your input is a sequence of numbers like this:
# 0 3 6 9 12 15

# you need to extrapolate the next number in the sequence by iteratively
# computing the difference between each number and the next one, until thses
# are all zeros:

# 0   3   6   9   12   15
#   3   3   3   3    3
#     0   0   0   0

# Then from the bottom-up, you add the last number of the last line to the
# last number of the second-to-last line, and so on, until you reach the top

# 0   3   6   9   12   15 -> 18
#   3   3   3   3    3 -> 3
#     0   0   0   0

# So in this case, the next number in the sequence is 18. Sum all the next
# numbers in the sequence for all lines in your input.

def read_input_into_lines():
    with open('../input/9', 'r', encoding='utf-8') as file:
        return file.readlines()

def input_sequences():
    lines = read_input_into_lines()
    return [[int(number) for number in line.split()] for line in lines]

def next_value(line):
    """Take a line and extrapolate the next value"""
    last_numbers= [line[-1]]
    while True:
        # compute the difference between each number and the next one
        numbers = [line[i+1] - line[i] for i in range(len(line)-1)]
        # if all differences are zero, we're done
        if all(number == 0 for number in numbers):
            break
        # otherwise, add the last number to the list of last numbers
        last_numbers.append(numbers[-1])
        # and replace the line with the differences
        line = numbers
    # now add the last numbers from the bottom up
    for i in range(len(last_numbers)-1, 0, -1):
        last_numbers[i-1] += last_numbers[i]
    return last_numbers[0]

CORRECT_ANSWER_1 = 1725987467
def answer_1():
    sequences = input_sequences()
    return sum(next_value(seq) for seq in sequences)

##########################################################################

# PART 2

# Now let's extrapolate the first number in the sequence instead of the last.
# As before compute iteratively the differences between each number and the
# next one, until they are all zero.
# Now instead of adding the last numbers from the bottom up, subtract them
# to the first number of the line above until you reach the top. E.g.:

# 10  13  16  21  30  45

# results in 5:

# 5 <- 10   13   16   21   30    45
#   5 <-  3    3    5    9    15
#     -2 <-  0   2     4    6
#        2 <-  2    2    2
#                 0   0

def previous_value(line):
    """Take a line and extrapolate the previous value"""
    first_numbers= [line[0]]
    while True:
        # compute the difference between each number and the next one
        numbers = [line[i+1] - line[i] for i in range(len(line)-1)]
        # if all differences are zero, we're done
        if all(number == 0 for number in numbers):
            break
        # otherwise, add the first number to the list of first numbers
        first_numbers.append(numbers[0])
        # and replace the line with the differences
        line = numbers
    # now subtract the first numbers from the bottom up
    for i in range(len(first_numbers)-1, 0, -1):
        first_numbers[i-1] -= first_numbers[i]
    return first_numbers[0]

CORRECT_ANSWER_2 = 971
def answer_2():
    sequences = input_sequences()
    return sum(previous_value(seq) for seq in sequences)

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
