# Std Libs:
import os


class CsvTranslator:
    """Converting CSV to a proper list
    """
    def __init__(self, csv_file_name):
        """Initialize the instance.

        Args:
            csv_file_name (str): Name of the csv file located at ../Product/
        """
        self.csv_file_name = csv_file_name
        self.translated_list = []

    def convert_to_list(self):
        """Convert CSV file to a list

        Returns:
            list: [[Action-name, price, profit], ...]
        """
        path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            os.pardir))
        folder = 'product'
        self.translated_list = []
        with open(
                f'{path}\\'
                f'{folder}\\'
                f'{self.csv_file_name}.csv', 'r') as csv_file:
            for line in csv_file:
                action = line.replace("\n", "")
                action = action.split(",")
                action[0] = str(action[0])
                try:
                    action[1] = int(action[1])
                    action[2] = int(action[2])
                except ValueError:
                    pass
                self.translated_list.append(action)
            # Delete 'name, price, profit' raw.
            self.translated_list.pop(0)
        return self.translated_list
