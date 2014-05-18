#!/usr/bin/env python
# Copyright (C) 2014. Senko Rasic <senko.rasic@goodcode.io>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
A decorator-based implementation of type checks.

Provides @params, @returns and @void decorators for annotating function
parameters, return value and the non-existence of return value, respectively.

Both @params and @returns take type signatures that can describe both simple
and complex types.

A type signature can be:

1. A type, such as `int`, `str`, `bool`, `object`, `dict`, `list`, or a
custom class, requiring that the value be of specified type or a subclass of
the specified type. Since every type is a subclass of `object`, `object`
matches any type.

2. A list containing a single element, requiring that the value be a list of
values, all matching the type signature of that element. For example, a type
signature specifying a list of integers would be `[int]`.

3. A tuple containing one or more elements, requiring that the value be a tuple
whose elements match the type signatures of each element of the tuple. For
eample, type signature `(int, str, bool)` matches tuples whose first element
is an integer, second a string and third a boolean value.

4. A dictionary containing a single element, requiring that the value be a
dictionary with keys of type matching the dict key, and values of type
matching the dict value. For example, `{str:object}` describes a dictionary
with string keys, and anything as values.

5. A set containing a single element, requiring that the value be a set
with elements of type matching the set element. For example, `{str}` matches
any set consisting solely of strings.

6. `xrange` (or `range` in Python 3), matching any iterator.

These rules are recursive, so it is possible to construct arbitrarily
complex type signatures. Here are a few examples:

* `{str: (int, [MyClass])}` - dictionary with string keys, where values are
    tuples with first element being an integer, and a second being a list
    of instances of MyClass

* `{str: types.FunctionType}` - dictionary mapping strings to functions

* `{xrange}` - set of iterators

Note that `[object]` is the same as `list`, `{object:object}` is the same
as `dict` and `{object}` is the same as  `set`.

"""

from params_decorator import params
from returns_decorator import returns, void
from conf import setup_typecheck

__version__ = '0.0.3'

__all__ = ['returns', 'void', 'params', 'setup_typecheck']




