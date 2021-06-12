import numba
import numpy
import stata
import speed

MIN_MERGE = 32


@numba.njit(parallel=False)
def calc_min_run(n):
    """Returns the minimum length of a
    run from 23 - 64 so that
    the len(array)/minrun is less than or
    equal to a power of 2.

    e.g. 1=>1, ..., 63=>63, 64=>32, 65=>33,
    ..., 127=>64, 128=>32, ...
    """
    r = 0
    while n >= MIN_MERGE:
        r |= n & 1
        n >>= 1
    return n + r


# This function sorts array from left index to
# to right index which is of size almost RUN

@numba.njit(parallel=False)
def insertion_sort(arr, left, right):
    sw = 0
    cmp = 0
    for i in range(left + 1, right + 1):
        j = i
        while j > left and arr[j] < arr[j - 1]:
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            j -= 1

            sw += 1
            cmp += 1
        else:
            if j > left:
                cmp += 1

    return sw, cmp


# Merge function merges the sorted runs

@numba.njit(parallel=False)
def merge(arr, l, m, r):
    sw = 0
    cmp = 0
    # original array is broken in two parts
    # left and right array
    len1, len2 = m - l + 1, r - m
    left, right = [], []
    for i in range(0, len1):
        left.append(arr[l + i])
    for i in range(0, len2):
        right.append(arr[m + 1 + i])

    i, j, k = 0, 0, l

    # after comparing, we merge those two array
    # in larger sub array
    while i < len1 and j < len2:
        sw += 1
        cmp += 1
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1

        else:
            arr[k] = right[j]
            j += 1

        k += 1

    # Copy remaining elements of left, if any
    while i < len1:
        arr[k] = left[i]
        k += 1
        i += 1

    # Copy remaining element of right, if any
    while j < len2:
        arr[k] = right[j]
        k += 1
        j += 1

    return sw, cmp


# Iterative Timsort function to sort the
# array[0...n-1] (similar to merge sort)

@speed.faster
@stata.get_stat
@numba.njit(parallel=False)
def sort(arr):
    """
        Timsort.

        Sorting array.

        Returns swap and compare count.

        :param arr: list
        :return (sw, cmp): (int, int)
        """

    sw = 0
    cmp = 0
    n = len(arr)
    min_run = calc_min_run(n)

    # Sort individual subarrays of size RUN
    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        a = insertion_sort(arr, start, end)
        sw += a[0]
        cmp += a[1]

    # Start merging from size RUN (or 32). It will merge
    # to form size 64, then 128, 256 and so on ....
    size = min_run
    while size < n:

        # Pick starting point of left sub array. We
        # are going to merge arr[left..left+size-1]
        # and arr[left+size, left+2*size-1]
        # After every merge, we increase left by 2*size
        for left in range(0, n, 2 * size):

            # Find ending point of left sub array
            # mid+1 is starting point of right sub array
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), (n - 1))

            # Merge sub array arr[left.....mid] &
            # arr[mid+1....right]
            if mid < right:
                a = merge(arr, left, mid, right)
                sw += a[0]
                cmp += a[1]

        size = 2 * size

    return sw, cmp


if __name__ == "__main__":
    import timeit
    import random
    import time

    random.seed(123)
    ar = [random.randint(1, int(1e6)) for i in range(int(1e6))]

    ar = numpy.array(ar)

    print(ar)

    print("pass")
    start1 = time.time()
    print(sort(ar))
    print(time.time() - start1)
    print(timeit.repeat("sort(ar)", "from __main__ import sort, ar", repeat=1, number=4))

    print("end")
