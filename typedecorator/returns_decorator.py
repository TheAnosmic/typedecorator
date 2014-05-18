from typedecorator._type_error import _type_error
from typedecorator.checker import _check_constraint_validity, _verify_type_constraint, _constraint_to_string
from typedecorator import conf

def returns(return_type):
    """
    Assert that function returns value of specific type

    Example:

        @returns(int)
        def get_random_number():
            return 4  # http://xckd.com/221/

    See module documentation for more information about type signatures.

    """
    _check_constraint_validity(return_type)

    def deco(fn):
        if not conf._decorator_enabled:
            return fn

        if not hasattr(fn, '__def__site__'):
            if hasattr(fn, '__code__'):
                fc = fn.__code__
            else:
                fc = fn.func_code
            fn.__def_site__ = (fc.co_filename, fc.co_firstlineno, fn.__name__,
                               '')

        def wrapper(*args, **kwargs):
            retval = fn(*args, **kwargs)
            if conf._enabled:
                if retval is None and return_type is not type(None):
                    _type_error("non-void function didn't return a value",
                                stack=fn.__def_site__)
                elif retval is not None and return_type is type(None):
                    _type_error("void function returned a value",
                                stack=fn.__def_site__)
                elif not _verify_type_constraint(retval, return_type):
                    _type_error("function returned value %s not matching "
                                "signature %s" % (repr(retval),
                                                  _constraint_to_string(return_type)),
                                stack=fn.__def_site__)
            return retval

        wrapper.__name__ = fn.__name__
        wrapper.__doc__ = fn.__doc__
        wrapper.__return_type__ = return_type
        return wrapper

    return deco


void = returns(type(None))
void.__doc__ = """Annotate function returning nothing"""

