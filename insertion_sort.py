import numba
import stata
import speed


@speed.faster
@stata.get_stat
@numba.njit(parallel=False, cache=False)
def sort(arr: "list like") -> (int, int):
    """
    Insertion sort.

    Sorting array.

    Returns swap and compare count.

    :param arr: list
    :return (sw, cmp): (int, int)
    """

    sw = 0
    cmp = 0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1

            sw += 1
            cmp += 1
        else:
            if j >= 0:
                cmp += 1
        arr[j + 1] = key
    return sw, cmp


if __name__ == "__main__":
    import timeit
    import random

    # import time

    # @stat.get_stat
    # def s(): sort
    # random.seed(123)

    ar = [random.randint(1, int(1e6)) for i in range(1, int(32))]
    # ar = numpy.array(ar, int)

    print("pass")

    # print(ar)
    # s(ar)
    print(sort(ar))

    # print(ar)

    print(timeit.repeat("sort(ar)", "from __main__ import sort, ar", repeat=1, number=1))

    # print("end")
