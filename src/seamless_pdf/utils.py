"""
Utility functions for document processing.
"""

import time


def timer(func):
    """
    Decorator to measure the execution time of a function.
    """

    def wrapper(*args, **kwargs):
        # 1. Start timer
        start_time = time.perf_counter()

        result = func(*args, **kwargs)
        # 2. End timer / Logging
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Compiled in: {elapsed_time:.5f} seconds")

        return result

    return wrapper
