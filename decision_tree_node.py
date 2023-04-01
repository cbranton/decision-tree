# Node class for decision tree
# Author: Chris Branton
# Created: 2023-04-01
# Adapted from AI for Games by Ian Millington

class TreeNode:

    def __init__(self):
        self.children = []

class BinaryTreeNode(TreeNode):

    def __init__(self):
        super(BinaryTreeNode, self).__init__()

    @property
    def left_child(self):
        return self.children[0]

    @property
    def right_child(self):
        return self.children[1]

class DecisionTreeNode(BinaryTreeNode):

    # Recursively walk through the tree
    def make_decision (self):
        pass