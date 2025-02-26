'''
Heaps

Heaps are an array object that can be viewed as a nearly complete binary tree
Their main properties are as follows:
    1. Element i is the parent of 2i (left child) and 2i+1 (right child).
        a. If an element doesn't exist, then i doesn't have that child.
        b. For element j, j//2 is the parent.
        c. A[0] has no parent and is the root.
        d. If a node has a right child, it must have a left child.
    2. Min-Heap Property: Every parent must be <= the value of its children.
        a. Max-Heap Property is just the reverse.
        b. A[0] is the minimum element in a minheap.
'''
from helper_functions import is_even, comparison
from graphs_classes import Vertex

def bubble_up(heap:list, maxheap:bool, child_index:int):
    child_value = heap[child_index]
    # find parent index and value
    if is_even(child_index):
        # child is the right of its parent
        parent_index = (child_index - 1)//2
    else:
        # child is the left of its parent
        parent_index = child_index//2
    parent_value = heap[parent_index]
    # determine comparator based on heap type (max/min)
    if maxheap:
        comp = 'greater than'
    else:
        comp = 'less than'
    # bubble up unless already in position 0
    if child_index > 0:
        if comparison(comp, child_value, parent_value):
            # not sure why but usual reference to values in next line didn't work so wrote out.
            heap[parent_index], heap[child_index] = heap[child_index], heap[parent_index]
            bubble_up(heap, maxheap, parent_index)
    
def bubble_down(heap:list, maxheap:bool, parent_index:int):
    lchild_index = 2*parent_index + 1
    rchild_index = lchild_index + 1
    parent_value = heap[parent_index]
    last_index = len(heap) - 1
    # set up correct comparators depending on heap type (min/max)
    if maxheap:
        comp = 'less than'
    else:
        comp = 'greater than'
    # parent has no children
    if lchild_index > last_index:
        return
    lchild_value = heap[lchild_index]
    # parent only has left child
    if lchild_index <= last_index and rchild_index > last_index:
        rchild_value = float('inf')
    # parent has both children
    else:
        rchild_value = heap[rchild_index]
    # determine if swap is necessary
    small = min(lchild_value, rchild_value)
    small_index = heap.index(small)
    if comparison(comp, parent_value, small):
        heap[parent_index], heap[small_index] = heap[small_index], heap[parent_index]
        bubble_down(heap, maxheap, small_index)


