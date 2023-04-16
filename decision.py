# Decision tree implementation
# @author: Chris Branton
# @created: 2018-04-15

import random
#import copy
import math

from decision_tree_node import DecisionTreeNode


# Not actually a multiset, but a dictionary of lists.
# Built to hold the elements of each attribute value
class MultiSet():

    def __init__(self):
        self.bag = {}

    def add(self, key, element):
        if key not in self.bag.keys():
            self.bag[key] = []
        self.bag[key].append(element)

    def values(self):
        return self.bag.values()


class Decision (DecisionTreeNode):

    def __init__(self):
        super().__init__()
        self.current_decision = False

    def make_decision(self):
        branch = self.get_branch()
        return branch.make_decision

class RandomDecision(Decision):

    def __init__(self):
        super().__init__()
        self.last_frame = -1

    def test_value(self):
        frame = self.get_current_frame()
        self.current_decision = False
        if frame > self.last_frame + 1:
            # get a random Boolean
            self.current_decision = random.choice([True,False])

        self.last_frame = frame
        return self.current_decision


class DecisionTree(DecisionTreeNode):

    def __init__(self):
        super(DecisionTree, self).__init__()
        self.action_attribute = None
#        self.left_child = None
#        self.right_child = None

    # Create a decision tree
    def train(self, training_set, attributes, action_attribute):
        print ("Training...")
        # Indirection allows us to shield caller from DecisionNode details
        # training_set is an ordered dictionary.
        # attributes is a list of training_set keys.
        self.action_attribute = action_attribute
        attributes.remove(action_attribute)
        self.make_tree(training_set, attributes, self)
        print ("Training complete")
        self.print()

    # Test the tree using a data set
    def test(self, test_set, attributes):
        correct = 0
        incorrect = 0
        set_size = len(test_set)
        print("Testing", set_size, "examples")

        for example in test_set:
            actual_result = example[self.action_attribute]
            predicted_result = self.predict(example)

            if predicted_result == actual_result:
                correct += 1
            else:
                incorrect += 1

        percent = correct / set_size * 100
        print(percent, " percent correct. ", set_size, "records tested.")
        return percent

    # Recursively build the tree based on maximum information gain
    def make_tree(self, examples, attributes, decision_node):
        # Calculate initial entropy
        initial_entropy = self.entropy(examples)

        # if entropy is 0, nothing else to do
        # let's talk about single points of entry and exit in class
        if initial_entropy > 0.0 and len(attributes) > 0:
            example_count = len(examples)

            # keep the best result
            best_information_gain = 0
            best_split_attribute = None
            best_sets = None

            # calculate information gain for each attribute
            for attr in attributes:  # attr is a key from the examples dict
                # sets will give me a dictionary: keys are values for attr;
                # values are lists of examples with that value for attr
                sets = self.split_by_attribute(examples, attr)
                overall_entropy = self.entropy_of_sets(sets, example_count)
                information_gain = initial_entropy - overall_entropy

                # if this one is better, keep it
                if information_gain > best_information_gain:
                    best_information_gain = information_gain
                    best_split_attribute = attr
                    best_sets = sets

            # set the decision node to this attribute
            decision_node.test_attribute = best_split_attribute
            print("Splitting on", best_split_attribute)

            if best_split_attribute == None:
                print("What the what?")
                return

            # remove the best attribute from the set we will pass down the tree
            #            new_attributes = deepcopy(attributes)
            new_attributes = list(attributes)
            new_attributes.remove(best_split_attribute)

            # create the child nodes
            # each node should action = attr and
            # test_value = val
            for val, this_set in best_sets.bag.items():
                print("Create child node for set " + val)
                child = DecisionTreeNode()
                attribute_value = val  # set[best_split_attribute]
                child.test_value = val
                decision_node.child_nodes[val] = child

                # recurse with child node
                self.make_tree(this_set, new_attributes, child)

        else:  # We are at a leaf
            decision_node.action = self.get_action(examples)
            if not decision_node.action:
                print("Something is wrong")

    # Calculate the information entropy of an example set
    def entropy(self, examples):
        example_count = len(examples)
        actionTallies = {}

        if example_count == 0:
            return 0

        for example in examples:
            if example[self.action_attribute] in actionTallies.keys():
                actionTallies[example[self.action_attribute]] += 1
            else:
                actionTallies[example[self.action_attribute]] = 1

        actionCount = len(actionTallies.keys())

        if actionCount <= 1:
            return 0

        entropy = 0

        # Add in the contribution to entropy of each action
        for action, number in actionTallies.items():
            proportion = number / example_count
            entropy -= proportion * math.log(proportion, 2)
        return entropy

    # Divide a set of examples based on an attribute value
    def split_by_attribute(self, examples, attribute):
        # print ("Splitting on " + attribute)
        # We create a set of lists, so we can access each list
        # by the attribute value
        sets = MultiSet()
        # Loop through each example
        for example in examples:
            # Assign it to the right set
            # example[attribute].value #is the attribute value to add to the set
            sets.add(example[attribute], example)
        # Return the sets
        return sets

    # Find the entropy of a list of sets
    def entropy_of_sets(self, sets, count):
        value = 0

        for set in sets.values():
            proportion = len(set) / count
            set_entropy = self.entropy(set)
            value -= proportion * set_entropy
        return value


    def predict(self, example):
        current_node = self
        next_node = None
        action = current_node.action

        while not action:
            test_attr = current_node.test_attribute
            try:
                ex_value = example[test_attr]
                if not ex_value in  current_node.child_nodes.keys():
                    return action
                next_node = current_node.child_nodes[ex_value]
            except KeyError:
                print ("KeyError on", test_attr)

            current_node = next_node
            action = current_node.action
        return action

    def get_action(self, examples):
        example_count = len(examples)
        action_tallies = {}
        if example_count == 0:
            return None

        for example in examples:
            if example[self.action_attribute] in action_tallies.keys() :
                action_tallies[example[self.action_attribute]] += 1
            else:
                action_tallies[example[self.action_attribute]] = 1

        action_count = len(action_tallies.keys())

        best_action = None
        high_count = 0
        for action, sum in action_tallies.items():
            if sum > high_count:
                high_count = sum
                best_action = action

        return best_action

    def print(self):
        print ("Printing decision tree")
        node = self
        self.printNode(node)

    def printNode(self, node):
        print (node.test_attribute, ":", node.test_value)
        if len(node.child_nodes) > 0:
            for val, child in node.child_nodes.items():
                self.printNode (child)


