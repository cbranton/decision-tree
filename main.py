import copy
import csv
import math
from collections import defaultdict

from decision_tree_node import DecisionTreeNode

class DecisionTreeApp:

    def entropy(self, observations):
        ent = 0
        example_count = len(observations)

        if example_count > 0:
            # keep track of how many action types we have
            action_tallies = {'0': 0, "1": 0}
            for example in observations:
                # todo: fix hard-coded action/answer
                action_tallies[example["survived"]] += 1

        action_count = len(action_tallies)
        if action_count > 0:
            ent = 0
            for action_tally in action_tallies:
                proportion = action_tally / example_count
                ent -= proportion * math.log2(proportion)

            # return total entropy
            return ent

    def split_by_attribute(self, observations, attribute):
        sets = defaultdict(list)
        for observation in observations:
            value = observations[attribute]
            sets[value].append(observation)
        return sets

    # Determines the entropy of a list of lists
    def entropy_of_sets(self, set_list, observation_count):
        ent = 0
        for set in set_list:
            proportion = len(set) / observation_count

            ent -= proportion * self.entropy(set)

        # return the total entropy
        return ent


    def build_tree(self, examples, attribute_list, decision_node):
        # calculate initial entropy
        initial_entropy = self.entropy(examples)

        if initial_entropy == 0:
            return

        example_count= len(examples)
        best_information_gain = 0
        best_split_attribute = None
        best_sets = []

        # try each attribute
        for attribute in attribute_list:
            sets = self.split_by_attribute(examples, attribute)

            # find overall entropy and information gain
            overall_entropy = self.entropy_of_sets(sets, example_count)
            information_gain = initial_entropy = overall_entropy

            if information_gain > best_information_gain:
                best_information_gain = information_gain
                best_split_attribute = attribute
                best_sets = sets

        decision_node.test_value = best_split_attribute
        new_attributes = copy.deepcopy(attribute_list)
        new_attributes.remove(best_split_attribute)

        # fill the child nodes
        for set in best_sets:
            # find the value for the attribute in this set
            attribute_value = set[0].get_value(best_split_attribute)

            # does this go outside the loop?
            child = DecisionTreeNode()
            decision_node.add_child(child, attribute_value)

            # recurse
            self.build_tree(examples, new_attributes, child)

    def read_csv(self, file_name):
        self.data = []
        with open(file_name)as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                print (row)
                self.data.append(row)
        self.attributes = self.data[0].keys()
        print(self.attributes)

        csv_file.close()

def main():
    dta = DecisionTreeApp()
    print ("Reading training data")
    dta.read_csv("titanic_train.csv")
    print("Creating tree")
    root_node = DecisionTreeNode()
    tree = dta.build_tree(dta.data, dta.attributes, root_node)
    print ("Testing the tree")
    print ("All done")



if __name__ == "__main__":
    main()