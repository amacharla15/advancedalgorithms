

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
using multipop stack :

Multipop Stack - Amortized Analysis (Accounting Method)
-------------------------------------------------------

We have three operations:
1. PUSH(x)       -> Put element x on top of the stack
2. POP()         -> Remove top element
3. MULTIPOP(k)   -> Pop up to k elements (or fewer if stack has less)

Worst-case for MULTIPOP is O(n) if k = n, but amortized analysis
shows that over a sequence of m operations, the average cost per
operation is O(1).

Accounting Method:
------------------
We assign an *amortized* cost to operations, possibly higher than
their actual cost, and store "credits" to pay for future work.

Plan:
- PUSH(x): Charge 2 units.
    - 1 unit pays for the actual push.
    - 1 unit is saved as credit *on the element* to pay for its eventual pop.
- POP(): Charge 0 units (already paid for by the element's stored credit).
- MULTIPOP(k): Charge 0 units (each popped element was prepaid when pushed).

Why cost = 2 for PUSH?
----------------------
When we push an element, we know it will be popped exactly once
(sometime in the future, either by POP or MULTIPOP). By charging
2 units now, we cover:
    - The immediate push cost (1 unit).
    - The future pop cost (1 unit), stored as credit.

Because each element gets exactly one extra credit for its pop,
MULTIPOP operations have no unpaid work left to do.

Amortized Cost:
---------------
Over m operations, total charged cost ≤ 2 * (number of pushes) = O(m),
so average per operation is O(1) amortized.


"""

