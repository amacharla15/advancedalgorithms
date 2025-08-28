"""Masters Theorem implementation."""
"""
general recurrence relation of the form: T(n) = aT(n/b) + f(n)
a>=1, b>1, f(n) = theta(n^k log^p n)

a = number of subproblems created in each step

b = factor by which problem size is reduced in each subproblem

f(n) = cost of work done outside the recursive calls (merge, combine, split, etc.)
"""

"""merge sort pseudo code
arr=[3,1,2,4,1]
low=0
n=len(arr)
high=n-1
def merge_sort(arr,low,high):
    if low>=high:
        return
    mid=low+(high-low)//2
    merge_sort(arr,low,mid)
    merge_sort(arr,mid+1,high)
    merge(arr,low,mid,high)
def merge(arr,low,mid,high):
    arr1=[]
    left=low
    right=mid+1
    while left<=mid and right<=high:
        if arr[left]<=arr[right]:
            arr1.append(arr[left])
            left+=1
        else:
            arr1.append(arr[right])
            right+=1
    while left<=mid:
        arr1.append(arr[left])
        left+=1
    while right<=high:
        arr1.append(arr[right])
        right+=1
    for i in range(len(arr1)):
        arr[low+i]=arr1[i]
merge_sort(arr,low,high)
"""

"""
Conditions and complexities:

T(n) = aT(n/b) + f(n)
a>=1, b>1, f(n) = theta(n^k log^p n)

case 1: if log_b(a) > k then T(n) = theta(n^log_b(a))
case 2: if log_b(a) = k then T(n) = theta(n^k log^(p+1) n)
case 3: if log_b(a) < k then T(n) = if  P>=0 then theta(n^k log^p n) else theta(n^k)
"""

""" Merge Sort Analysis:

T(n) = 2T(n/2) + f(n)
f(n) = theta(n) (merging two sorted halves)
a = 2, b = 2, k = 1, p = 0
log_b(a) = log_2(2) = 1 = k
Case 2 applies: T(n) = theta(n^1 log^(0+1) n) = theta(n log n)
Therefore, the time complexity of Merge Sort is O(n log n).
"""