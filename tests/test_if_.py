import copy
import math
import pickle
from unittest import TestCase

from if_ import if_


class Obj:
    attr = 789

    def method(self, x):
        return x + 1


d = {
    'i': 123,
    'n': None,
    'd': {'this': 456, 'that': False},
    'l': [1, 2, 3, True],
    'f': lambda x: x * 11,
    'o': Obj(),
    'T': True,
    'F': False,
}


class UnitTests(TestCase):

    def test_if_(self):
        self.assertEqual(if_(d)['i']._, 123, 'Dict item works')
        self.assertEqual(if_(d)['d']['this']._, 456, 'Chained dict item works')
        self.assertIs(if_(d)['d']['that']._, False, 'Chained boolean dict item works')
        self.assertEqual(if_(d)['l'][1]._, 2, 'Chained list item works')
        self.assertEqual(if_(d)['f'](4)._, 44, 'Chained function call works')
        self.assertEqual(if_(d)['o'].attr._, 789, 'Chained attribute works')
        self.assertEqual(if_(d)['o'].method(1)._, 2, 'Chained method call works')

    def test_failed(self):
        self.assertIsNone(if_(None).anything._, 'Chain from None is None')
        self.assertIsNone(if_(d).anything._, 'Failed attribute in chain returns None')
        self.assertIsNone(if_(d)['n']['anything']._, 'Failed dict item in chain returns None')
        self.assertIsNone(if_(d)['l'][5]._, 'Failed list item in chain returns None')
        self.assertIsNone(if_(d)['o'].missing(1)._, 'Call on failed attribute returns None')

    def test_if_without_underscore(self):
        self.assertTrue(if_(d)['T'], 'Chained True works without _')
        self.assertFalse(if_(d)['F'], 'Chained False works without _')
        self.assertTrue(if_(d)['i'], 'Chained truthy works without _')
        self.assertFalse(if_(d)['n'], 'Chained falsy works without _')
        self.assertFalse(if_(d)['foo'], 'Bool of chained fail works without _')
        self.assertTrue(if_(d)['i'] == 123, 'Dict item works without _')
        self.assertTrue(if_(d)['foo'] != 123, 'Failed dict item works without _')

    def test_iteration(self):
        self.assertEqual(list(if_(d)['l']), [1, 2, 3, True], 'Iteration yields the value\'s items')
        self.assertIn(2, if_(d)['l'], 'Membership test uses the value')
        self.assertNotIn(5, if_(d)['l'], 'Membership test uses the value')
        with self.assertRaises(TypeError, msg='Iterating a failed chain raises like None'):
            list(if_(d)['foo'])

    def test_repr(self):
        self.assertEqual(repr(if_((1, 2))), '<if_ with value (1, 2)>', 'repr of tuple value works')
        self.assertEqual(repr(if_('None')), "<if_ with value 'None'>", 'repr distinguishes str from None')
        self.assertEqual(repr(if_(None)), '<if_ with value None>', 'repr of None works')

    def test_copy_and_pickle(self):
        self.assertEqual(copy.copy(if_(d)['l'])._, [1, 2, 3, True], 'copy works')
        self.assertEqual(copy.deepcopy(if_(d)['d'])._, d['d'], 'deepcopy works')
        self.assertEqual(pickle.loads(pickle.dumps(if_(d)['d']))._, d['d'], 'pickle works')

    def test_non_chainable(self):
        self.assertIsNone(if_(123)['x']._, 'Item of non-subscriptable value returns None')
        self.assertIsNone(if_(123)()._, 'Call of non-callable value returns None')
        self.assertEqual(if_(list)[int]._, list[int], 'Subscripting a generic class works')

    def test_errors_propagate(self):
        def buggy():
            return None + 1

        class Buggy:
            @property
            def prop(self):
                return self.typo

            def __getitem__(self, key):
                raise TypeError('bug')

        with self.assertRaises(TypeError, msg='TypeError inside a called function propagates'):
            if_(buggy)()
        with self.assertRaises(AttributeError, msg='AttributeError inside a property propagates'):
            if_(Buggy()).prop
        with self.assertRaises(TypeError, msg='TypeError inside __getitem__ propagates'):
            if_(Buggy())['x']
        with self.assertRaises(TypeError, msg='Wrong key type for a list propagates'):
            if_(d)['l']['x']

    def test_hash_and_eq(self):
        self.assertEqual(hash(if_(d)['i']), hash(123), 'Hash matches the value\'s hash')
        self.assertIn(if_(d)['i'], {123}, 'Wrapper can be found in a set of values')
        self.assertTrue(if_(d)['i'] == if_(123), 'Two wrappers compare by value')
        with self.assertRaises(TypeError, msg='Unhashable value makes the wrapper unhashable'):
            hash(if_(d)['l'])

    def test_operators(self):
        i = if_(d)['i']  # 123
        self.assertTrue(i > 100 and i >= 123 and i < 200 and i <= 123, 'Ordering compares the value')
        self.assertTrue(i != 124 and i != if_(124), 'Inequality compares the value')
        self.assertEqual(i + 1, 124, 'Arithmetic uses the value')
        self.assertEqual(1 + i, 124, 'Reflected arithmetic uses the value')
        self.assertEqual(i + if_(1), 124, 'Arithmetic unwraps a wrapped operand')
        self.assertEqual(i - 3, 120)
        self.assertEqual(200 - i, 77)
        self.assertEqual(i * 2, 246)
        self.assertEqual(i / 2, 61.5)
        self.assertEqual(i // 2, 61)
        self.assertEqual(i % 10, 3)
        self.assertEqual(divmod(i, 10), (12, 3))
        self.assertEqual(divmod(1000, i), (8, 16))
        self.assertEqual(i ** 2, 15129)
        self.assertEqual(2 ** if_(3), 8)
        self.assertEqual(pow(i, 2, 10), 9)
        self.assertEqual(i << 1, 246)
        self.assertEqual(i >> 1, 61)
        self.assertEqual(i & 1, 1)
        self.assertEqual(i | 4, 127)
        self.assertEqual(i ^ 1, 122)
        self.assertEqual(-i, -123)
        self.assertEqual(+i, 123)
        self.assertEqual(abs(if_(-5)), 5)
        self.assertEqual(~i, -124)

        n = i
        n += 1
        self.assertEqual(n, 124, 'In-place operators fall back to binary operators')

    def test_conversions(self):
        self.assertEqual(int(if_('7')), 7)
        self.assertEqual(float(if_(d)['i']), 123.0)
        self.assertEqual(complex(if_(1)), 1 + 0j)
        self.assertEqual([10, 20, 30][if_(1)], 20, '__index__ allows use as an index')
        self.assertEqual(round(if_(2.567), 1), 2.6)
        self.assertEqual(round(if_(2.5)), 2)
        self.assertEqual(math.trunc(if_(-2.5)), -2)
        self.assertEqual(math.floor(if_(2.5)), 2)
        self.assertEqual(math.ceil(if_(2.5)), 3)
        self.assertEqual(str(if_(d)['i']), '123', 'str uses the value')
        self.assertEqual(f'{if_(3.14159):.2f}', '3.14', 'format uses the value')
        self.assertEqual(bytes(if_(b'ab')), b'ab')

    def test_containers(self):
        self.assertEqual(len(if_(d)['l']), 4, 'len uses the value')
        self.assertEqual(list(reversed(if_(d)['l'])), [True, 3, 2, 1], 'reversed uses the value')
        self.assertIn(if_(2), if_(d)['l'], 'Membership unwraps a wrapped item')

    def test_failed_chain_operators_act_like_none(self):
        with self.assertRaises(TypeError):
            if_(d)['foo'] + 1
        with self.assertRaises(TypeError):
            if_(d)['foo'] > 1
        with self.assertRaises(TypeError):
            len(if_(d)['foo'])
        self.assertEqual(str(if_(d)['foo']), 'None')
