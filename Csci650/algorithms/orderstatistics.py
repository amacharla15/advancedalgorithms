"""
Finding kth smallest element in  a list 
Naive approach is to sort the list and return the kth element:

Quickselect algorithm algorithm medin of medians where 5 groups of partitioning is done 

We want a deterministic way to pick a pivot for Quickselect/Quicksort that guarantees balanced partitions (avoids worst-case O(n^2)).
Median-of-medians gives a pivot that’s always “close enough” to the true median, enabling linear-time selection.

---

## Algorithm (Groups of 5)

**Input:** Unsorted array A, target order statistic k (for selection)  
**Output:** A pivot value p with guaranteed balance

1. **Chunk:** Split A into ⌈n/5⌉ groups of size 5 (last may have < 5).
2. **Sort each group:** (constant work per group; size is fixed).
3. **Take medians:** From each group, record the median (3rd smallest in size-5).
4. **Recurse on medians:** Compute the **median of these medians**; call it p.
5. **Partition A by p:** Elements ≤ p left, elements > p right.
6. **Recurse** on the side that contains the target rank (Quickselect), or recurse on both sides (Quicksort).

---

## The Key Condition (Balance Guarantee)

Using groups of 5, the pivot p (median of medians) satisfies:

- At least **30%** of all elements are **≤ p**
- At least **30%** of all elements are **≥ p**

Equivalently, after partitioning around p, **each side has ≥ 3n/10 elements** (up to small constants from edges/leftovers).
This prevents pathological splits and yields **O(n)** selection.

---

## Why 30%? (Tight, quick proof)

Let n be the number of elements and form ⌈n/5⌉ groups.

- In each size-5 group, the median is the 3rd smallest element.
- When we take the median of these medians as pivot p, at least **half** of the group-medians are **≥ p**.
- For each median ≥ p, in its group there are at least **3 elements ≥ p** (the median itself and the two larger ones).

Therefore, from at least **half** of the groups, each contributes **3 elements ≥ p**.

Counting those: roughly **#groups ≈ n/5**, so **#groups with median ≥ p ≥ (1/2)·(n/5) = n/10**.  
Each such group contributes **3 elements ≥ p**, so we get **3·(n/10) = 3n/10** elements ≥ p.

By symmetry, the same lower bound holds for elements ≤ p. Hence each side has at least **3n/10** elements ⇒ **30% guarantee**.

*(Edge cases with the last short group subtract only small constants and don’t affect the linear bound.)*

---

## Complexity (Quickselect with this pivot)

Let T(n) be the time to select.

- Split into 5’s + sort each small group: **O(n)** (constant per group).
- Recurse on medians: **T(n/5)**.
- Partition by pivot: **O(n)**.
- Recurse on the “big” side of size at most **7n/10** (since one side is ≤ 7n/10 by the 30% rule): **T(7n/10)**.

**Recurrence:** T(n) = T(n/5) + T(7n/10) + O(n) = **O(n)**.

---

## Worked Example (n = 25)

Array (unsorted):  
[13, 2, 9, 4, 8, 7, 1, 5, 3, 10, 11, 6, 20, 18, 12, 25, 23, 21, 22, 24, 17, 15, 19, 14, 16]

**Groups of 5 → sort each:**  
- [2, 4, 8, 9, 13] → median **8**  
- [1, 3, 5, 7, 10] → median **5**  
- [6, 11, 12, 18, 20] → median **12**  
- [21, 22, 23, 24, 25] → median **23**  
- [14, 15, 16, 17, 19] → median **16**

**Medians array:** [8, 5, 12, 23, 16] → median is **12** ⇒ pivot p = 12

**Partition by 12:**  
Left (≤ 12): many elements …  
Right (> 12): many elements …  
Both sides are guaranteed reasonably large (≥ 30% of 25 ≈ at least 7–8 elements each, up to constants).

---

## Where to use it

- **Quickselect (k-th smallest):** Deterministic **linear time** in worst case.
- **Quicksort:** Using MoM for every pivot is theoretical; in practice, random/median-of-3 is faster. MoM is used when you need **guarantees** (adversarial inputs, real-time bounds).

---

## Pseudocode (selection; C++-style structure, no heavy language specifics)

```
SELECT(A, k):
    if |A| <= 5:
        sort(A)
        return A[k]             // k is 0-indexed order statistic

    // 1) groups of 5 and their medians
    groups = chunk(A, 5)
    medians = []
    for G in groups:
        sort(G)                      // size <= 5
        medians.push( G[ |G|/2 ] )   // median of small group

    // 2) pivot via recursive median of medians
    p = SELECT(medians, |medians|/2)

    // 3) partition by p
    L = [ x in A where x < p ]
    E = [ x in A where x = p ]
    R = [ x in A where x > p ]

    // 4) recurse into the bucket containing k
    if k < |L|:
        return SELECT(L, k)
    else if k < |L| + |E|:
        return p                     // k falls inside equal bucket
    else:
        return SELECT(R, k - |L| - |E|)
```

**Invariants at partition:** |L| ≥ 3n/10 − O(1) and |R| ≥ 3n/10 − O(1).  
This keeps recursion depth under control ⇒ **O(n)** total.

---

## Common Pitfalls

- **Not sorting groups:** You must sort (or explicitly pick the 3rd of 5) to get the true median per group.
- **Wrong group size:** 5 is standard; 3 works but yields weaker bounds; 7+ also works but increases overhead.
- **Mixing up ranks:** Be consistent with 0-indexed vs 1-indexed order statistics.

---

## TL;DR

Median-of-medians (groups of 5) picks a pivot p so that **≥ 30%** of elements are **≤ p** and **≥ 30%** are **≥ p**.  
This guarantees balanced partitions ⇒ **linear-time** Quickselect and robust Quicksort behavior under adversarial inputs.
"""