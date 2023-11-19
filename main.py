import numpy as np
from ortools.graph.python import max_flow

Teams = {
    7:"A",
    8:"B",
    9:"C",
    10:"D",
    11:"E",
    12:"F",
}

# Instantiate a SimpleMaxFlow solver.
smf = max_flow.SimpleMaxFlow()

# Define three parallel arrays: start_nodes, end_nodes, and the capacities
start_nodes = np.array([
    0,0,0,0,0,0, # From S
    1,1,1,1, # From 1
    2,2,2, # From 2
    3,3,3, # From 3
    4,4,4, # From 4
    5,5,5,5, # From 5
    6,6,6, # From 6
    7, # ...
    8,
    9,
    10,
    11,
    12, # ...
    ])

end_nodes = np.array([ # 7-A 8-B 9-C 10-D 11-E 12-F
    1,2,3,4,5,6, # To 1 2 3 4 5 6
    7,9,10,12, # To A C D F
    8,9,11, # To B C E
    7,8,10, # To A B D
    8,9,11, # To B C E
    7,9,10,12, # To A C D F
    7,11,12, # To A E F
    13, # To T ...
    13, 
    13,
    13,
    13,
    13, # To T 
    ])

capacities = np.array([ # For all edges capatity 1
    1,1,1,1,1,1,
    1,1,1,1,
    1,1,1,
    1,1,1,
    1,1,1,
    1,1,1,1,
    1,1,1,
    1,
    1,
    1,
    1,
    1,
    1,
    ])

# Add arcs in bulk.
all_arcs = smf.add_arcs_with_capacity(start_nodes, end_nodes, capacities)

# Find the maximum flow between source  and tail.
status = smf.solve(0, 13)

if status != smf.OPTIMAL:
    print("There was an issue with the max flow input.")
    print(f"Status: {status}")
    exit(1)
solution_flows = smf.flows(all_arcs)
for arc, flow, capacity in zip(all_arcs, solution_flows, capacities):
    if flow>0 and smf.tail(arc)>=1 and smf.tail(arc)<=6:
        print(f"Project {smf.tail(arc)} can be assigned to team {Teams[smf.head(arc)]}")