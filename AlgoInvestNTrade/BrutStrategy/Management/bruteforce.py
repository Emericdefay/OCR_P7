# Std Libs:
import math
from itertools import permutations
# Local Libs:
from csv_translator import CsvTranslator


class BrutForce:
    """

    """
    def __init__(self, sequence):
        """ """
        self.sequence = sequence
        self.actions = CsvTranslator("actions").convert_to_list()

        self.budget = 500
        self.benefits = 0
        self.transactions = []

        self.buy()

    def __lt__(self, obj):
        """ """
        if self.benefits < obj.benefits:
            return True
        return False

    def buy(self):
        """ """
        for index in self.sequence:
            if self.budget > 0:
                cost = self.actions[index][1]
                profit = self.actions[index][2]
                benefit = cost*(profit/100)

                self.budget -= cost

                if self.budget < 0:
                    break
                else:
                    self.benefits += benefit
                    transaction = self.actions[index][0]
                    self.transactions.append(transaction)
            else:
                break


def main():
    init_seq = [var for var in range(20)]
    brut_sequences = []
    best_sequence = BrutForce(init_seq)
    print(f"best : {best_sequence.benefits}")
    for sequence in permutations(init_seq):
        brut_force = BrutForce(sequence)
        if brut_force > best_sequence:
            best_sequence = brut_force
            print(f"New best : {best_sequence.benefits}")
            print(f"\tTransactions : {best_sequence.transactions}")
    

if __name__ == '__main__':
    main()