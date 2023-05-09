"""
Basic Exercise
Please write a function that sorts 11 small numbers (<100) as fast as possible. Once written, 
provide an estimate for how long it would take to execute that function 10 Billion 
(10^10) times on a normal machine.

I decided do an implementation of the quicksort algorithm, that as it follows
a divide and conquer strategi on average is O(n log n).

So for a billion, more or less it could take 

I time it and for 10 elements is around 0.000006 or 6µs
So for a 10 billion

(10^9 log 10^9 ) 6µs = 180000s = 50 hours more or less

"""


def quickshort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)
