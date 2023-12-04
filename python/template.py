import sys


# PART 1

def read_input_into_lines():
    with open('../input/XXX', 'r', encoding='utf-8') as file:
        return file.readlines()

CORRECT_ANSWER_1 = None
def answer_1():
    pass

##########################################################################

# PART 2

CORRECT_ANSWER_2 = None
def answer_2():
    pass

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
