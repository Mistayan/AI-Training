import logging
import tracemalloc
from functools import wraps
from time import perf_counter


def measure_perf(func, print_inout=False, print_doc=False):
    """Measure performance of a function/method/class"""

    logger = logging.getLogger("measure_perf")

    @wraps(func)
    def wrapper(*args, **kwargs):
        """ wrapper is like the function it-self.Requires to run the function/method/class in here"""
        not print_doc or logger.debug(f'Method:{func.__doc__}')
        not print_inout or logger.debug(f"input :{args}{kwargs}")
        tracemalloc.start()
        start_time = perf_counter()

        res = func(*args, **kwargs)  # Execute request action

        not print_inout or logger.debug('Output : %s', res)
        finish_time = perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        logger.debug(f"{func.__name__}\n" +
                     f"Time elapsed is seconds: {finish_time - start_time:.6f}\n"
                     f"Memory usage:\t\t {current / 10 ** 6:.6f} MB\n"
                     f"Peak memory usage:\t {peak / 10 ** 6:.6f} MB")
        return res

    return wrapper
