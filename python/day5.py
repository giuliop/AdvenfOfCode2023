import sys


# PART 1

# Your input is in the following format:
# seeds: 79 14 55 13

# seed-to-soil map:
# 50 98 2
# ...

# soil-to-fertilizer map:
# 0 15 37

# fertilizer-to-water map:
# 49 53 8

# water-to-light map:
# 88 18 7

# light-to-temperature map:
# 45 77 23

# temperature-to-humidity map:
# 0 69 1

# humidity-to-location map:
# 60 56 37

# Every map is a list of lines of 3 numbers: destination range start,
# source range start, and range length. So the first line in the seed-to-soil
# map means seed 98 maps to soil 50, 99 -> 51 and that's it, range is 2.
# Each number that is not in the range maps to itself.
# Run though the maps in order, and find the lowest "location" mapped from
# the initial seeds.

# TEST = True
TEST = False

DAY = "5"
INPUTFILE = "../input/" + DAY + ("_test" if TEST else "")

def read_input_into_string():
    with open(INPUTFILE, 'r', encoding='utf-8') as file:
        return file.read()

data = read_input_into_string().split('\n\n')

seeds = [int(seed) for seed in data[0].split()[1:]]
seed_to_soil_map = [tuple(map(int, line.split())) for line in data[1].splitlines()[1:]]
soil_to_fertilizer_map = [tuple(map(int, line.split())) for line in data[2].splitlines()[1:]]
fertilizer_to_water_map = [tuple(map(int, line.split())) for line in data[3].splitlines()[1:]]
water_to_light_map = [tuple(map(int, line.split())) for line in data[4].splitlines()[1:]]
light_to_temperature_map = [tuple(map(int, line.split())) for line in data[5].splitlines()[1:]]
temperature_to_humidity_map = [tuple(map(int, line.split())) for line in data[6].splitlines()[1:]]
humidity_to_location_map = [tuple(map(int, line.split())) for line in data[7].splitlines()[1:]]

# sort by the source_range_start
seed_to_soil_map.sort(key=lambda x: x[1])
soil_to_fertilizer_map.sort(key=lambda x: x[1])
fertilizer_to_water_map.sort(key=lambda x: x[1])
water_to_light_map.sort(key=lambda x: x[1])
light_to_temperature_map.sort(key=lambda x: x[1])
temperature_to_humidity_map.sort(key=lambda x: x[1])
humidity_to_location_map.sort(key=lambda x: x[1])

def destination(src, mapping):
    """Take a source number and a mapping and returns the destination number.
    We expect the mapping to be sorted by the first number in the tuple."""
    for destination_range_start, source_range_start, range_length in mapping:
        if source_range_start <= src < source_range_start + range_length:
            return destination_range_start + src - source_range_start
        if src < source_range_start:
            return src
    return src

def location_from_seed(seed):
    """Take a seed and return the location"""
    soil = destination(seed, seed_to_soil_map)
    fertilizer = destination(soil, soil_to_fertilizer_map)
    water = destination(fertilizer, fertilizer_to_water_map)
    light = destination(water, water_to_light_map)
    temperature = destination(light, light_to_temperature_map)
    humidity = destination(temperature, temperature_to_humidity_map)
    return destination(humidity, humidity_to_location_map)

CORRECT_ANSWER_1 = 35 if TEST else 278755257
def answer_1():
    return min(map(location_from_seed, seeds))

##########################################################################

# PART 2

# Now consider the seed list as pairs of numbers describing a range of seed
# numbers: the first number is the start of the range and the second number
# is the length of the range. Recumpute the minimum location number

# split seeds which is a list of numbers into a list of tuples of two
# numbers. So [1, 2, 3, 4] becomes [(1, 2), (3, 4)]

# We are dealing with huge lists of numbers, so instead of analysing
# one seed at a time we'll do by a a range at a time.

seeds_ranges = [(seeds[i], seeds[i+1]) for i in range(0, len(seeds), 2)]
seeds_ranges.sort()

def match(range1, range2):
    """Take two ranges (start, length) and return a tuple of 3 elements:
       1. the subrange 1 left of range2, or None
       2. the subrange 1 overlapping with range2, or None
       3. the subrange 1 right of range2, or None """
    (start1, length1) = range1
    last1 = start1 + length1 - 1
    (start2, length2) = range2
    last2 = start2 + length2 - 1

    left = (start1, min(start2 - start1, length1)) if start1 < start2 else None
    right = (
        (max(start1, last2 + 1), length1 - max(0, last2 - start1 + 1))
        if last1 > last2 else None
    )
    if start1 <= start2 <= last1:
        # start, last = start2, min(last1, last2)
        middle = (start2, min(last1, last2) - start2 + 1)
    elif start2 <= start1 <= last2:
        # start, last = start1, min(last1, last2)
        middle = (start1, min(last1, last2) - start1 + 1)
    else:
        middle = None
    return(left, middle, right)

def destination_ranges(source_ranges, mapping):
    """Take a list of source ranges and an ordered mapping and returns an
       ordered list of destination ranges."""
    dest_ranges = []
    mapping_index = 0
    for to_process in source_ranges:
        while to_process:
            dest_start, range_start, range_length = mapping[mapping_index]
            left, middle, to_process = match(to_process, (range_start, range_length))
            if left:
                dest_ranges.append(left)
            if middle:
                dest_ranges.append((dest_start + middle[0] - range_start,
                                    middle[1]))
            if to_process:
                if mapping_index == len(mapping) - 1:
                    dest_ranges.append(to_process)
                    break
                mapping_index += 1
    dest_ranges.sort()
    return dest_ranges

def locations_from_seed_ranges(seed_ranges):
    """Take a list of seed ranges and return the locations"""
    soil_ranges = destination_ranges(seed_ranges, seed_to_soil_map)
    fertilizer_ranges = destination_ranges(soil_ranges, soil_to_fertilizer_map)
    water_ranges = destination_ranges(fertilizer_ranges, fertilizer_to_water_map)
    light_ranges = destination_ranges(water_ranges, water_to_light_map)
    temperature_ranges = destination_ranges(light_ranges, light_to_temperature_map)
    humidity_ranges = destination_ranges(temperature_ranges, temperature_to_humidity_map)
    location_ranges = destination_ranges(humidity_ranges, humidity_to_location_map)
    return location_ranges

CORRECT_ANSWER_2 = 46 if TEST else 26829166
def answer_2():
    location_ranges = locations_from_seed_ranges(seeds_ranges)
    return location_ranges[0][0]

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
