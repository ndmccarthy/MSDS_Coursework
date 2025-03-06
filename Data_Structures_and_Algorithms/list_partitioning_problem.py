"""
In this problem, you are given a list of numbers l: [l[0], ..., l[n-1]]. 
Your goal is to partition this into two lists l1, l2 such that each element l[i] belongs to exactly one of l1, l2
The difference between the sums of the two lists is minimized: min |sum(𝚕𝟷)−sum(𝚕𝟸)|
    where  sum(𝚕) for a list  𝑙 denotes the sum of the elements in a list.
"""

class DecisionNode:
    def __init__(self, elt, parent, lchild: bool):
        # previous decisions are reflected in the parentage
        # elt = the current element from the original list that is being considered for placement
        self.parent = parent
        if parent == None: # creating root node
            # self.l1_sum and self.l2_sum store the current summations l1 and l2, respectively
            self.l1_sum = 0
            self.l2_sum = 0
            # self.level keeps track of the id number of the elt
            self.level = 0
        else:
            self.l1_sum = parent.l1_sum
            self.l2_sum = parent.l2_sum
            self.level = parent.level + 1
        if lchild:
            self.l1_sum += elt
        else:
            self.l2_sum += elt
        # the key of the node is the absolute sum difference between l1 and l2, which we are trying to minimize
        self.key = abs(self.l1_sum - self.l2_sum)
        # initialize pointers for children
        self.left = None
        self.right = None

    def __repr__(self):
        return f"(Level: {self.level}, Diff: {self.key})"
    
    def makeBabies(self, elt):
        left = DecisionNode(elt, self, True)
        right = DecisionNode(elt, self, False)
        self.left = left
        self.right = right
        return (left, right)


def memoizePartition(lst:list):
# create memo table in form of decision tree
    # start with root; root is first decision to put ii = 0 into l1
    root = DecisionNode(lst[0], None, True)
    # keep track of nodes at last level 
    possibilities = {}
    # initialize queue of nodes to process
    q = [root]
    while len(q) > 0:
        current_node = q[0]
        ii = current_node.level
        if ii < len(lst) - 1:
            elt = lst[ii+1]
            left, right = current_node.makeBabies(elt)
            if left.level == len(lst) - 1:
                possibilities[left.key] = left
                possibilities[right.key] = right
            else:
                q.append(left)
                q.append(right)
        q.pop(0)
    result = min(possibilities.keys())
    final_node = possibilities[result]
    return final_node
    
def computeBestPartition(lst: list):
    n = len(lst)
    assert n >= 1
    assert all(elt >= 1 and elt== int(elt) for elt in lst)
    l1 = [lst[0]] # the first element of the original list is automatically put into l1
    l2 = []
    final_node = memoizePartition(lst)
    ii = final_node.level
    current_node = final_node
    while ii > 0:
        if current_node == current_node.parent.left:
            l1.append(lst[ii])
        else:
            l2.append(lst[ii])
        current_node = current_node.parent
        ii -= 1
    return (l1, l2)