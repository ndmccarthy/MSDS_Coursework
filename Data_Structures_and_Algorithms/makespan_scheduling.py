"""
Makespan Scheduling

Makespan is the total time it takes to finish a set of tasks.
This is a greedy algorithm designed to minimize the maximum makespan.

Inputs: a list of n jobs that take time (T1, ..., Tn), represented as a list
Outputs: a list of assignments (A1, ..., An) of which processor will do the job

There are m number of processors available.
"""

import heapq as hq

def compute_makespan(times=list, processors=int, assignments=list):
    # returns the maximum makespan of a processor
    makespan = 0
    for processor in range(processors):
        temp_makespan = 0
        for task in range(len(assignments)):
            assigned_proc = assignments[task]
            if assigned_proc == processor:
                temp_makespan += times[task]
        if temp_makespan > makespan:
            makespan = temp_makespan
    return makespan

def greedy_makespan_min(times=list, processors=int):
    # Returns a tuple of two things: 
    #    - Assignment list of job numbers from 0 to m-1
    #    - The makespan of your assignment
    assert len(times) >= 1
    assert all(elt >= 0 for elt in times)
    assert processors >= 2
    jobs = len(times)
    # create processor object to place in priority queue
    class processor:
        def __init__(self, id):
            self.id = id
            self.mksp = 0
        
        def __lt__(self, other):
            return self.mksp < other.mksp
        
        def __repr__(self):
            return f'({self.id}, {self.mksp})'
    # initialize a list of processors then turn into a heap
    priorityq = []
    for ii in range(processors):
        new_proc = processor(ii)
        priorityq.append(new_proc)
    hq.heapify(priorityq)
    # initialize assignments list
    assignments = [None]*jobs
    # find processor with smallest makespan and assign job there
    for job in range(len(times)):
        proc_min = priorityq[0]
        assignments[job] = proc_min.id
        # remember to change makespan and reorganize priorityq
        job_time = times[job]
        proc_min.mksp += job_time
        hq.heapify(priorityq)
    # compute makespan
    makespan = compute_makespan(times, processors, assignments)
    return (assignments, makespan)