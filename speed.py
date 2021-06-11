import numpy


def faster(func):
    def wrapper(arr):
        if isinstance(arr, list):
            ar = numpy.array(arr)
            return func(ar)
        else:
            return func(arr)
    return wrapper
