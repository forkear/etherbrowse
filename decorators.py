from flask import redirect, url_for
from functools import wraps
import config 


def use_compiler_or_redirect(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        if not config.USE_COMPILER:
            return redirect(url_for('index'))

        return f(*args, **kwargs)

    return decorator

