# Std Libs:
import math
from itertools import permutations
# Local Libs:
from csv_translator import CsvTranslator


class BrutForce:
    """

    """
    def __init__(self, sequence):
        self.sequence = sequence
        self.actions = CsvTranslator("actions").translated_list()

        self.budget = 500
        self.profit = 0

    def __lt__(self, obj):
        return self.profit < obj.profit

    def simulate(self):
        pass


def swap_elements(list, n1, n2):
    list[n1], list[n2] = list[n2], list[n1]
    return list


def steps_factorial(number):
    """Give factors of factorial

    Args:
        number (int): range of factorial

    Returns:
        list: List of steps
    """
    factorial = math.factorial(number)
    steps = []
    while factorial > 1:
        steps.append(factorial)
        factorial = factorial//number
        number -= 1
    steps.append(1)
    return steps


def generate_sequences(num_seq):
    """Generate all permutations' sequences
        O(num_seq!)

    Args:
        num_seq (int): the range of the list

    Returns:
        [List] : List of sequences' list
    """
    # Generate the list that'll be sequenced:
    init_seq = [var for var in range(num_seq)]
    sequences = list(permutations(init_seq))
    return sequences
