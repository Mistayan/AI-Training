import tracemalloc
from functools import wraps
from time import perf_counter


def measure_perf(func):
    """Measure performance of a function/method/class"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """ wrapper is like the function it-self. Requires to run the function/method/class in here"""
        print("#"*45)
        print(f'Function: {func.__name__}')
        print(f'Method:\n{func.__doc__}')
        print(f"input :\n{args}\n{kwargs}")
        tracemalloc.start()
        start_time = perf_counter()
        res = func(*args, **kwargs)
        print(f'Output :\n{"-" * 40}')
        print(res)
        print(f'{"-" * 40}')
        finish_time = perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        print(f'Memory usage:\t\t {current / 10 ** 6:.6f} MB \n'
              f'Peak memory usage:\t {peak / 10 ** 6:.6f} MB ')
        print(f'Time elapsed is seconds: {finish_time - start_time:.6f}')
        print("#"*45)
        tracemalloc.stop()
        return res

    return wrapper
