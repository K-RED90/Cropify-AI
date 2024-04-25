import time
import logging
from functools import wraps

log_file = "logger.log"

def log_function_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logging.basicConfig(filename=log_file, level=logging.INFO)
        logging.info(f"Function {func.__name__} started")
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logging.info(f"Function {func.__name__} completed in {execution_time:.6f} seconds")
        return result
    return wrapper