class MinHeap:
    def __init__(self):
        self.minheap = [None]
 
    def size(self):
        return len(self.minheap)
    
    def __repr__(self):
        return str(self.minheap)
        
    def satisfies_assertions(self):
        for ii in range(len(self.minheap)-1):
            if self.minheap[ii] > self.minheap[ii//2] or self.minheap[ii] > self.minheap[(ii//2)+1]:
                return False
        return True
    
    def min_element(self):
        if self.size() != 0:
            return self.minheap[0]
        else:
            return None

    def insert(self, elt):
        self.minheap.append(elt)
        if self.minheap[0] == None:
            self.minheap.pop(0)
        end = len(self.minheap)-1
        if end > 0:
            bubble_up(self.minheap, False, end)
    
    def delete_min(self):
        # deletes the smallest element in the heap
        self.minheap.pop(0)
        if self.size() != 0:
            min_elt = min(self.minheap)
            if self.minheap[0] != min_elt:
                min_index = self.minheap.index(min_elt)
                bubble_up(self.minheap, False, min_index)

class TopKHeap:
    # This is a part of the coding project. 
    # It is meant to be a data structure with 1-k elements in sorted array A and n-k elements in minheap H.
    # All elements in the sorted array must be smaller than the elements in the minheap.
    # "k" has been replaced with "size" in this implementation to make reading and searching the code easier.

    # The constructor of the class to initialize an empty data structure
    def __init__(self, size):
        self.sizek = size
        self.Array = []
        self.TopHeap = MinHeap()
        
    def size(self): 
        return len(self.Array) + (self.TopHeap.size)
    
    def get_jth_element(self, j):
        # returns jth element in self.Array
        assert 0 <= j < self.sizek-1
        assert j < self.sizek()
        return self.Array[j]
    
    def satisfies_assertions(self):
        # is self.Array sorted
        for i in range(len(self.Array) -1 ):
            assert self.Array[i] <= self.Array[i+1], f'Array A fails to be sorted at position {i}, {self.Array[i], self.Array[i+1]}'
        # is self.TopHeap a heap (check min-heap property)
        self.TopHeap.satisfies_assertions()
        # is every element of self.Array less than or equal to each element of self.TopHeap
        for i in range(len(self.Array)):
            assert self.Array[i] <= self.TopHeap.min_element(), f'Array element A[{i}] = {self.Array[i]} is larger than min heap element {self.TopHeap.min_element()}'
        
    # Function : insert_into_A
    def insert_into_A(self, elt):
        # This is a helper function that inserts an element `elt` into `self.Array`.
        print("k = ", self.sizek)
        
        # whenever size is < k, append elt to the end of the array A
        size = len(self.Array)
        assert(size < self.sizek), "Array does not have enough spots to insert new element."
        self.Array.append(elt)

        # Move the element that you just added at the very end of array A out into its proper place so that the array A is sorted.
        j = len(self.Array)-1
        while (j >= 1 and self.Array[j] < self.Array[j-1]):
            # Swap A[j] and A[j-1]
            (self.Array[j], self.Array[j-1]) = (self.Array[j-1], self.Array[j])
            # return the "displaced last element" jHat (None if no element was displaced)
            j = j -1 
        return
    
    # Function: insert -- insert an element into the data structure.
    def insert(self, elt):
        size = len(self.Array)
        # If we have fewer elements than the self.sizek, handle that in a special manner
        if size < self.sizek:
            self.insert_into_A(elt)
            return
        # determine whether elt belongs in the Array or Heap based on its value and that of the largest element in the Array.
        array_max_id = self.sizek - 1
        max_in_array = self.Array[array_max_id]
        if elt >= max_in_array:
            self.TopHeap.minheap.insert(elt)
        else:
            # move the maximum item from self.Array (which must have exactly k elements) to self.TopHeap to make room for elt
            self.TopHeap.insert(max_in_array)
            self.Array.pop(array_max_id)
            self.insert_into_A(elt)
        
    # Function: Delete top k -- delete an element from the array A
    # In particular delete the j^{th} element where j = 0 means the least element.
    # j must be in range 0 to self.sizek-1
    def delete_top_k(self, j):
        size = len(self.Array)
        assert self.sizek >= size # we need not handle the case when size is less than or equal to size
        assert j >= 0
        assert j < self.sizek
        # delete j from Array
        self.Array.pop(j)
        # insert the smallest element from Heap into the Array to keep the correct array size; delete this element from the heap
        heap_min = self.TopHeap.min_element()
        self.Array.append(heap_min)
        self.TopHeap.delete_min()
        # fix issues in minHeap, if any
        heap_size = self.TopHeap.size()
        parent_index = 0
        last_parent_index = (heap_size-2)//2
        while parent_index < last_parent_index:
            # checking indices with both children
            parent_value = self.TopHeap.minheap[parent_index]
            lchild_index = (2*parent_index)+1
            lchild_value = self.TopHeap.minheap[lchild_index]
            rchild_index = lchild_index + 1
            rchild_value = self.TopHeap.minheap[rchild_index]
            if parent_value > min(lchild_value, rchild_value):
                bubble_down(self.TopHeap.minheap, False, parent_index)
            parent_index += 1
        # checking last_parent
        last_parent_value = self.TopHeap.minheap[last_parent_index]
        lchild_index = (2*last_parent_index)+1
        lchild_value = self.TopHeap.minheap[lchild_index]
        # when last_parent_index is even, it only has a left child
        if is_even(heap_size):
            # set rchild_value to infinity so parent value only compares with left child value.
            rchild_value = float('inf')
        else:
            rchild_index = lchild_index + 1
            rchild_value = self.TopHeap.minheap[rchild_index]
        if last_parent_value > min(lchild_value, rchild_value):
            bubble_down(self.TopHeap.minheap, False, parent_index)

class MaxHeap:
    def __init__(self):
        self.maxheap = [None]
        
    def size(self):
        return len(self.maxheap)
    
    def __repr__(self):
        return str(self.maxheap)
        
    def satisfies_assertions(self):
        for ii in range(len(self.maxheap)-1):
            if self.maxheap[ii] < self.maxheap[ii//2] or self.maxheap[ii] < self.maxheap[(ii//2)+1]:
                return False
        return True
    
    def max_element(self):
        if self.size() != 0:
            return self.maxheap[0]
        else:
            return None
    
    def insert(self, elt):
        self.maxheap.append(elt)
        if self.maxheap[0] == None:
            self.maxheap.pop(0)
        end = len(self.maxheap)-1
        if end > 0:
            bubble_up(self.maxheap, True, end)
        
    def delete_max(self):
        # delete the largest element in the heap
        self.maxheap.pop(0)
        if self.size() != 0:
            max_elt = max(self.maxheap)
            if self.maxheap[0] != max_elt:
                max_index = self.maxheap.index(max_elt)
                bubble_up(self.maxheap, True, max_index)


class MedianMaintainingHeap:
    def __init__(self):
        self.hmin = MinHeap()
        self.hmax = MaxHeap()
        
    def satisfies_assertions(self):
        s_min = self.hmin.size()
        s_max = self.hmax.size()
        if s_min == 0 or s_max == 0:
            return
        # 1. min heap min element >= max heap max element
        if self.hmax.max_element() != None:
            assert self.hmax.max_element() <= self.hmin.min_element(), f'Failed: Max element of max heap = {self.hmax.max_element()} > min element of min heap {self.hmin.min_element()}'
        # 2. size of max heap must be equal or one less than min heap.
        assert (s_min == s_max or s_max  == s_min -1 ), f'Heap sizes are unbalanced. Min heap size = {s_min} and Maxheap size = {s_max}'
    
    def __repr__(self):
        return 'Maxheap:' + str(self.hmax) + ' Minheap:' + str(self.hmin)
    
    def get_median(self):
        if self.hmin.size() == 0:
            assert self.hmax.size() == 0, 'Sizes are not balanced'
            assert False, 'Cannot ask for median from empty heaps'
        if self.hmax.size() == 0:
            assert self.hmin.size() == 1, 'Sizes are not balanced'
            return self.hmin.min_element()
        min_elt = self.hmin.min_element()
        max_elt = self.hmax.max_element()
        if self.hmin.size() == self.hmax.size() and max_elt != None:
            median = (min_elt + max_elt)/2
        else:
            median = min_elt
        return median
        
    def balance_heap_sizes(self):
        # This function could be called from insert/delete_median methods
        # hmin must be equal to or 1 element greater than hmax
        min_elt = self.hmin.min_element()
        max_elt = self.hmax.max_element()
        # deal with case that hmax is still empty
        if max_elt == None:
            self.hmax.maxheap.pop(0)
        # hdiff should only be able to return -1, 0, 1, 2, since the heaps are balanced in every insertion and deletion
        hmin_size = self.hmin.size()
        hmax_size = self.hmax.size()
        hdiff = hmin_size - hmax_size
        if hdiff == 0 or hdiff == 1:
            return
        elif hdiff == 2:
            self.hmax.insert(min_elt)
            self.hmin.delete_min()
        elif hdiff == -1:
            self.hmin.insert(max_elt)
            self.hmax.delete_max()
    
    def insert(self, elt):
        # Handle the case when either heap is empty
        # hmin must be equal to or 1 element greater than hmax
        min_elt = self.hmin.min_element()
        # min heap is empty -- remove None holder and directly insert into min heap
        if min_elt == None:
            self.hmin.minheap.pop(0)
            self.hmin.insert(elt)
            return 
        if elt >= min_elt:
            self.hmin.insert(elt)
        else:
            self.hmax.insert(elt)
        self.balance_heap_sizes()

    def delete_median(self):
        median = self.get_median()
        min_elt = self.hmin.min_element()
        if median == min_elt:
            self.hmin.delete_min()
            self.balance_heap_sizes()
        else:
            self.hmax.delete_max()

class PriorityQueue:
    # Constructor:  Implement a empty heap data structure for prioritizing Vertex datastructure (from graphs)
    def __init__(self):
        self.q = [None] # pad it with one element

    def insert(self, v=Vertex):
        n = len(self.q)
        self.q.append(v)
        v.idx_in_priority_queue = n
        self.bubble_up(n)
        
    def swap(self, i=Vertex, j=Vertex):
        # Using new in-class function instead of helper function to update the positions of the vertices in the priority queue.
        tmp = self.q[i]
        self.q[i] = self.q[j]
        self.q[i].idx_in_priority_queue = i
        self.q[j] = tmp
        self.q[j].idx_in_priority_queue = j
        
    # Using in-class bubble up and down functions instead of earlier ones because items in queue are Vertex data structure, not ints
    def bubble_up(self, j=Vertex):
        assert j >= 1
        assert j < len(self.q)
        if j == 1:
            return
        val = self.q[j].d
        parent_idx = j // 2
        parent_val = self.q[parent_idx].d
        if val < parent_val:
            self.swap(j, parent_idx)
            self.bubble_up(parent_idx)
        return
    
    def bubble_down(self, j=Vertex):
        n = len(self.q)
        left_child_idx = 2 * j
        right_child_idx = 2 * j + 1
        if left_child_idx >= n:
            return
        if right_child_idx >= n:
            child_idx = left_child_idx
            child_d = self.q[left_child_idx].d
        else:
            (child_d, child_idx) = min ( (self.q[left_child_idx].d, left_child_idx), 
                                         (self.q[right_child_idx].d, right_child_idx)
                                       )
        if self.q[j].d > child_d:
            self.swap(j, child_idx)
            self.bubble_down(child_idx)
        return 
        
    def get_and_delete_min(self):
        # Find the minimum weight vertex and delete it from the heap.
        # returns the deleted vertex back
        n = len(self.q)
        assert n > 1
        v = self.q[1]
        if n > 2: 
            self.q[1] = self.q[n-1]
            self.q[n-1].idx_in_priority_queue = 1
            del self.q[n-1]
            self.bubble_down(1)
        #self.check_invariant()
        return v
    
    def is_empty(self):
        # returns bool
        return len(self.q) == 1
    
    def update_vertex_weight(self, v=Vertex):
        j = v.idx_in_priority_queue
        n = len(self.q)
        assert j >= 0 and j < n
        self.bubble_down(j)
        self.bubble_up(j)