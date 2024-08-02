import numpy as np

from functools import wraps

def convert_to_numpy(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        new_args = [np.array(arg) if not isinstance(arg, np.ndarray) else arg for arg in args]
        new_kwargs = {k: np.array(v) if not isinstance(v, np.ndarray) else v for k, v in kwargs.items()}
        return func(*new_args, **new_kwargs)
    return wrapper