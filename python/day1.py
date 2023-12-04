import sys


# PART 1

# load file `input/1` into a list of strings
# each string is a combination of numbers and letters
# from each string, extract the first and last digit
# and concatenate them into a two digit number
# for example, if the string is `a1sdf234sdf`, the number is `14`

# find the sum of all the numbers

def read_input_into_lines():
    with open('../input/1', 'r', encoding='utf-8') as f:
        return f.readlines()

def first_digit(line):
    for char in line:
        if char.isdigit():
            return char

def last_digit(line):
    for char in reversed(line):
        if char.isdigit():
            return char

CORRECT_ANSWER_1 = 54450
def answer_1():
    input_lines = read_input_into_lines()
    nums = ((int(first_digit(line) + last_digit(line)))
            for line in input_lines)
    return sum(nums)

##########################################################################

# PART 2

# Now consider also numbers spelled out as words
# e.g., two1nine -> 29

NUMBER_WORDS = {
    'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
    'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9
}

NUMBERS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

def word_indexes(line):
    # return a dictionary of all the positions of the keys in NUMBER_WORDS
    # in line, using the values as keys, e.g., {2: [0, 4], 1: [1]}
    indexes = {}
    for word, num in NUMBER_WORDS.items():
        index = line.find(word)
        if index == -1:
            continue
        indexes[num] = []
        while index != -1:
            indexes[num].append(index)
            index = line.find(word, index + 1)
    return indexes

def number_indexes(line):
    # return a dictionsy of all the positions of the numbers in NUMBERS
    # in line, e.g., {1: [0, 4], 2: [1]}
    indexes = {}
    for number in NUMBERS:
        index = line.find(str(number))
        if index == -1:
            continue
        indexes[number] = []
        while index != -1:
            indexes[number].append(index)
            index = line.find(str(number), index + 1)
    return indexes

CORRECT_ANSWER_2 = 54265
def answer_2():
    input_lines = read_input_into_lines()
    res = 0
    for line in input_lines:
        d1 = word_indexes(line)
        d2 = number_indexes(line)
        indexes =  {key: d1.get(key, []) + d2.get(key, [])
                    for key in set(d1) | set(d2)}
        # first_digit is the key with the smallest value
        first = min(indexes, key=lambda key: min(indexes[key]))
        # last_digit is the key with the largest value
        last = max(indexes, key=lambda key: max(indexes[key]))
        res += int(str(first) + str(last))
    return res

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
