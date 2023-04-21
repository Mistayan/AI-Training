import logging
import tracemalloc
from functools import wraps
from time import perf_counter

from matplotlib import pyplot as plt

# @valid_type
# def gibson(any, name: str) -> str :
#     return name
__my__figures__ = {}


def show_perfs():
    global __my__figures__
    print("Showing performances"
          "----------------"
          "----------------"
          "----------------")

    for k, v in __my__figures__.items():
        print(f"Showing figures for {k}")
        ### make a graphic with 3 subplots, each will be aligned y axis
        fig, (sp1, sp2, sp3) = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(12, 5))
        fig.suptitle(f"Performance of {k}", fontsize=16)
        sp1.plot([i for i in range(len(v))], [i[0] for i in v], label="memory (MB)", color="red", marker="o")
        sp1.set_ylabel("Memory Usage (MB)")
        sp3.plot([i for i in range(len(v))], [i[1] for i in v], label="time (ns)", color="green", marker="o")
        sp3.set_ylabel("time (ns)")
        plt.legend()
        plt.tight_layout()
        plt.show()


def measure_perf(func):
    """Measure performance of a function/method/class
    pass print_inout=True to print input and output of the function/method/class
    pass print_doc=True to print the docstring of the function/method/class
    :rtype: function
    """

    logger = logging.getLogger(func.__name__)

    @wraps(func)
    def wrapper(*args, **kwargs):
        """ wrapper is like the function it-self. Requires to run the function/method/class in here"""
        global __my__figures__
        name = func.__name__
        print_doc = kwargs.pop("print_doc", False)
        print_inout = kwargs.pop("print_inout", False)
        if name not in __my__figures__:
            __my__figures__[name] = []
            print(f"Creating figure for {args[0].__class__.__name__}")
        logger.debug(f"Running {func.__name__}")
        logger.debug("#" * 45)
        not print_doc or logger.debug(f'Method:{func.__doc__}')
        tracemalloc.start()
        start_time = perf_counter()
        res = func(*args, **kwargs)
        total_time = perf_counter() - start_time
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        not print_inout or (logger.debug(f"input :{args}{kwargs}") or logger.debug('Output : %s', res))
        logger.debug("-" * 40)
        current = current / 10 ** 6
        peak = peak / 10 ** 6
        logger.debug(f'Memory usage:\t\t {current:.6f} MB')
        logger.debug(f'Peak memory usage:\t {peak:.6f} MB ')
        logger.debug(f'Total memory usage:\t {peak:.6f} MB ')
        logger.warning(f'{func.__name__} : Time elapsed (s): {total_time:.6f}')
        logger.debug("#" * 45)
        __my__figures__[name].append((peak - current, total_time))
        return res

    return wrapper
