import logging
import tracemalloc
from functools import wraps
from time import perf_counter


def measure_perf(func, print_inout=False, print_doc=False):
    """Measure performance of a function/method/class"""

    logger = logging.getLogger("measure_perf")


    @wraps(func)
    def wrapper(*args, **kwargs):
        """ wrapper is like the function it-self. Requires to run the function/method/class in here"""
        logger.debug("#" * 45)
        logger.debug(f'Function: {func.__name__}')
        not print_doc or logger.debug(f'Method:{func.__doc__}')
        not print_inout or logger.debug(f"input :{args}{kwargs}")
        tracemalloc.start()
        start_time = perf_counter()
        res = func(*args, **kwargs)
        not print_inout or logger.debug('Output : %s', res)
        logger.debug("-" * 40)
        finish_time = perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        logger.debug(f'Memory usage:\t\t {current / 10 ** 6:.6f} MB')
        logger.debug(f'Peak memory usage:\t {peak / 10 ** 6:.6f} MB ')
        logger.debug(f'Time elapsed is seconds: {finish_time - start_time:.6f}')
        logger.debug("#" * 45)
        tracemalloc.stop()
        return res

    return wrapper
