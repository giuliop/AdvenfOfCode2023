import sys


# PART 1

# Your input is of the form:
# Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
# Card 2:  ...
# ...

# The numbers before the | are the winning numbers, the numbers after are the
# numbers you played. The first winning number you have is worth 1 point, each
# next one doubles the points.

# Calculate the total number of points you have across all cards.

def read_input_into_lines():
    with open('../input/4', 'r', encoding='utf-8') as file:
        return file.readlines()

def the_cards():
    """Return a dictionary of cards, where the key is the card number and the
    value is a tuple of the winning numbers and the numbers you played."""
    cards = {}
    for line in read_input_into_lines():
        card_number_string, numbers_string = line.split(':')
        card_number = int(card_number_string.split()[1])
        winning_numbers_string, numbers_played_string = numbers_string.split('|')
        winning_numbers = [int(n) for n in
                           winning_numbers_string.strip().split()]
        numbers_played = [int(n) for n in
                          numbers_played_string.strip().split()]
        cards[card_number] = (winning_numbers, numbers_played)
    return cards

def points_for(card):
    """Return the number of points for the given card."""
    winning_numbers, numbers_played = card
    points = 0
    for number in numbers_played:
        if number in winning_numbers:
            points = 1 if points == 0 else points * 2
    return points

CORRECT_ANSWER_1 = 18653
def answer_1():
    return sum(points_for(card) for card in the_cards().values())

##########################################################################

# PART 2

# Now the rules are different. Each number you have that is a winning number
# makes you win a copy of the following card. So for instance if Card 1 has
# three winning numbers you win a copy of card 2, 3 and 4.
# Process all cards you win and calculate the total cards you got
# (including the starting cards).

# let's memoize the cards we already processed
# this is a dictionary card number : number of cards won
won_cards_by_card_number = {}

def cards_won_by(number, cards):
    """Return the number of cards won by the given card number."""
    if number in won_cards_by_card_number:
        return won_cards_by_card_number[number]

    winning_numbers, numbers_played = cards[number]
    winning_played_numbers = [n for n in numbers_played if n in winning_numbers]
    won_card_numbers = [number + n for n in range(1, len(winning_played_numbers)+1)]
    total_cards_won = (
        len(won_card_numbers) +
        sum(cards_won_by(n, cards) for n in won_card_numbers)
    )
    won_cards_by_card_number[number] = total_cards_won
    return total_cards_won

CORRECT_ANSWER_2 = 5921508
def answer_2():
    cards = the_cards()
    return len(cards) + sum(cards_won_by(n, cards) for n in cards)

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
