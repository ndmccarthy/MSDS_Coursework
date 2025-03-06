# All Binary Search Trees

class myTreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None

    def nodeFamily(self):
        # Prints node information (key, parent, left child, and right child)
        print(f"Key: {self.key}")
        if self.parent is None:
            print ("    Parent: None")
        else: 
            print(f"    Parent: {self.parent.key}")
        if self.left is None:
            print("    Left: None")
        else:
            print(f"    Left: {self.left.key}")
        if self.right is None:
            print("    Right: None")
        else:
            print(f"    Right: {self.right.key}")

class BinarySearchTree:
    def __init__(self):
        self.root = None
    
    def insertNode(self, key):
        # key becomes root if root is None
        if self.root is None:
            self.root = myTreeNode(key)
            print(f"Key {self.root.key} was made the root node.")
            return
        # if root exists, determine if key already exists. NO DUPLICATES.
        search_results = self.iterativeTreeSearch(key)
        exists = search_results[0]
        if exists is True:
            print(f"Key {key} already exists in this tree.")
            return
        # if key does not already exist, create node and set parent from second position in search_results tuple.
        else:
            parent = search_results[1]
            node = myTreeNode(key)
            node.parent = parent
            # set as left or right child of parent, depending on comparison of keys
            if parent.key > key:
                parent.left = node
            else: 
                parent.right = node
        print(f"Key {key} was added with {parent.key} as its parent.")

    def iterativeTreeSearch(self, key):
        # returns a tuple
        # if key does not exist (False, parent node); if key exists (True, node)
        
        # check if tree is empty
        if self.root is None:
            print("Tree is empty.")
            return (False, None)

        # begin with current node at root
        current = self.root
        parent = None

        # if current node exists, check if key matches
        while current is not None:
            # if key matches, return True tuple
            if key == current.key:
                return (True, current)
            # if the key does not match, move the parent and current nodes down the tree accordingly
            parent = current
            if key < current.key:
                current = current.left
            else: 
                current = current.right
        # if current node does not exist, return the correct tuple
        return (False, parent)
    
    def treeHeight(self):
        # Create recursive helper function
        def _height(node):
            # Base case: if the node is None, return -1 (empty subtree)
            if node is None:
                return 0
            # Recursively compute the height of the left and right subtrees
            left_height = _height(node.left)
            right_height = _height(node.right)

            # The height of the current node is the maximum of the left/right heights +1
            return max(left_height, right_height) + 1
        return _height(self.root)

    def treeMinimum(self, node):
        # Finds leftmost node, which is the smallest key
        # Returns reference to a node, not just the key
        while node.left != None:
            node = node.left
        return node

    def transplant(self, node_removing=myTreeNode, child=myTreeNode):
        # replaces a node with one of its children, effectively removing the node
        # if the node being removed is the root, make the node's child the new root.
        if node_removing.parent == None:
            self.root = child
        # replace the node being removed with its child as the correct side (left/right) of it's parent.
        elif node_removing == node_removing.parent.left:
            node_removing.parent.left = child
        else:
            node_removing.parent.right = child
        # set the child's grandparent as its new parent.
        if child is not None:
            child.parent = node_removing.parent
    
    def deleteNode(self, key):
        # find node with key first
        (found, node_deleting) = self.iterativeTreeSearch(key)
        assert(found == True), f"key to be deleted:{key} does not exist in the tree"
        # if the node being deleted only has one child, replace it with it's existing child.
        if node_deleting.left == None:
            self.transplant(node_deleting, node_deleting.right)
        elif node_deleting.right == None:
            self.transplant(node_deleting,node_deleting.left)
        else: 
            # if the node has two children, find its successor (leftmost child of its right child).
            successor = self.treeMinimum(node_deleting.right)
            # if successor is not the child of the node being deleted, replace the node with it's right child.
            if successor.parent != node_deleting:
                self.transplant(successor, successor.right)
                # set successor as parent of the node's right child and vice versa
                successor.right = node_deleting.right
                successor.right.parent = successor
            # if successor is the child of the node being deleted, replace the node with it's left child and set relations.
            self.transplant(node_deleting, successor)
            successor.left = node_deleting.left
            successor.left.parent = successor
        print(f"Node {node_deleting.key} was successfully deleted from the tree.")

#-----------------------------------------------------------------------------
# Everything below is another construction method of binary search trees
#-----------------------------------------------------------------------------

class TreeNode:
    # Constructor for tree node
    def __init__(self, key, parent_node=None):
        self.key = key # set the key
        self.parent = parent_node # set the parent_node
        self.left = None # set the left child to None -- no left child to begin with
        self.right = None # set the right child to None - no right child to begin with.
        self.depth = 1
    
    def is_root(self):
        return self.parent == None
    
    # Function: insert
    # insert a node with key `new_key` into the current tree.
    def insert(self, new_key):
        key = self.key 
        if new_key == key:
            print(f'Already inserted key {key}. Ignoring')
        elif new_key < key: # new_key must go into the left subtree
            if self.left == None: # no left child?
                new_node = TreeNode(new_key, self) # create one with self as parent
                self.left = new_node # set the left pointer
            else:
                self.left.insert(new_key) # recursively call insert on left subtree
        else:  # new_key must go into the right subtree.
            assert new_key > key
            if self.right == None: # no right child?
                new_node = TreeNode(new_key, self) # create one
                self.right = new_node
            else: 
                self.right.insert(new_key) # recusively call insert on right subtree.
        #update the depth
        left_depth = self.left.depth if self.left != None else 0
        right_depth = self.right.depth if self.right != None else 0
        self.depth = max(left_depth, right_depth) + 1

def depthWiseTraverse(root_node=TreeNode):
    # returns a list of nodes in order of their height from largest to smallest (root, ..., furthest depth nodes)
    # create priority queue for visiting nodes and finding children
    pq = [root_node]
    # initialize the list of results
    results = []
    # visit a node in the queue
    for node in pq:
        # add its children to the queue
        if node.left:
            pq.append(node.left)
        if node.right:
            pq.append(node.right)
        # add its key to the list of results
        results.append(node.key)
    return results

def sumOfBranches(root_node):
    # returns a list of sums of each branch of the tree; begins at root and sums every node to a leaf (no children)
    # initialize a results list
    sums = []
    # visit every node along the left side, then visit the right child down the left side, etc. (recursively)
    # create visit function that stores node and current sum
    def currentBranchSum(node, sum):
        # add parent sum to value of current key
        current_sum = sum + node.key
        # check if left child and visit
        if node.left:
            currentBranchSum(node.left, current_sum)
        # if no left child, check if right child and visit
        if node.right:
            currentBranchSum(node.right, current_sum)
        # if no children, add sum to results list and return to parent node
        if not node.left and not node.right:
            sums.append(current_sum)
    currentBranchSum(root_node, 0)
    return sums

def getLongestPathLength(root):
    return root.depth + 1
        # Create recursive helper function
        #def _height(node):
        #    # Base case: if the node is None, return -1 (empty subtree)
        #    if node is None:
        #        return 1
        #    # Recursively compute the height of the left and right subtrees
        #    left_height = _height(node.left)
        #    right_height = _height(node.right)
#
        #    # The height of the current node is the maximum of the left/right heights +1
        #    return max(left_height, right_height) + 1
        #return _height(root)