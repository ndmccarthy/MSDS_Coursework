# Apriori Algorithm

def alpha_in_order(letter1, letter2):
    # helps determine whether letter 1 does in fact go before letter 2
    letters = [letter1, letter2]
    if sorted(letters)[0] == letters[0]:
        return True
    else:
        return False

def found_subset(transaction_list, itemset_list):
    # requires transaction_list and itemset_list to already be sorted
    jj = 0
    ii = 0
    found = []
    while jj < len(transaction_list) and ii < len(itemset_list):
        item = itemset_list[ii]
        trans_item = transaction_list[jj]
        if not alpha_in_order(trans_item, item):
            return False
        else:
            if item == trans_item:
                found.append(item)
                ii += 1
            jj += 1
    if found == itemset_list:
        return True
    return False

def create_freq_dict(transactions: list, items: list, min_count):
    # initialize frequent item dictionary
    freq_dict = {}
    for item in items:
        freq_dict[item] = 0
    # loop through sorted lists in transactions and items
    for transaction in transactions:
        transaction = sorted(transaction)
        for item in items:
            if item is not list:
                item_list = list(item)
            else:
                item_list = sorted(item)
            # check list for sublist (each sorted alphabetically)
            if found_subset(transaction, item_list):
                freq_dict[item] += 1
    # delete keys that have value less than minimum
    delete = []
    for key, value in freq_dict.items():
        if value < min_count:
            delete.append(key)
    for item in delete:
        freq_dict.pop(item)
    return freq_dict

def combine_freq_items(frequent_items: dict):
    indiv_items = sorted(list(frequent_items.keys()))
    item_size = len(indiv_items[0])
    itemset = []
    for ii in range(len(indiv_items)):
        jj = ii + 1
        while jj < len(indiv_items):
            if item_size == 1:
                combined = (indiv_items[ii], indiv_items[jj])
                itemset.append(combined)
            elif item_size == 2:
                # items must have the same beginning in order to be eligible to combine into a new candidate
                if indiv_items[ii][0] == indiv_items[jj][0]:
                    combined = indiv_items[ii] + (indiv_items[jj][-1],)
                    itemset.append(combined)
            else:
                # subtract one for starting at 0 and another for ignoring last element (-2)
                if indiv_items[ii][0:item_size-2] == indiv_items[jj][0:item_size-2]:
                    combined = indiv_items[ii] + (indiv_items[jj][-1],)
                    itemset.append(combined)
            jj += 1
    return itemset

def generate_frequent_itemsets(dataset, support, items, n=1, frequent_items={}):
    
#   Input:
#       1. dataset - A python dictionary containing the transactions.
#       2. support - A floating point variable representing the min_support value for the set of transactions.
#       3. items - A python list representing all the items that are part of all the transactions.
#       4. n - An integer variable representing what frequent item pairs to generate.
#       5. frequent_items - A dictionary representing k-1 frequent sets. 
#   Output:
#       1. frequent_itemsets - A dictionary representing the frequent itemsets and their corresponding support counts.
    transactions = list(dataset.values())
    min_count = len(dataset) * support
    # grab correct frequent items to consider
    if n == 1:
        itemset = items
    else:
        prev_frequent = generate_frequent_itemsets(dataset, support, items, n=n-1)
        itemset = combine_freq_items(prev_frequent)
    freq_itemset = create_freq_dict(transactions, itemset, min_count)
    return freq_itemset




# FP-Growth Algorithm

def item_support(dataset):
    
#   A helper function that returns the support count of each item in the dataset.
#   Input:
#       1. dataset - A python dictionary containing the transactions. 
#       2. min_support - A floating point variable representing the min_support value for the set of transactions.
#   Output:
#       1. support_dict - A dictionary representing the support count of each item in the dataset.
    transactions = list(dataset.values())
    # initialize support dictionary
    support_dict = {}
    items = set()
    for transaction in transactions:
        new_items = set(transaction)
        items.update(new_items)
    for item in items:
        support_dict[item] = 0
    # loop through sorted lists in transactions
    for transaction in transactions:
        # increase count/value for support_dict key of transaction
        for item in transaction:
            support_dict[item] += 1
    return support_dict

def reorder_transactions(dataset, min_support):
    
    '''
        A helper function that reorders the transaction items based on maximum support count. It is important that you finish
        the code in the previous cells since this function makes use of the support count dictionary calculated above.
        Input:
            1. dataset - A python dictionary containing the transactions. 
            2. items - A python list representing all the items that are part of all the transactions.
            3. min_support - A floating point variable representing the min_support value for the set of transactions.
        Output:
            1. updated_dataset - A dictionary representing the transaction items in sorted order of their support counts.
    '''
    pruned_support = item_support(dataset) 
    updated_dataset = dict()
    
    # This loop sorts the transaction items based on the item support counts
    for key, value in dataset.items():
        updated_dataset[key] = sorted(value, key=pruned_support.get, reverse=True)
    
    # Update the following loop to remove items that do not belong to the pruned_support dictionary
    for key, value in updated_dataset.items():
        updated_values = list()
        for item in value:
            if item in pruned_support:
                updated_values.append(item) 
        updated_dataset[key] = updated_values

    return updated_dataset

def build_fp_tree(updated_dataset):
    
#   Input: 
#       1. updated_dataset - A python dictionary containing the updated set of transactions based on the pruned support dictionary.
#   Output:
#       1. fp_tree - A dictionary representing the fp_tree. Each node should have a count and children attribute.
#        
#   HINT:
#       1. Loop over each transaction in the dataset and make and update to the fp_tree dictionary. 
#       2. For each loop iteration store a pointer to the previously visited node and update it's children in the next pass.
#       3. Update the root pointer when you start processing items in each transaction.
#       4. Reset the root pointer for each transaction.
#
#   Sample Tree Output:
#   {'Y': {'count': 3, 'children': {'V': {'count': 1, 'children': {}}}},
#    'X': {'count': 2, 'children': {'R': {'count': 1, 'children': {'F': {'count': 1, 'children': {}}}}}}}
    
    fp_tree = dict()
    for transaction, item_list in updated_dataset.items():
        parent = None
        for item in item_list:
            if parent != None:
                try:
                    parent['children'][item]['count'] += 1
                except:
                    parent['children'][item] = {'count': 1, 'children': {}}
                parent = parent['children'][item]
            else:
                try:
                    fp_tree[item]['count'] += 1
                except:
                    fp_tree[item] = {'count': 1, 'children': {}}
                parent = fp_tree[item]
    return fp_tree

###########################
# TESTING
###########################


data = {'T1': ['C', 'D', 'E'], 
        'T2': ['B', 'C', 'D'], 
        'T3': ['A', 'C', 'D'], 
        'T4': ['A', 'C', 'D', 'E'], 
        'T5': ['A', 'B', 'C', 'D'], 
        'T6': ['B'], 
        'T7': ['D', 'E'], 
        'T8': ['A', 'B', 'C', 'D'], 
        'T9': ['A', 'B', 'D', 'E'], 
        'T10': ['A', 'B', 'C', 'D', 'E']}
items = ['A', 'B', 'C', 'D', 'E']

updated_item_set = reorder_transactions(data, 0.6)
print(updated_item_set)
fp_tree = build_fp_tree(updated_item_set)
print(fp_tree)