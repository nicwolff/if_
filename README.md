# if_

Optional chaining for Python

## Installation

`pip install if_optional`

The distribution is named `if_optional`; the module it installs is `if_`.
Requires Python 3.10 or later.

## Usage

Call `if_()` with a Python expression, and chain attribute, item and call
accessors on the return value, ending with `._`. If the initial expression
evaluates to `None`, so will the whole chain. Otherwise each accessor runs
normally, and if a step is missing the chain returns `None`. A step is missing
when:

- the attribute does not exist on the value,
- the key or index is not found (`KeyError` / `IndexError`),
- the value is not subscriptable, or
- the value is not callable.

Errors raised *inside* a property, a `__getitem__` method or a called function
are not caught, so bugs in your own code still raise. A key of the wrong type,
such as a string index into a list, also raises `TypeError`.

All other operators act on the wrapped value, so you can leave off the `._` in
comparisons, arithmetic, `bool()`, `len()`, `str()`, iteration, `in` and so on.
These return the plain result, not an `if_`. On a failed chain they act on
`None`, so `if_(d)['missing'] + 1` raises `TypeError` just as `None + 1` does.

### Limitations

- A missing value cannot be told apart from a value that is actually `None`:
  `if_({'a': None})['a']._` and `if_({})['a']._` are both `None`.
  Likewise, in a boolean test a missing value and a falsy value (`False`, `0`,
  `''`) both count as false.
- The chain does not short-circuit. In `if_(None).f(expensive())`,
  `expensive()` is still evaluated.
- Attributes named `_` and dunder attributes such as `__name__` can't be
  accessed through the chain.

## Examples

    In [1]: from if_ import if_

    In [2]: d = {
       ...:     'a': 123,
       ...:     'c': None,
       ...:     'd': {'this': 456},
       ...:     'l': [1, 2, 3],
       ...:     'f': lambda x: x * 11,
       ...: }

    In [3]: if_(None).anything._ is None
    Out[3]: True

    In [4]: if_(d).anything._ is None
    Out[4]: True

    In [5]: if_(d)['a']._ == 123
    Out[5]: True

    In [6]: if_(d)['c']['anything']._ is None
    Out[6]: True

    In [7]: if_(d)['l'][1]._ == 2
    Out[7]: True

    In [8]: if_(d)['l'][5]._ is None
    Out[8]: True

    In [9]: if_(d)['f'](4) == 44
    Out[9]: True

    In [10]: if_(d)['a'] + 1
    Out[10]: 124

    In [11]: list(if_(d)['l'])
    Out[11]: [1, 2, 3]

## Running the tests

    python -m unittest
