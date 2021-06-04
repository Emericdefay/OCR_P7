# Std Libs:
import time
from typing import Optional
# External Libs:
import numpy as np
# Local Libs:
from csv_translator import CsvTranslator


class Optimized:
    """
    Able to choose best benefits actions.
    Given actions & budget.
    """
    def __init__(self,
                 actions_file_name: str,
                 budget: Optional[int] = 500,
                 minimum_cost: Optional[float] = 0.,
                 static_fees: Optional[float] = 0.,
                 pourc_fees: Optional[float] = 0.) -> None:
        """
        Args:
            - actions_file_name (str) : The .csv action file name.
            - budget (int) : The budget, optional.
        """
        # Convert file
        self.file = CsvTranslator(actions_file_name)
        self.actions = self.file.convert_to_list()
        print(self.actions)
        # Exploit file
        self.num_actions = len(self.actions)
        self.num_decimals = self.count_decimals()
        # Convert action if num_decimals > 0:
        if self.num_decimals > 0:
            self.file = CsvTranslator(actions_file_name, self.num_decimals)
            self.actions = self.file.convert_to_list()
        # Initialization
        self.budget = budget * 10**self.num_decimals
        self.minimum_cost = minimum_cost * 10**self.num_decimals
        self.static_fees = static_fees * 10**self.num_decimals
        self.pourc_fees = pourc_fees / 100
        self.transactions = []

    def count_decimals(self) -> int:
        """
        Count the number of decimals after point.
        Optimizing the precision of Algorithm but multiply by ten
        the number of calculations per decimal.
        """
        list_count_decimals = [0]
        for action in self.actions:
            # Get number of decimals after point for price values
            if str(action[1]).split(".")[1] != '0':
                list_count_decimals.append(len(str(action[1]).split(".")[1]))
        max_decimals = max(list_count_decimals)
        return max_decimals

    def create_zeros_array(self) -> np.ndarray:
        """
        Create a null matrice with dimensions : (number action; self.budget)
        """
        list_zeros = [[0. for _ in range(self.budget+1)]
                      for _ in range(len(self.actions))]
        array = np.array(list_zeros)
        return array

    def mapping(self) -> np.ndarray:
        """
        First step of the resolution.

        Algorithm:
            1. Initialization
                a) Set a matrice of zeros with correct dims (dim1, dim2)
                b) Get the actions
                c) Define a counter "row" at 0
            2. For: a number (A) going from 0 to dim1*dim2
                a) Memorize A in another variable (B)
                b) Do A modulo dim2 ( A will be <= dim2 ) : A = money invest
                c) Set the cost value (C) for current 'row'

                If : A >= C
                (Meaning : Money invest >= Cost of action)
                    - Calculate the benefit
                    If : 'row' > 0:
                        - Get the value (D) at the row upside
                        - Get the cost of action
                        If : D > benefits + benefits of action upside without
                                        the cost of the current action added
                            - current benefit = D
                            ! Meaning that this current action is not worth it
                        Else:
                            - current benefit = benef + benefits action upside
                                                without cost of current action.
                            ! Meaning that this current action is worth it
                    Else:
                        - Set the first row with benefits of first action
                Else:
                    If 'row' > 0:
                        - Take the value upside
                    else:
                        - Make it to 0
                If col == 0 and var != 0:
                    row += 1

        Time complexity:
            variables :
                - budget_precision : 500.00€     ->  50000 operations
                - number_of_actions: 50 actions  ->  50 operations
            Number of operation :
                Number of operation = budget_precision * number_of_actions

                Since max(budget_precision) IN THIS CASE should be 50000:
                    It's constant
                Then:
                    Number of operation = Constant * number_of_actions
            Big-O :
                Time = O(number_of_actions)

        Space complexity:
            Array:
                array = [[0. for _ in range(budget)] for _ in range(actions)]
            Big-O :
                Space = O(number_of_actions)
        """
        array = self.create_zeros_array()
        actions = self.actions
        row = 0
        for col in range(0, array.size):
            var = col
            col = col % (array.shape[1])
            cost = int(float(actions[row][1]))
            if col >= cost:
                benefit = ((cost * float(actions[row][2]))
                           / ((10**self.num_decimals)))
                # To approach Sienna Logic
        
                #
                # Enter condition with static and pourc fees
                #
                if row > 0:
                    last_value = array[row - 1][col]
                    key = int(cost)
                    if last_value > (benefit + array[row - 1][col-key]):
                        array[row][col] = last_value
                    else:
                        if benefit > self.minimum_cost:
                            array[row][col] = benefit + array[row - 1][col-key]
                        else:
                            array[row][col] = last_value
                else:
                    array[row][col] = benefit
            else:
                if row > 0:
                    array[row][col] = array[row - 1][col]
                else:
                    array[row][col] = 0.
            if col == 0 and var != 0:
                row += 1
        print(array)
        return array

    def opt_transactions(self) -> list:
        """
        Second step of the resolution.

        To understand this process, check the docstring of the previous step.
        ( Section Algorithm and especially at '! Meaning' lines )

        Algorithm:
            1. Get the map for optimized way
            2. Get actions
            3. Set the column_point to the last value ( equivalent to [-1] )
            4. Set an empty list (A)
            5. For: index of actions for the end to the start
                a) If current pos > pos upside
                    - 'teleport' pos to : pos - cost value
                    - Append cost value to A list
                b) (Else:)
                    - Pass and check pos upside by passing index

        Time Complexity:
               Time = Time_mapping + O(number_of_actions)
            => Time = O(number_of_actions) + O(number_of_actions)
            => Time = O(number_of_actions)

        Space Complexity:
               Space = Space_mapping + O(number_of_actions)
            => Space = O(number_of_actions) + O(number_of_actions)
            => Space = O(number_of_actions)
        """
        trans_map = self.mapping()
        actions = self.actions
        col_point = trans_map.shape[1] - 1
        list_transactions = []
        for i in range(len(actions) - 1, -1, -1):
            if trans_map[i][col_point] > trans_map[i - 1][col_point]:
                col_point -= int(actions[i][1])
                list_transactions.append(actions[i])
            if i == 0 and col_point > 0:
                list_transactions.append(actions[i])

        # print(list_transactions)
        return list_transactions

    def decisions(self) -> dict:
        """
        With the list of transactions that optimized the investment, calculate:
            - benefits
            - costs
        Returns:
            dict :
                - "actions" (list): List of transactions
                - "cost" (int)    : Total cost
                - "benefit" (int) : Total benefit
        """
        cost = 0.
        benefits = 0.
        actions = self.opt_transactions()
        for action in actions:
            price = action[1]/(10**self.num_decimals)
            profit = action[2]/100

            cost += price
            benefits += price*profit
            self.transactions.append([action[0], price, action[2]])
            # self.transactions.append([action[0]])
        dict_decision = {
            "actions": self.transactions,
            "cost": round(cost, 2),
            "return": round(benefits, 2),
        }
        return dict_decision


