import inspect
from typing import Any, Callable, Union


def signaturize(func: Callable) -> tuple[dict[str, Any], Union[str, None], Union[int, None], Union[str, None]]:
    """Map the given function's arguments to their default values and also return the name and index of the args parameter if such a parameter exists."""
    
    signature = {}
    args_parameter = None
    args_i = None
        
    for i, parameter in enumerate(inspect.signature(func).parameters.values()):
        # Skip the kwargs parameter.
        if parameter.kind.name == 'VAR_KEYWORD':
            continue
        
        # If the parameter is the args parameter, record its name and index.
        if parameter.kind.name == 'VAR_POSITIONAL':
            args_parameter = parameter.name
            args_i = i
        
        # Set the parameter's default value if it has one, otherwise, use `None` instead of `inspect._empty`.
        signature[parameter.name] = parameter.default if parameter.default != parameter.empty else None
    
    return signature, args_parameter, args_i

def inflate_arguments(signature: dict[str, Any], args_parameter: Union[str, None], args_i: Union[int, None], args: list, kwargs: dict) -> dict[str, Any]:
    """Map arguments to their keywords or the keyword of the args parameter where necessary using the given mapping of a function's arguments to their default values and the name and index of the function's args parameter if such a parameter exists."""
    
    # Copy the signature to avoid modifying the original.
    arguments = signature.copy()
    
    # Map positional arguments to their keywords by zipping the function's arguments with the provided positional arguments truncated to the index of the args parameter if such a parameter exists.
    for argument, positional_argument in zip(arguments, args[:args_i]):
        arguments[argument] = positional_argument
    
    # If the args parameter exists, map the remaining positional arguments to the args parameter.
    if args_parameter is not None:
        arguments[args_parameter] = args[args_i:]
    
    # Merge positional and keyword arguments with the function's arguments.
    arguments |= kwargs
    
    return arguments