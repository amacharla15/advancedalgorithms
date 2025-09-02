

"""
    --average runtime 
    --runtime of worstcaseinput


    
    
    """
"""
Amortized Analysis Example in Python
------------------------------------

Definition:
-----------
Amortized analysis studies the *average* cost per operation over a sequence
of operations, even in the worst-case sequence. 

Example: Python list.append(), Hash table insertions when load factor exceeds threshold.
-----------------------------
Python lists are dynamic arrays. Appending to a non-full list takes O(1) time.
When the list is full, it resizes (allocates a larger block and copies items),
which is O(n) for that one operation. However, because capacity grows
geometrically, resizes are rare.

Over m appends:
    Total cost = O(m)  → Amortized cost per append = O(1)

This is why we say list.append() is *amortized O(1)*.
"""

# Simulation of amortized cost for list.append()

arr = []
costs = []

capacity = 0
for i in range(1, 17):
    # Checking if resize is needed
    if len(arr) == capacity:
        # Resizing logic (doubling capacity)
        new_capacity = max(1, capacity * 2)
        copy_cost = len(arr)  # copying old elements
        capacity = new_capacity
    else:
        copy_cost = 0

    arr.append(i)
    actual_cost = 1 + copy_cost  # 1 for insertion + copy cost if any
    costs.append(actual_cost)

print("Operation costs:", costs)
print("Total cost:", sum(costs))
print("Amortized cost per append:", sum(costs) / len(costs))

""" The above one is aggregate method of amortized analysis"""

"""
Accounting method:

"""