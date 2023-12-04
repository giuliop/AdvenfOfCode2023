import sys
from collections import defaultdict


# PART 1

# You have input such as this, a list of "games":
# Game 2: 6 blue, 3 green; 4 red, 1 green, 7 blue; 2 green

# You have to ouput the sum of game ids (e.g., 2 above) that are valid,
# that is that have a number of balls equal or lower with the following:
# 12 red cubes, 13 green cubes, and 14 blue cubes

def read_input_into_lines():
    with open('../input/2', 'r', encoding='utf-8') as file:
        return file.readlines()

def game_id(game):
    """Return the game id"""
    return int(game.split(':')[0].split(' ')[1])

def draws(game):
    """Return a list of dicts of color to number of balls"""
    res = []
    for draw in game.split(':')[1].split(';'):
        balls_data = defaultdict(int)
        for part in draw.strip().split(','):
            part = part.strip()
            number, color = part.split(' ')
            balls_data[color] = int(number)
        res.append(balls_data)
    return res

def games_data():
    """Split input into a dict of game id to a list of ball numbers"""
    games = read_input_into_lines()
    return {game_id(game): draws(game) for game in games}

def is_valid(draw):
    """Return whether a game is valid"""
    return draw['red'] <= 12 and draw['green'] <= 13 and draw['blue'] <= 14

CORRECT_ANSWER_1 = 2406
def answer_1():
    """Return the sum of valid game ids"""
    return sum(game_id for game_id, draws in games_data().items()
               if all(is_valid(draw) for draw in draws))

##########################################################################

# PART 2

# For each game, find the minimum number of balls needed to make it valid.
# Then multiply this minimum number of balls together to find the `power`
# of that game. Return the sum of all powers.

def minimum_balls(draws):
    """Return the minimum number of balls needed to make a game valid"""
    # calculate the max number of balls of each color for all draws in a game
    min_balls = {}
    for color in ['red', 'green', 'blue']:
        min_balls[color] = max(draw[color] for draw in draws)
    return min_balls

def power(draw):
    """Return the power of a draw"""
    return draw['red'] * draw['green'] * draw['blue']

CORRECT_ANSWER_2 = 78375
def answer_2():
    data = games_data()
    return sum(power(minimum_balls(draws)) for draws in data.values())

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
