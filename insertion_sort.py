def sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


if __name__ == "__main__":
    import timeit
    import random
    import time

    random.seed(123)
    ar = [random.randint(1, int(1e6)) for i in range(1, int(1e6))]

    print("pass")
    start = time.time()
    sort(ar)
    print(time.time()-start)
    print(timeit.repeat("sort(ar)", "from __main__ import sort, ar",repeat=1, number=1))

    print("end")

