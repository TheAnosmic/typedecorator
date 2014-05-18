import logging

_decorator_enabled = True  # whether the decorators should install the wrappers
_enabled = False  # whether the wrappers should do anything at runtime
_logger = logging.getLogger(__name__)
_loglevel = None  # logging.LOGLEVEL to use
_exception = False  # exception to throw on type error (eg. TypeError)

try:
    range_type = xrange
except NameError:
    range_type = range



def setup_typecheck(enabled=True, exception=TypeError, loglevel=None):
    """
    Enable and configure type checking

    Call this function once to configure how the type checking subystem should
    behave. Calling it multiple times only updates the configuration values,
    and can be used to disabling and re-enabling the checks at runtime.

    :param bool enabled:
        Whether to enable type checks of any kind (default: True).
    :param Exception exception:
        Which exception to raise if type check fails (default: TypeError)
        Setting this to None disables raising the exception.
    :param int loglevel:
        Log level at which to log the type error (default: None), see the
        standard `logging` module for possible levels. If None, disables
        logging the type error.

    By default, the type checking system is inactive unless activated through
    this function. However, the type-checking wrappers are in place, so the
    type checking can be enabled or disabled at runtime (multiple times).
    These wrappers do incur a very small but real performance cost. If you
    want to disable the checks at "compile" time, call this function with
    `enabled=False` *before* defining any functions or methods using the
    typecheck decorator.

    For example, if you have a `config.py` file with `USE_TYPECHECK` constant
    specifying whether you want the type checks enabled:

        #!/usr/bin/env python

        from typecheck import setup_typecheck, params
        import config

        setup_typecheck(enabled=config.USE_TYPECHECK)

        @params(a=int, b=int):
        def add(a, b):
            return a + b

    Note that in this case, the checks cannot be enabled at runtime.

    """

    global _decorator_enabled, _enabled, _loglevel, _exception

    _enabled = _decorator_enabled = enabled
    _exception = exception
    _loglevel = loglevel

