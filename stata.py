class Stat:
    def __init__(self, time, sw, cmp):
        self.time = time
        self.sw = sw
        self.cmp = cmp

    def __repr__(self):
        return "(" + str(self.time) + ", " + str(self.sw) + ", " + str(self.cmp) + ")"


def get_stat(func):

    def wrapper(arr):
        import timeit
        from functools import partial

        ar = arr.copy()

        sw, cmp = func(arr)
        tm = timeit.Timer(partial(func, ar)).repeat(1, 1)[0]

        return Stat(tm, sw, cmp)

    return wrapper
