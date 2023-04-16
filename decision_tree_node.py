# Node class for decision tree
# Author: Chris Branton
# Created: 2023-04-01
# Adapted from AI for Games by Ian Millington

class TreeNode:

    def __init__(self):

        self.child_nodes = []

class BinaryTreeNode(TreeNode):

    def __init__(self):
        super(BinaryTreeNode, self).__init__()

    @property
    def left_child(self):
        return self.child_nodes[0]

    @property
    def right_child(self):
        return self.child_nodes[1]

class DecisionTreeNode(TreeNode):

    def __init__(self):
        self.test_value = None
        self.action = None
        self.test_attribute = None
        self.child_nodes = {}


    # Recursively walk through the tree
    def make_decision (self):
        pass

    def add_child(self, node, value):
        if value == True:
            left_child = node
        else:
            right_child = node