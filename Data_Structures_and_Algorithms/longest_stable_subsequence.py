'''
Longest Stable Subsequence

Input: [a0, a1, ...,an-1]
Output: [ai, ai2, ..., aik]

This program takes a list of integers and calculates the longest stable subsequence such that:
    1) i1 < i2 < ... < ik
    2) ai(j-1) - 1 <= ai(j) <= ai(j+1) + 1
    3) length (k) is maximized
'''


def lssLength(original_list, current_id, previous_id):
    # this is a recursive function for the problem
    # make sure the original list only includes integers
    for item in original_list:
        assert type(item) == int, "Original List contains items that are not integers. Program will not work."
    og_size = len(original_list)
    # run function until it's worked through the whole list; initialize length counter
    while current_id < og_size:
        # for first round, previous_id = -1, so cannot find pre_val
        if previous_id < 0:
            # when previous_id has not been initialized, you may choose whether to take the current_id or not
            cur_val_acceptable = True
        else:
            # if the previous_id has been initialized, then you need to determine if the current value is accentable for choosing
            pre_val = original_list[previous_id]
            current_val = original_list[current_id]
            cur_val_acceptable = bool(abs(current_val - pre_val) <= 1)
        # when the current value is acceptable, you may choose to take or skip it
        # if you skip the current_id, then add one to it and keep the previous_id
        skip = lssLength(original_list, current_id + 1, previous_id)
        if skip is None:
            skip = 0
        if cur_val_acceptable:
            # when you take the current_id, it then takes the place of previous_id and itself is moved up one
            take = lssLength(original_list, current_id + 1, current_id)
            if take is None:
                take = 0
            choice = max(skip, take)
            # if the choice is made to take the current_id, then add one to the length counter
            if choice == take:
                return 1 + choice
            # call the proper recursion
            else:
                return choice
        else:
            # if the current value is not acceptable, you must skip it
            return skip

def memoizeLSS(og_list):
    # this function creates a memoized table of values for each possible set of decisions
    # Initialize the memo table to empty dictionary
    memo_tbl = {} 
    # Now populate the entries for the base case; move from largest to smallest on current id then on previous id
    og_size = len(og_list)
    for cur_id in reversed(range(og_size + 1)):
        for pre_id in reversed(range(-1, og_size)):
            # pad table with zeros; by nature, cur_id can never be past the last element.
            if cur_id == og_size:
                memo_tbl[(cur_id, pre_id)] = 0
                continue
            # by nature, pre_id can never be the cur_id
            if pre_id >= cur_id:
                continue
            # determine if current value is acceptable for taking 
            # cur_id is always acceptable to take when pre_id == -1 because nothing has been chosen yet
            if pre_id == -1:
                cur_val_acceptable = True
            else:
                pre_val = og_list[pre_id]
                cur_val = og_list[cur_id]
                cur_val_acceptable = bool(abs(cur_val - pre_val) <= 1)
            # when the current value is acceptable to add to the subsequence, add 1 to the proper prior amount
            if cur_val_acceptable:
                # initialize possible_previous_takes list with 0 in it in case there are no entries to append.
                possible_previous_takes = [0]
                # look for places in the memo_tbl where the pre_id is the now cur_id
                entries = memo_tbl.keys()
                for entry in entries:
                    temp_cur, temp_pre = entry
                    if temp_pre == cur_id:
                        # check if the entry is a valid predecessor for the current addition based on value
                        if  temp_cur != og_size and abs(og_list[cur_id] - og_list[temp_cur]) <= 1:
                            possible_previous_takes.append(memo_tbl[entry])
                    prev_len = max(possible_previous_takes)
                memo_tbl[(cur_id, pre_id)] = prev_len + 1
            else:
                # when the current value is not acceptable for adding, place the max of the previous take or skip.
                # remember we are filling in the table from end to beginning in the sequence
                if cur_id + 1 == pre_id: 
                    skip = 0
                else:
                    skip = memo_tbl[(cur_id + 1, pre_id)]
                take = memo_tbl[(cur_id + 1, cur_id)]
                memo_tbl[(cur_id, pre_id)] = max(skip, take)
    return memo_tbl

def computeLSS(og_list):
    # this is a dynamic program using the memoized table that retrieves the actual subsequence with the longest length
    subsequence = []
    # create memoized table
    memo_tbl = memoizeLSS(og_list)
    # find first element in longest subsequence
    # pre_id will be -1 because nothing has been chosen, then find cur_id attached to max entry (sub_len)
    # track ids for possible starts
    possible_starts = []
    # track possible lengths
    possible_lens = []
    entries = memo_tbl.keys()
    for entry in entries:
        cur_id, pre_id = entry
        if pre_id == -1:
            possible_lens.append(memo_tbl[(entry)])
            possible_starts.append(cur_id)
    sub_len = max(possible_lens)
    start_id = possible_starts[possible_lens.index(sub_len)] # match starting id to length found
    # move from current id to next id selected until subsequence complete
    og_size = len(og_list)
    # track the expected length remaining
    remain_len = sub_len
    # track which segment of table you're on; begin with first selection
    entry = (start_id, -1)
    cur_id = start_id
    while cur_id < og_size - 1:
        (cur_id, pre_id) = entry
        # determine if cur_id of entry is part of subsequence; recorded_len must have changed
        skipped = (cur_id + 1, pre_id)
        taken = (cur_id + 1, cur_id)
        skipped_len = memo_tbl[skipped]
        taken_len = memo_tbl[taken]
        if pre_id == -1:
                cur_val_acceptable = True
        else:
            pre_val = og_list[pre_id]
            cur_val = og_list[cur_id]
            cur_val_acceptable = bool(abs(cur_val - pre_val) <= 1)
        if taken_len >= skipped_len and memo_tbl[entry] == remain_len and cur_val_acceptable:
            subsequence.append(og_list[cur_id])
            remain_len -= 1
            entry = taken
        else:
            entry = skipped
    if len(subsequence) == 0:
        subsequence.append(og_list[start_id])
    return subsequence