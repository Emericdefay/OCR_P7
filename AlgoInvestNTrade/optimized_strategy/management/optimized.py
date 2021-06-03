# Std Libs:
import time
from typing import Optional
# External Libs:
import numpy as np
# Local Libs:
from csv_translator import CsvTranslator


class Optimized:
    """

    """
    def __init__(self,
                 actions_file_name: str,
                 budget: Optional[int] = 500) -> None:
        """ """
        # Convert file
        self.file = CsvTranslator(actions_file_name)
        self.actions = self.file.convert_to_list()
        # Exploit file
        self.num_actions = len(self.actions)
        self.num_decimals = self.count_decimals()
        # Convert action if num_decimals > 0:
        if self.num_decimals > 0:
            self.file = CsvTranslator(actions_file_name, self.num_decimals)
            self.actions = self.file.convert_to_list()
        # Initialization
        self.budget = budget * 10**self.num_decimals
        self.transactions = []

    def count_decimals(self) -> int:
        """ """
        list_count_decimals = [0]
        for action in self.actions:
            # Get number of decimals after point for price values
            if str(action[1]).split(".")[1] != '0':
                list_count_decimals.append(len(str(action[1]).split(".")[1]))
        max_decimals = max(list_count_decimals)
        return max_decimals

    def create_zeros_array(self) -> np.ndarray:
        """ """
        size = self.budget + 1
        list_zeros = [[0. for _ in range(1, size)]
                      for _ in range(len(self.actions))]
        array = np.array(list_zeros)
        return array

    def mapping(self) -> np.ndarray:
        """ """
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

                if row > 0:
                    try:
                        last_value = array[row - 1][col]
                        # key = int(cost * 10**self.num_decimals)
                        key = int(cost)
                        if last_value > (benefit + array[row - 1][col-key]):
                            array[row][col] = last_value
                        else:
                            array[row][col] = benefit + array[row - 1][col-key]
                    except IndexError:
                        array[row][col] = benefit
                        raise
                else:
                    array[row][col] = benefit
            else:
                if row > 0:
                    array[row][col] = array[row - 1][col]
                else:
                    array[row][col] = 0
            if col == 0 and var != 0:
                row += 1
        # print(array)
        return array

    def opt_transactions(self) -> list:
        """ """
        trans_map = self.mapping()
        actions = self.actions
        col_point = trans_map.shape[1] - 1
        list_transactions = []
        for i in range(len(actions) - 1, 0, -1):
            if trans_map[i][col_point] > trans_map[i - 1][col_point]:
                col_point -= int(actions[i][1])
                list_transactions.append(actions[i])
        # print(list_transactions)
        return list_transactions

    def decisions(self) -> dict:
        """ """
        cost = 0
        benefits = 0
        actions = self.opt_transactions()
        for action in actions:
            price = action[1]/(10**self.num_decimals)
            profit = action[2]/100
            cost += price
            benefits += price*profit
            # self.transactions.append([action[0], price, profit])
            self.transactions.append([action[0]])
        dict_decision = {
            "actions": self.transactions,
            "cost": round(cost, 2),
            "return": round(benefits, 2),
        }
        return dict_decision


def timer(func):
    """ """
    def decorator(*args, **kwargs):
        """ """
        time_a = time.time()
        result = func(*args, **kwargs)
        time_b = time.time()
        print(f"Duration : {round(time_b - time_a, 3)}s")
        return result
    return decorator


@timer
def take_decision(**kwargs):
    """ """
    return Optimized(**kwargs).decisions()


def main():
    """ """
    budget = int(input("Give budget : "))
    file = input("Give name of csv file containing actions : ")
    dict_args = {
        "budget": budget,
        "actions_file_name": file,
    }
    best_decision = take_decision(**dict_args)
    print(best_decision)


if __name__ == '__main__':
    main()
