# Std Libs:
from itertools import combinations
from typing import Optional
import time
# Local Libs:
from csv_translator import CsvTranslator


class BrutForce:
    """
    Simulate the benefits according to a given sequence.
    """
    def __init__(self,
                 sequence: list,
                 actions: list,
                 budget: Optional[int] = 500) -> None:
        """
        Making the simulation in it.

        Args:
            - sequence (list) : The sequence given for this simulation.
            - actions (list)  : The actions.
            - budget (int)    : The budget, optional.
        """
        # Arguments
        self.sequence = sequence
        self.actions = actions
        self.budget = budget
        # Initialization
        self.benefits = 0
        self.cost = 0
        self.transactions = []
        # Simulating
        self.buy()

    def __lt__(self, obj) -> bool:
        """
        Define the comparasion between BrutForce objects by their benefits.
        """
        if self.benefits < obj.benefits:
            return True
        return False

    def buy(self) -> None:
        """
        Try to buy every action according to the sequence.
        If budget < 0, then it break the loop.

        That updates (self) :
            - budget
            - cost
            - benefits
            - transactions
        """
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
    """
    A little decorator function that give that execution time of a function.
    """
    def decorator(**kwargs):
        """
        Print the difference of time between start and end of function's exec'.
        """
        time_a = time.time()
        result = func(**kwargs)
        time_b = time.time()
        print(f"Duration : {round(time_b - time_a, 3)}s")
        return result
    return decorator


@timer
def apply_brut_force(file: str, budget: Optional[int] = 500) -> dict:
    """
    Apply a brute force method.
    For each combinations of actions given, return the benefit
    then it compares this benefits to the best benefit already registered.
    If it's higher, then it replaces the old best benefit.
    Else, pass to the next combination.

    Args:
        - file (str)  : Name of the .csv file (check main() for precisions)
        - budget (int): The amout of money for investments

    Algorithm: (Sifting algorithm)
        1. Get a list of each actions (actions)
        2. Initialize :
            a) Set the initial sequence representing the index of each actions.
            b) Set the first best_sequence object.
        3. For a number (A) that'll go from 0 to the size of the initial seq'.
            a) Then for each combinations of the initial seq at size (A):
                I)  Simulate the brut force with the combination
                II) If this brut force simulation is greater than the best
                    - Replace the older best by this simulation
        4. Return the informations of the very best simulation :
            - Actions choosen
            - The total cost
            - The total return
    """
    actions = CsvTranslator(file).convert_to_list()
    num_actions = len(actions)
    init_seq = [var for var in range(num_actions)]
    best_sequence = BrutForce(init_seq, actions, budget)
    for r in range(num_actions):
        for sequence in combinations(init_seq, r):
            brut_force = BrutForce(sequence, actions)
            if brut_force > best_sequence:
                best_sequence = brut_force
    dict_decision = {
        "actions": best_sequence.transactions,
        "cost": best_sequence.cost,
        "return": round(best_sequence.benefits, 2)
    }
    return dict_decision


def main() -> dict:
    """
    This function is called to apply brut strategy with inputs.

    Inputs :
        - budget (int) : The amount of money for investments
        - file (str)   : Name of the .csv file that contain three columns
                         'action_name', 'price' & 'profit'
    Returns:
        - dict (dict)  : A dictionnary containing several informations:
                            - actions took
                            - The total cost according to the budget
                            - The return of the investment
    """
    budget = int(input("Give budget : "))
    file = input("Give .csv file name : ")
    dict_args = {
        "file": file,
        "budget": budget,
    }
    return apply_brut_force(**dict_args)


if __name__ == '__main__':
    best_decision = main()
    print(f"{best_decision}")
