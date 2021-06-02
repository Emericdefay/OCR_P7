# Std Libs:
import math
from sys import stdout
# External Libs:
import numpy as np
# Local Libs:
from csv_translator import CsvTranslator


class Optimized:
    """

    """
    def __init__(self, actions_file_name: str) -> None:
        """ """
        self.actions = CsvTranslator(actions_file_name).convert_to_list()
        self.num_actions = len(self.actions)
        self.transactions = []
        self.best_benefits = 0
        self.budget = 500
        self.num_decimals = 0
    
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
            cost = int(float(actions[row][1]) * 10**self.num_decimals)
            if col*10**self.num_decimals >= cost:
                benefit = (cost * float(actions[row][2])) / (100*10**self.num_decimals)
                if row > 0:
                    try:
                        last_value = array[row - 1][col]
                        key = int(cost * 10**self.num_decimals)
                        if last_value > (benefit + array[row - 1][col-key]):
                            array[row][col] = last_value
                        else:
                            array[row][col] = benefit + array[row - 1][col-key]
                    except IndexError:
                        array[row][col] = benefit
                        pass
                else:
                    array[row][col] = benefit
            else:
                if row > 0:
                    array[row][col] = array[row - 1][col]
                else:
                    array[row][col] = 0
            if col == 0 and var != 0:
                row += 1
        print(array)
        return array

    def opt_transactions(self) -> list:
        """ """
        trans_map = self.mapping()
        actions = self.actions
        col_point = trans_map.shape[1] - 1
        list_transactions = []
        for i in range(len(actions) - 1, 0, -1):
            if trans_map[i][col_point] > trans_map[i - 1][col_point]:
                col_point -= int(float(actions[i][1]))
                list_transactions.append(actions[i])
        print(list_transactions)
        return list_transactions

    def decisions(self) -> None:
        """ """
        cost = 0
        profit = 0
        actions = self.opt_transactions()
        for action in actions:
            cost += action[1]
            profit += action[1] * action[2]/100
        print("Emeric bought :\n")
        for action in actions:
            print(action[0])
        print(f"\nTotal cost : {cost}€")
        print(f"Total return : {round(profit, 2)}€")

            
            

a = Optimized("actions").decisions()