def timer(func):
    """
    A little decorator function that give that execution time of a function.
    """
    def decorator(*args, **kwargs):
        """
        Print the difference of time between start and end of function's exec'.
        """
        time_a = time.time()
        result = func(*args, **kwargs)
        time_b = time.time()
        print(f"Duration : {round(time_b - time_a, 3)}s")
        return result
    return decorator


@timer
def take_decision(**kwargs):
    """Apply optimized strategy with setup arguments"""
    return Optimized(**kwargs).decisions()


def main(budget, minimum_cost, static_fees, pourc_fees) -> dict:
    """
    This function is called to apply optimized strategy with inputs.

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
    # budget = int(input("Give budget : "))
    file = input("Give name of csv file containing actions : ")
    # minimum_cost = float(input("Give minimum value of action to buy :"))
    # static_fees = float(input("Give static fees : "))
    # pourc_fees = float(input("Give pourcentage fees : "))
    dict_args = {
        "budget": budget,
        "actions_file_name": file,
        "minimum_cost": minimum_cost,
        "static_fees": static_fees,
        "pourc_fees": pourc_fees,
    }
    best_decision = take_decision(**dict_args)
    print(best_decision)
    return best_decision


if __name__ == '__main__':
    static = 0
    pourc = 0
    mini = 0
    result = main(
                    budget=5,
                    minimum_cost=mini,
                    static_fees=static,
                    pourc_fees=pourc
                 )
