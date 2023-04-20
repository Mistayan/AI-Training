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
        sp1.plot([i for i in range(len(v))], [i[0] for i in v], label="current", color="red", marker="o", markersize=12,
                 markerfacecolor="yellow", markeredgecolor="blue", markeredgewidth=2)
        sp1.set_ylabel("current Memory (MB)")
        sp2.plot([i for i in range(len(v))], [i[1] for i in v], label="peak", color="blue", marker="o")
        sp2.set_ylabel("peak Memory (MB)")
        sp3.plot([i for i in range(len(v))], [i[2] for i in v], label="time", color="green", marker="o")
        sp3.set_ylabel("time (ns)")
        plt.legend()
        plt.tight_layout()
        plt.show()


def measure_perf(func, print_inout=False, print_doc=False):
    """Measure performance of a function/method/class
    :rtype: function
    """

    logger = logging.getLogger(func.__name__)

    @wraps(func)
    def wrapper(*args, **kwargs):
        """ wrapper is like the function it-self. Requires to run the function/method/class in here"""
        global __my__figures__
        name = func.__name__
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
        logger.warning(f'{func.__name__} : Time elapsed (s): {total_time:.6f}')
        logger.debug("#" * 45)
        __my__figures__[name].append((current, peak, total_time))
        return res

    return wrapper
