'''
Knapsack Problem

A dynamic program that optimizes the sum of elements collected while ensuring that sum is still less than or equal to the target value
The difference between the sum and the target value is minimized.
'''

def targetSum(og_set, index, target):
    # recursive algorithm for finding the difference between the found sum and the target
    index_value = og_set[index]
    last_index = len(og_set) - 1
    if index < last_index:
        take_op = targetSum(og_set, index + 1, target - index_value)
        leave_op = targetSum(og_set, index + 1, target)
        if take_op == None:
            take = 0
        elif take_op < 0:
            take = float('inf')
        else:
            take = take_op
        if leave_op == None:
            leave = 0
        else:
            leave = leave_op
        choice = min(take, leave)
        if choice == take:
            return take_op
        else:
            return leave_op
    elif index == last_index:
        if index_value > target:
            take = float('inf')
        else: 
            take = target - index_value
        leave = target
        choice = min(take, leave)
        if choice == take:      
            target -= index_value
    return target

def memoTargetSum(og_set, target):
    # creates a memoized table of values for indexes and potential target values
    assert target >= 0, "Target is less than 0"
    # Memo table initialized as empty dictionary
    memo_tbl = {}
    set_size = len(og_set)
    for index in reversed(range(set_size + 1)):
        for summation in range(target + 1):
            current_entry = (index, summation)
            if index < set_size:
                index_value = og_set[index]
            if index == set_size:
                memo_tbl[current_entry] = summation
            else:
                if summation - index_value >=  0:
                    take = memo_tbl[(index+ 1, summation - index_value)]
                else:
                    take = float('inf')
                leave = memo_tbl[(index + 1, summation)]
                choice = min(take, leave)
                if choice == take:
                    memo_tbl[current_entry] = take
                else:
                    memo_tbl[current_entry] = leave
    return memo_tbl

def getBestTargetSum(og_set, target):
    # uses memo table to get correct sequence for minimizing the difference between the sum and the target
    assert target >= 0
    # create memoized table and set starting values
    memo_tbl = memoTargetSum(og_set, target)
    index = 0
    # create subset and add proper values
    subset = []
    og_size = len(og_set)
    while index < og_size:
        if target == 0:
            break
        index_value = og_set[index]
        tbl_entry = memo_tbl[(index, target)]
        if target - index_value >= 0:
            take = memo_tbl[(index + 1, target - index_value)]
        else:
            take = float('inf')
        leave = memo_tbl[(index + 1, target)]
        if take < leave:
            subset.append(index_value)
            target -= index_value
        index += 1
    return subset