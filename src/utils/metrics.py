import logging
import tracemalloc
from functools import wraps
from time import perf_counter

# @valid_type
# def gibson(any, name: str) -> str :
#     return name


def measure_perf(func, print_inout=False, print_doc=False):
    """Measure performance of a function/method/class
    :rtype: function
    """

    logger = logging.getLogger("measure_perf")

    @wraps(func)
    def wrapper(*args, **kwargs):
        """ wrapper is like the function it-self. Requires to run the function/method/class in here"""
        logger.debug("#" * 45)
        logger.warning(
            f'Function: {func.__qualname__}')
        not print_doc or logger.debug(f'Method:{func.__doc__}')
        tracemalloc.start()
        start_time = perf_counter()
        res = func(*args, **kwargs)
        finish_time = perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        not print_inout or (logger.debug(f"input :{args}{kwargs}") or logger.debug('Output : %s', res))
        logger.debug("-" * 40)
        logger.debug(f'Memory usage:\t\t {current / 10 ** 6:.6f} MB')
        logger.debug(f'Peak memory usage:\t {peak / 10 ** 6:.6f} MB ')
        logger.warning(f'Time elapsed (s): {finish_time - start_time:.6f}')
        logger.debug("#" * 45)
        tracemalloc.stop()
        return res

    return wrapper
