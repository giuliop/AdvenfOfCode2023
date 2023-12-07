import sys
import math


# PART 1

# Consider toy boat races with fixed time. Who goes the furthest wins.
# At the start of the race you can hold the power button of the boat, for
# each ms you hold it, the boat speed once you release the button will be
# 1mm/ms faster. So if you press for 5mms, the boat will go at 5mm/ms.
# The time spent pressing the button still counts as race time.
# The boat does not move until you release the button.

# Your input is the following:

# Time:        53     91     67     68
# Distance:   250   1330   1081   1025

# Each column is a race, with the time it lasts and the record distance.

# For each race, calculate how many options you have for time spent pressing
# the button and set a new record. Multiply all those options together.

def read_input_into_lines():
    with open('../input/6', 'r', encoding='utf-8') as file:
        return file.readlines()

def races():
    race_data = read_input_into_lines()
    times = race_data[0].split(':')[1].split()
    records = race_data[1].split(':')[1].split()
    return [(int(time), int(record)) for time, record in zip(times, records)]

def distance(time_pressed, race_time):
    return (race_time - time_pressed) * time_pressed

def count_record_options(race):
    # return the list of times_pressed that beat the record
    race_time, record = race
    return len([time_pressed for time_pressed in range(1, race_time)
               if distance(time_pressed, race_time) > record])

CORRECT_ANSWER_1 = 625968
def answer_1():
    return math.prod(count_record_options(race) for race in races())

##########################################################################

# PART 2

# Now you should read your input as just one race, ignoring
# the spaces between columns:

# Time:       53916768
# Distance:   250133010811025

# Calculate the number of options for time_pressed that beat the record.

def race():
    """The time, record from the input file"""
    race_data = read_input_into_lines()
    times = race_data[0].split(':')[1].split()
    records = race_data[1].split(':')[1].split()
    return (int(''.join(times)), int(''.join(records)))

CORRECT_ANSWER_2 = 43663323
def answer_2():
    return count_record_options(race())

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
