# if_

Optional chaining for Python

## Installation

`python setup.py install`

## Usage

Call `if_()` with a Python expression, and chain attribute and item accessors on
the return value, ending with `.then`. If the initial expression evaluates to
`None`, so will the whole chain; if not, each accessor will run normally but if
it fails the chain will return `None`.

## Examples

    In [1]: from if_ import if_

    In [2]: d = {
       ...:     'a': 123,
       ...:     'c': None,
       ...:     'd': {'this': 456},
       ...:     'l': [1, 2, 3],
       ...:     'f': lambda x: x * 11,
       ...: }

    In [3]: if_(None).anything.then is None
    Out[3]: True

    In [4]: if_(d).anything.then is None
    Out[4]: True

    In [5]: if_(d)['a'].then == 123
    Out[5]: True

    In [6]: if_(d)['c']['anything'].then is None
    Out[6]: True

    In [7]: if_(d)['l'][1].then == 2
    Out[7]: True

    In [8]: if_(d)['l'][5].then is None
    Out[8]: True

    In [9]: if_(d)['f'](4).then == 44
    Out[9]: True
