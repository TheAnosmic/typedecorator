from collections import Sequence
from typedecorator.conf import range_type

try:
    from mock import Mock
except ImportError:
    Mock = None


class Checker(object):
    def __init__(self, is_checker_func, is_valid_func, to_string_func):
        self.is_checker_func = is_checker_func
        self.is_valid_func = is_valid_func
        self.to_string_func = to_string_func

    def is_checker_of(self, obj):
        return self.is_checker_func(obj)

    def is_valid(self, obj):
        return self.is_valid_func(obj)

    def to_string(self, obj):
        return self.to_string_func(obj)


type_checker = Checker(
    lambda t: isinstance(t, type),
    lambda t: True,
    lambda t: t.__name__)

list_checker = Checker(
    lambda t: isinstance(t, list) and len(t) == 1,
    lambda t: _check_constraint_validity(t[0]),
    lambda t: '[%s]' % _constraint_to_string(t[0]))

tuple_checker = Checker(
    lambda t: isinstance(t, tuple),
    lambda t: all(_check_constraint_validity(x) for x in t),
    lambda t: '(%s)' % ', '.join(_constraint_to_string(x) for x in t)
)

dict_checker = Checker(
    lambda t: isinstance(t, dict) and len(t) == 1,
    lambda t: _check_constraint_validity(t.keys()[0]) and \
              _check_constraint_validity(t.values()[0]),
    lambda t: '{%s:%s}' % (_constraint_to_string(t.keys()[0]),
                           _constraint_to_string(t.values()[0]))
)

set_checker = Checker(
    lambda t: isinstance(t, set) and len(t) == 1,
    lambda t: _check_constraint_validity(list(t)[0]),
    lambda t: '{%s}' % _constraint_to_string(list(t)[0])
)

checkers = [
    type_checker,
    list_checker,
    tuple_checker,
    dict_checker,
    set_checker,
]


def _constraint_to_string(t):
    for checker in checkers:
        if checker.is_checker_of(t):
            return checker.to_string(t)
    if isinstance(t, Sequence) and len(t) != 1:
        msg = 'Invalid length for %s, (should be 1)' % type(t)
    else:
        msg = 'Invalid type signature, %s' % type(t)
    raise TypeError(msg)


def _check_constraint_validity(t):
    for checker in checkers:
        if checker.is_checker_of(t):
            return checker.is_valid(t)
    if isinstance(t, Sequence) and len(t) != 1:
        msg = 'Invalid length for %s, (should be 1)' % type(t)
    else:
        msg = 'Invalid type signature, %s' % type(t)
    raise TypeError(msg)


def _verify_type_constraint(v, t):
    if Mock and isinstance(v, Mock):
        return True
    if t is range_type and hasattr(v, '__iter__') and callable(v.__iter__):
        return True
    elif isinstance(t, type):
        return isinstance(v, t)
    elif isinstance(t, list) and isinstance(v, list):
        return all(_verify_type_constraint(vx, t[0]) for vx in v)
    elif isinstance(t, tuple) and isinstance(v, tuple) and len(t) == len(v):
        return all(_verify_type_constraint(vx, tx) for vx, tx in zip(v, t))
    elif isinstance(t, dict) and isinstance(v, dict):
        tk, tv = list(t.items())[0]
        return all(_verify_type_constraint(vk, tk) and
                   _verify_type_constraint(vv, tv) for vk, vv in v.items())
    elif isinstance(t, set) and isinstance(v, set):
        tx = list(t)[0]
        return all(_verify_type_constraint(vx, tx) for vx in v)
    else:
        return False
