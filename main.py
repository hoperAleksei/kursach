import gui
import insertion_sort as ins
import random
import timsort

if __name__ == "__main__":
    ar = [random.randint(1, 1000) for i in range(1000)]

    # ins.sort(ar)

    timsort.sort(ar)

    print(ar)
    gui.gui()


