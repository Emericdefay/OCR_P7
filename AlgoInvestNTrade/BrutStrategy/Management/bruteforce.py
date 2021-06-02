# Std Libs:
import math
from itertools import permutations, combinations
from sys import stdout
# Local Libs:
from csv_translator import CsvTranslator


class BrutForce:
    """

    """
    def __init__(self, sequence: list, actions: list) -> None:
        """ """
        self.sequence = sequence
        self.actions = actions

        self.budget = 500
        self.benefits = 0
        self.transactions = []

        self.buy()

    def __lt__(self, obj) -> bool:
        """ """
        if self.benefits < obj.benefits:
            return True
        return False

    def buy(self) -> None:
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


def main() -> BrutForce:
    """ """
    actions = CsvTranslator("actions").convert_to_list()
    num_actions = len(actions)
    init_seq = [var for var in range(num_actions)]
    best_sequence = BrutForce(init_seq, actions)
    print(f"best : {best_sequence.benefits}")
    for r in range(num_actions):
        for sequence in combinations(init_seq, r):
            brut_force = BrutForce(sequence, actions)
            if brut_force > best_sequence:
                best_sequence = brut_force
                print(f"New best : {round(best_sequence.benefits, 2)}€")
                print(f"\tTransactions : {best_sequence.transactions}")
    return best_sequence

if __name__ == '__main__':
    a = main()
    print(f"Very Best : {round(a.benefits, 2)}€")
    print(f"\tTransactions : {a.transactions}")