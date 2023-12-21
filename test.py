from unittest import TestCase

from if_ import if_

d = {
    'a': 123,
    'c': None,
    'd': {'this': 456},
    'l': [1, 2, 3],
    'f': lambda x: x * 11,
}


class UnitTests(TestCase):

    def test_if_(self):
        assert if_(None).anything.then is None, 'Chain from None is None'
        assert if_(d).anything.then is None, 'Failed accessor in chain returns None'
        assert if_(d)['a'].then == 123, 'Chained dict item getter works normally'
        assert if_(d)['c']['anything'].then is None, 'Failed dict item getter in chain returns None'
        assert if_(d)['l'][1].then == 2, 'Chained list item getter works normally'
        assert if_(d)['l'][5].then is None, 'Failed list item getter in chain returns None'
        assert if_(d)['f'](4).then == 44, 'Chained function call works normally'
