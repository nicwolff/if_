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
