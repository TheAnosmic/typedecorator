import traceback
from typedecorator import conf

def _type_error(msg, stack=None):
    if not conf._enabled:
        return

    if conf._loglevel:
        if not stack:
            stack = traceback.extract_stack()[-4]
        path, line, in_func, instr = stack
        if instr:
            instr = ': ' + instr
        log_msg = 'File "%s", line %d, in %s: %s%s' % (
            path, line, in_func, msg, instr)

        conf._logger.log(conf._loglevel, log_msg)

    if conf._exception:
        raise conf._exception(msg)