from functools import wraps

import dill as pickle
import lz4.frame


@wraps(pickle.dumps)
def dumps(*args, **kwargs):
    return lz4.frame.compress(pickle.dumps(*args, **kwargs))

@wraps(pickle.loads)
def loads(*args, **kwargs):
    return pickle.loads(lz4.frame.decompress(*args, **kwargs))