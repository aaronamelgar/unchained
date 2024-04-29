import functools

evaluation_registry = {}


def register_evaluator(func):
    name = func.__name__

    if name not in evaluation_registry.keys():
        evaluation_registry[name] = func

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
