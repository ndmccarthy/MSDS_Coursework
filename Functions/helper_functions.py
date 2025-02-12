# These functions are basic helper functions to make more complex ones easier to write and read.

def is_even(num:int):
    return bool(num % 2 == 0)

def comparison(comparison, first, second):
    if comparison == 'greater than':
        return first > second
    elif comparison == 'less than':
        return first < second
    else:
        return SyntaxError, "Comparison input not valid."
    
def find_second_max(iterable):
    # returns the value of the second largest element in an iterable object
    # requires input to be an iterable without None place holders (only int and/or floats)
    max_elt = max(iterable)
    max_id = iterable.index(max_elt)
    iterable.pop(max_id)
    return max(iterable)

def replace_Nones(iterable, positive:bool):
    # replaces None place holders in an iterable object with positive or negative infinity to make it possible to sort, max, min, etc.
    if positive:
        inf = float('inf')
    else:
        inf = float('-inf')
    for elt in iterable:
        if elt == None:
            elt_id = iterable.index(elt)
            iterable[elt_id] = inf
    return iterable

def swap(iterable, first_id, second_id):
    assert 0 <= first_id < len(iterable), f'accessing index {first_id} beyond end of array {len(iterable)}'
    assert 0 <= second_id < len(iterable), f'accessing index {second_id} beyond end of array {len(iterable)}'
    if first_id == second_id:
        pass
    else:
        iterable[first_id], iterable[second_id] = iterable[second_id], iterable[first_id]