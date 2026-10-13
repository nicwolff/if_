import copy
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
