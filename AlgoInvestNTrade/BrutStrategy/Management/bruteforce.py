# Std Libs:
import math
from itertools import permutations, combinations
from sys import stdout
# Local Libs:
from csv_translator import CsvTranslator


class BrutForce:
    """

    """
    def __init__(self, sequence, actions):
        """ """
        self.sequence = sequence
        self.actions = actions

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
    actions = CsvTranslator("actions").convert_to_list()
    best_sequence = BrutForce(init_seq, actions)
    print(f"best : {best_sequence.benefits}")
    counter = 0
    for r in range(20):
        for sequence in combinations(init_seq, r):
            counter+=1
            stdout.write(f"\r{round((counter*100)/(math.pow(2, 20)))}%")
            stdout.flush()
            brut_force = BrutForce(sequence, actions)
            if brut_force > best_sequence:
                best_sequence = brut_force
                print(f"New best : {best_sequence.benefits}")
                print(f"\tTransactions : {best_sequence.transactions}")
    return best_sequence

if __name__ == '__main__':
    a = main()
    print(f"Very Best : {a.benefits}")
    print(f"\tTransactions : {a.transactions}")