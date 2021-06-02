# Std Libs:

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
    
    def create_zeros_array(self) -> np.ndarray:
        """ """
        list_zeros = [[0. for _ in range(self.budget+1)] for _ in range(len(self.actions))]
        array = np.array(list_zeros)
        return array

    def mapping(self) -> None:
        """ """
        array = self.create_zeros_array()
        actions = self.actions
        row = 0
        for col in range(array.size):
            var = col
            col = col%(array.shape[1])
            cost = actions[row][1]
            if col >= cost:
                benefit = float(cost * (actions[row][2]/100))
                #benefit = actions[row][2]
                if row > 0:
                    try:
                        last_value = array[row-1][col]
                        if last_value > (benefit + array[row-1][col-cost]):
                            array[row][col] = last_value
                        else:
                            array[row][col] = benefit + array[row-1][col-cost]
                    except IndexError:
                        array[row][col] = benefit
                        pass
                else:
                    array[row][col] = benefit
            else:
                if row > 0:
                    array[row][col] = array[row-1][col]
                else:
                    array[row][col] = 0

            if col == 0 and var != 0:
                row += 1
        print(array)
        return array

    def defined_way(self, map):
        """"""

    def opt_transactions(self):
        """ """
        trans_map = self.mapping()
        actions = self.actions



            
            

a = Optimized("actions").mapping()