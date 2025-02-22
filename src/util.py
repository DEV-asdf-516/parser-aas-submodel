import warnings
import functools


def deprecated(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        warnings.warn(
            f"{func.__name__} is deprecated.", DeprecationWarning, stacklevel=3
        )
        return func(*args, **kwargs)

    return wrapper
