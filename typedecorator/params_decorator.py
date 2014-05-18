from typedecorator import _type_error
from typedecorator.checker import _check_constraint_validity, _verify_type_constraint, _constraint_to_string
from typedecorator import conf


def params(**types):
    """
    Assert that function is called with arguments of correct types

    Example:

        @params(a=int)
        def double(a):
            return a * 2

    See module documentation for more information about type signatures.

    Note: this decorator must be used directly on the function being annotated
    (ie. there should be no other decorators "between" this one and the
    function), because it inspects the function argument declarations.

    This means that, if using both @returns and @params, @returns must go
    first, as in this example:

        @returns(int)
        @params(a=int, b=int)
        def add(a, b):
            return a + b

    """

    for arg_name, arg_type in types.items():
        _check_constraint_validity(arg_type)

    def deco(fn):
        if not conf._decorator_enabled:
            return fn

        if hasattr(fn, '__return_type__'):
            raise TypeError('You must use @returns before @params')

        if hasattr(fn, '__code__'):
            fc = fn.__code__
        else:
            fc = fn.func_code

        if not hasattr(fn, '__def__site__'):
            fn.__def_site__ = (fc.co_filename, fc.co_firstlineno, fn.__name__,
                               '')

        arg_names = fc.co_varnames[:fc.co_argcount]
        if any(arg not in arg_names for arg in types.keys()) \
                or any(arg not in types for arg in arg_names):
            raise TypeError("Annotation doesn't match function signature")

        def wrapper(*args, **kwargs):
            if conf._enabled:
                for arg, name in zip(args, arg_names):
                    if not _verify_type_constraint(arg, types[name]):
                        _type_error("argument %s = %s doesn't match "
                                    "signature %s" % (name, repr(arg),
                                                      _constraint_to_string(types[name])))

                for k, v in kwargs.items():
                    if k not in types:
                        _type_error("unknown keyword argument %s "
                                    "(positional specified as keyword?)" % k)
                    if not _verify_type_constraint(v, types[k]):
                        _type_error("keyword argument %s = %s "
                                    "doesn't match signature %s" % (k, repr(v),
                                                                    _constraint_to_string(types[k])))
            return fn(*args, **kwargs)

        wrapper.__name__ = fn.__name__
        wrapper.__doc__ = fn.__doc__
        return wrapper

    return deco
