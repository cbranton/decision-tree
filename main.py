# Code for decision tree demo application
# @author: Chris Branton
# @created: 2018-04-15
# @updated: 2023-04-16. Made some improvements in consistency,
#   readability, and structure.

import csv

from decision import DecisionTree


class DecisionTreeApp:

    TRAINING_FILE_NAME = "titanic_train.csv"
    TESTING_FILE_NAME = "titanic_test.csv"
    ACTION_ATTRIBUTE = "survived"

    def __init__(self):
        self.test_set = []
        self.data = []
        self.attributes = []
        self.decision_tree = None

    def load_training_data(self, file_name):
        self.data = []
        self.read_file(file_name, self.data)
        self.attributes = list(self.data[0].keys())

    def train(self):
        self.load_training_data (self.TRAINING_FILE_NAME)
        self.decision_tree = DecisionTree()
        self.decision_tree.train(self.data, self.attributes, self.ACTION_ATTRIBUTE)

    def test(self):
        self.read_file(self.TESTING_FILE_NAME, self.test_set)
        accuracy = self.decision_tree.test(self.test_set, self.attributes)
        print ("Test complete.")
        print (str(accuracy), "percent correctly classified.")

    # read the comma-separated data file and store the contents
    # file_name is a string with valid path to the file
    # data_list is a list that will contain a dictionary in each entry
    def read_file(self, file_name, data_list):
        print ("Reading File", file_name)
        with open(file_name) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # print (row)
                data_list.append(row)


# Simple app to demonstrate decision tree
def main():
    print ("Reading training data")
    dta = DecisionTreeApp()

    print("Creating tree")
    dta.train()

    print ("Testing the tree")
    dta.test()
    print ("All done")


# if this is the main file, run main()
if __name__ == "__main__":
    main()