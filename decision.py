
from decision_tree_node import DecisionTreeNode
import random

class Decision (DecisionTreeNode):

    def __init__(self):
        super().__init()
        self.current_decision = False

    def make_decision(self):
        branch = self.get_branch()
        return branch.make_decision

class DecisionTree(DecisionTreeNode):

    def __init__(self):
        super(DecisionTree, self).__init__()
        self.left_child = None
        self.right_child = None

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

