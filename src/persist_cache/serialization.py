from typing import Any, Union

import msgspec
import pickle

Msgpackables = Union[str, int, list, dict, bool, float, None]
"""Types that are directly msgpackable."""

# Initialise msgpack encoders and decoders once to speed up subsequent serialization and deserialization.
msgpack_encoder = msgspec.msgpack.Encoder()
msgpack_decoder = msgspec.msgpack.Decoder(type=Msgpackables)

SIGNATURE_SEPARATOR = '\x1c\x1e'
"""A separator used to distinguish between a signature indicating how data has been serialized and the data itself."""

TUPLE_SIGNATURE = f'🌷{SIGNATURE_SEPARATOR}'
"""A signature indicating that serialized data is a tuple."""

SET_SIGNATURE = f'🧺{SIGNATURE_SEPARATOR}'
"""A signature indicating that serialized data is a set."""

FROZENSET_SIGNATURE = f'🧊🧺{SIGNATURE_SEPARATOR}'
"""A signature indicating that serialized data is a frozenset."""

LISTED_SIGNATURES = {TUPLE_SIGNATURE, SET_SIGNATURE, FROZENSET_SIGNATURE}
"""The signatures of data types that are serialized as lists."""

PICKLE_SIGNATURE = f'🥒{SIGNATURE_SEPARATOR}'
"""A signature indicating that serialized data is a pickled object."""

BYTES_SIGNATURE = f'🔟{SIGNATURE_SEPARATOR}'
"""A signature indicating that serialized data is a bytes object."""

BYTEARRAY_SIGNATURE = f'🔢{SIGNATURE_SEPARATOR}'
"""A signature indicating that serialized data is a bytearray."""

# Preserve the lengths of the signatures to avoid having to constantly recompute them.
PICKLE_SIGNATURE_LEN = len(PICKLE_SIGNATURE)
BYTES_SIGNATURE_LEN = len(BYTES_SIGNATURE)
BYTEARRAY_SIGNATURE_LEN = len(BYTEARRAY_SIGNATURE)

STR_SIGNATURES = (PICKLE_SIGNATURE, BYTES_SIGNATURE, BYTEARRAY_SIGNATURE)
"""The signatures of data types that are serialized as strings."""

ABSOLUTELY_DIRECTLY_MSGPACKABLE_TYPES = (bool, float, type(None),)
"""Types that are absolutely directly msgpackable."""

def directly_msgpackable(data: Any) -> bool:
    """Determine whether the provided data is directly msgpackable."""
    
    # Data will be directly msgpackable if:
    # - It is a string and it does not start with any of the signatures of data types that are serialized as strings;
    # - It is an integer and is between -2**63 and 2**64-1, inclusive;
    # - It is a list and all of its elements are directly msgpackable and it is either empty or its first element is not a signature of a data type that is serialized as a list;
    # - It is a dictionary and all of its keys and values are directly msgpackable; or
    # - It is of a type specified by `ABSOLUTELY_DIRECTLY_MSGPACKABLE_TYPES`.
    if (isinstance(data, str) and not any(data.startswith(str_signature) for str_signature in STR_SIGNATURES)) \
        or isinstance(data, int) and -2**63 <= data <= 2**64-1 \
        or (isinstance(data, list) and all(directly_msgpackable(d) for d in data) and (len(data) == 0 or not isinstance(data[0], str) or data[0] not in LISTED_SIGNATURES)) \
        or (isinstance(data, dict) and all(directly_msgpackable(k) and directly_msgpackable(v) for k, v in data.items())) \
        or isinstance(data, ABSOLUTELY_DIRECTLY_MSGPACKABLE_TYPES):
        return True
    
    return False

def make_directly_msgpackable(data: Any) -> Msgpackables:
    """Make the given data capable of being directly serialized to msgpack."""
    
    # If the data is directly msgpackable, return it as is.
    if directly_msgpackable(data):
        return data
    
    # If the data is a tuple, make all of its elements directly msgpackable and return it as a list with a signature indicating that it is a tuple.
    elif isinstance(data, tuple):
            return [TUPLE_SIGNATURE, *[make_directly_msgpackable(d) for d in data]]

    # If the data is a set, make all of its elements directly msgpackable and return it as a list with a signature indicating that it is a set.
    elif isinstance(data, set):
            return [SET_SIGNATURE, *[make_directly_msgpackable(d) for d in data]]

    # If the data is a bytes object, return it as a string with a signature indicating that it is a bytes object.
    elif isinstance(data, bytes):
        return f'{BYTES_SIGNATURE}{data.decode("latin1")}'

    # If the data is a frozenset, make all of its elements directly msgpackable and return it as a list with a signature indicating that it is a frozenset.
    elif isinstance(data, frozenset):
            return [FROZENSET_SIGNATURE, *[make_directly_msgpackable(d) for d in data]]

    # If the data is a bytearray, return it as a string with a signature indicating that it is a bytearray.
    elif isinstance(data, bytearray):
        return f'{BYTEARRAY_SIGNATURE}{data.decode("latin1")}'
    
    # If the data is incapable of other being forced into a directly msgpackable form, pickle it and return it as a string with a signature indicating that it is a pickled object.
    return f'{PICKLE_SIGNATURE}{pickle.dumps(data).decode("latin1")}'

def serialize(data: Any) -> str:
    """Serialize the provided data as msgpack."""
    
    # Force the data into a directly msgpackable form.
    data = make_directly_msgpackable(data)
    
    # Encode the data as msgpack.
    data = msgpack_encoder.encode(data)
    
    return data

def make_pythonic(data: Msgpackables) -> Any:
    """Transform the provided msgpackable data back into Python objects."""
    
    # If the data is a string, check if it has a signature indicating that it is a pickled object, bytes object or bytearray and then decode it to the corresponding object, otherwise return it as is.
    if isinstance(data, str):
        if data.startswith(PICKLE_SIGNATURE):
            return pickle.loads(data[PICKLE_SIGNATURE_LEN:].encode("latin1"))
        
        elif data.startswith(BYTES_SIGNATURE):
            return data[BYTES_SIGNATURE_LEN:].encode("latin1")
        
        elif data.startswith(BYTEARRAY_SIGNATURE):
            return bytearray(data[BYTEARRAY_SIGNATURE_LEN:].encode("latin1"))
        
        return data
    
    # If the data is a list, check if it has a signature indicating that it is a tuple, set or frozenset and then decode it to the corresponding object, otherwise return it as is.
    elif isinstance(data, list):
        if len(data) != 0:
            if data[0] == TUPLE_SIGNATURE:
                return tuple(make_pythonic(d) for d in data[1:])
            
            elif data[0] == SET_SIGNATURE:
                return set(make_pythonic(d) for d in data[1:])
            
            elif data[0] == FROZENSET_SIGNATURE:
                return frozenset(make_pythonic(d) for d in data[1:])
        
        return data
    
    # If the data is neither a string nor a list, return it as is.
    return data

def deserialize(data: str) -> Any:
    """Deserialize the provided msgpack-encoded data."""
    
    # Decode the data.
    data = msgpack_decoder.decode(data)
    
    # Transform the data back into Python objects.
    data = make_pythonic(data)    
    
    return data