def get_stat(func):

    def wrapper(arr):
        import time
        start = time.time()

        sw, cmp = func(arr)

        return time.time()-start, sw, cmp

    return wrapper
