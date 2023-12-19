import sys

# PART 1

# Your input is a series of rules to apply to part and parts.
# The rules come first, then a blank line, then the parts.

# The parts are of the form: {x=787,m=2655,a=1222,s=2876}
# They have four attributes: x, m, a, s with a corresponding value.

# The rules are of the form: px{a<2006:qkq,m>2090:A,rfg}
# They have a label (px), and a list of condition:label, comma-separated.

# All parts start with the rule labeled "in" and go through the conditions
# sequentially. If a condition is met, the part is sent to that label.
# If the lavel is 'A' the part is accepted, if 'R' it is rejected and in
# these two cases processing ends.

# Process all parts and for the accepted ones, sum the values of all attributes.

def read_input():
    """Read the input file and return a tuple (list[rules], list[parts])"""
    with open('../input/19', 'r', encoding='utf-8') as file:
        rules, parts = file.read().split('\n\n')
    rules = [line.strip() for line in rules.split('\n')]
    parts = [line.strip() for line in parts.split('\n')]
    if rules[-1] == '':
        rules.pop()
    if parts[-1] == '':
        parts.pop()
    return rules, parts

class Condition:
    """A condition is a tuple (attribute, operator, value, label)
       Conditions could be (None, None, None, label) where label could be
       a rule lable, 'A' or 'R'"""
    def __init__(self, attribute, operator, value, label):
        self.attribute = attribute
        self.operator = operator
        self.value = value
        self.label = label

    @classmethod
    def from_string(cls, condition_string):
        if not ':' in condition_string:
            return Condition(None, None, None, condition_string)

        left, label = condition_string.split(':')
        op_position = left.find('<') if '<' in left else left.find('>')
        assert op_position != -1

        attribute = left[:op_position]
        operator = left[op_position]
        value = int(left[op_position+1:])

        return Condition(attribute, operator, value, label)

def parse_rules(rules_strings):
    """Parse a rule string into a label, list of conditions tuple"""
    label, conditions_string = rules_strings.split('{')
    condition_strings = conditions_string[:-1].split(',')
    conditions = [Condition.from_string(c) for c in condition_strings]
    return label, conditions

def parse_parts(part_string):
    """Parse a part string into a dictionary of attributes and values"""
    part_string = part_string[1:-1]
    pairs = part_string.split(',')
    return {p.split('=')[0] : int(p.split('=')[1]) for p in pairs}

def is_accepted(part, rules, start_label='in'):
    """Return True if the part is accepted, False if rejected"""
    if start_label == 'A':
        return True
    if start_label == 'R':
        return False
    rule = rules[start_label]
    for condition in rule:
        if condition.attribute is None:
            return is_accepted(part, rules, condition.label)
        if condition.attribute not in part:
            continue
        if condition.operator == '<':
            if part[condition.attribute] < condition.value:
                return is_accepted(part, rules, condition.label)
        elif condition.operator == '>':
            if part[condition.attribute] > condition.value:
                return is_accepted(part, rules, condition.label)
    raise ValueError('No label found for part')

CORRECT_ANSWER_1 = 409898
def answer_1():
    rule_strings, part_strings = read_input()
    rules = {label : conditions for label, conditions in
             (parse_rules(r) for r in rule_strings)}
    parts = [parse_parts(p) for p in part_strings]

    accepted_parts = [p for p in parts if is_accepted(p, rules)]
    return sum(sum(p.values()) for p in accepted_parts)

##########################################################################

# PART 2

# Now consider only the rules and calculates the total number of different parts
# (i.e., distinct attributes combinations) that could be accepted.

# The strategy we will follow is to start with the rule labeled 'in' and
# trasverse the rules graph, building all the possible paths as dictionaries
# of attribure constraints. When we reach a rule labeled 'A' we add the
# current path to the list of accepted paths.

class Path:
    """A path is a dictionary of attribute constraints"""
    # {a : {'<' : 100, > : 50}, m : {'>' : 20} }

    # class constants
    attributes = ['a', 'm', 's', 'x']
    operators = ['<', '>']
    min_attribute_value = 1
    max_attribute_value = 4000

    def __init__(self):
        self.constraints = {x : {} for x in self.attributes}

    @classmethod
    def copy(cls, path):
        """Return a copy of the path"""
        new_path = cls()
        for attribute, constraints in path.constraints.items():
            new_path.constraints[attribute] = constraints.copy()
        return new_path

    def add_constraint(self, attribute, operator, value):
        """Add a constraint to the path, return True if the constraint is
           compatible or False if it is not"""
        current_value = self.constraints[attribute].get(operator)
        if not current_value:
            self.constraints[attribute][operator] = value
        elif operator == '<':
            self.constraints[attribute][operator] = min(current_value, value)
        elif operator == '>':
            self.constraints[attribute][operator] = max(current_value, value)
        return is_compatible(self.constraints[attribute])

    def count_combinations(self):
        """Return the number of combinations from the path"""
        combinations = 1
        for _, constraints in self.constraints.items():
            if len(constraints) == 0:
                combinations *= self.max_attribute_value
            if len(constraints) == 2:
                combinations *= constraints['<'] - constraints['>'] - 1
            if len(constraints) == 1:
                if '<' in constraints:
                    combinations *= constraints['<'] - self.min_attribute_value
                else:
                    combinations *= self.max_attribute_value - constraints['>']
        return combinations

def is_compatible(constraints):
    """Return True if the constraints are compatible, False otherwise"""
    if '<' in constraints and '>' in constraints:
        return constraints['>'] < constraints['<'] - 1
    return True

def build_accepted_paths(rules):
    """Traverse the rules graph and build all the accepted paths"""
    accepted_paths = []

    def traverse_rules(path, label):
        if label == 'A':
            accepted_paths.append(path)
            return
        if label == 'R':
            return
        rule = rules[label]
        for condition in rule:
            if condition.attribute is None:
                traverse_rules(path, condition.label)
            else:
                # we duplicate the path to follow two branches, fulfilling or not the condition
                new_path = Path.copy(path)
                if condition.operator == '<':
                    if new_path.add_constraint(condition.attribute, '<', condition.value):
                        traverse_rules(new_path, condition.label)
                    if not path.add_constraint(condition.attribute, '>', condition.value - 1):
                        break
                elif condition.operator == '>':
                    if new_path.add_constraint(condition.attribute, '>', condition.value):
                        traverse_rules(new_path, condition.label)
                    if not path.add_constraint(condition.attribute, '<', condition.value + 1):
                        break

    traverse_rules(Path(), 'in')
    return accepted_paths


CORRECT_ANSWER_2 = 113057405770956
def answer_2():
    rule_strings, _ = read_input()
    rules = dict(parse_rules(r) for r in rule_strings)
    accepted_paths = build_accepted_paths(rules)
    return sum(path.count_combinations() for path in accepted_paths)

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
