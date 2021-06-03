# Std Libs:
from itertools import combinations
import time
from typing import Optional
# Local Libs:
from csv_translator import CsvTranslator


class BrutForce:
    """

    """
    def __init__(self,
                 sequence: list,
                 actions: list,
                 budget: Optional[int] = 500) -> None:
        """ """
        #
        self.sequence = sequence
        self.actions = actions
        #
        self.budget = budget
        self.benefits = 0
        self.cost = 0
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
                benefit = cost * (profit/100)

                self.budget -= cost

                if self.budget < 0:
                    break
                else:
                    self.cost += cost
                    self.benefits += benefit
                    transaction = self.actions[index][0]
                    self.transactions.append(transaction)
            else:
                break


def timer(func):
    """ """
    def decorator(**kwargs):
        """ """
        time_a = time.time()
        result = func(**kwargs)
        time_b = time.time()
        print(f"Duration : {round(time_b - time_a, 3)}s")
        return result
    return decorator


@timer
def apply_brut_force(file: str, budget: Optional[int] = 500) -> BrutForce:
    """ """
    actions = CsvTranslator(file).convert_to_list()
    num_actions = len(actions)
    init_seq = [var for var in range(num_actions)]
    best_sequence = BrutForce(init_seq, actions, budget)
    for r in range(num_actions):
        for sequence in combinations(init_seq, r):
            brut_force = BrutForce(sequence, actions)
            if brut_force > best_sequence:
                best_sequence = brut_force
                # print(f"New best : {round(best_sequence.benefits, 2)}€")
                # print(f"\tTransactions : {best_sequence.transactions}")
    dict_decision = {
        "actions": best_sequence.transactions,
        "cost": best_sequence.cost,
        "return": round(best_sequence.benefits, 2)
    }
    return dict_decision


def main() -> BrutForce:
    """ """
    budget = int(input("Give budget : "))
    file = input("Give csv file name : ")
    dict_args = {
        "file": file,
        "budget": budget,
    }
    return apply_brut_force(**dict_args)


if __name__ == '__main__':
    best_decision = main()
    print(f"{best_decision}")
