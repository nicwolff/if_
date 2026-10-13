"""Optional chaining for Python.

    if_(data)['user'].address.city._

returns None if any step of the chain is missing, instead of raising.
"""

import math
import operator


def _subscriptable(value):
    return hasattr(type(value), '__getitem__') or (
        isinstance(value, type) and hasattr(value, '__class_getitem__'))


def _unwrap(value):
    return value._ if isinstance(value, if_) else value


def _unary(op):
    def method(self):
        return op(self._)
    return method


def _binary(op):
    def method(self, other):
        return op(self._, _unwrap(other))
    return method


def _reflected(op):
    def method(self, other):
        return op(_unwrap(other), self._)
    return method


class if_:
    """Wrap a value so that attribute, item and call access can be chained.

    Each of those accesses returns a new if_. The chain continues with
    if_(None) when a step is missing: the attribute does not exist on the
    value, the key or index is not found, or the value is not subscriptable
    or not callable. Errors raised inside a property, __getitem__ or called
    function are not caught.

    Get the result with ._. All other operators (comparison, arithmetic,
    bool, len, iter, str, ...) act on the wrapped value directly and return
    a plain result, so on a failed chain they behave as they would on None.
    """

    def __init__(self, maybe):
        self._ = maybe

    def __getattr__(self, key):
        if key == '_' or key.startswith('__') and key.endswith('__'):
            raise AttributeError(key)
        value = self._
        try:
            return if_(getattr(value, key))
        except AttributeError as e:
            # Only a missing attribute on the value ends the chain. An
            # AttributeError raised inside a property is a real error.
            if e.name == key and e.obj is value:
                return if_(None)
            raise

    def __getitem__(self, key):
        value = self._
        if not _subscriptable(value):
            return if_(None)
        try:
            return if_(value[key])
        except LookupError:
            return if_(None)

    def __call__(self, *a, **kw):
        if not callable(self._):
            return if_(None)
        return if_(self._(*a, **kw))

    def __repr__(self):
        return '<if_ with value %r>' % (self._,)

    def __format__(self, spec):
        return format(self._, spec)

    def __round__(self, ndigits=None):
        return round(self._, ndigits)

    def __pow__(self, other, mod=None):
        return pow(self._, _unwrap(other), mod)

    def __rpow__(self, other):
        return pow(_unwrap(other), self._)

    __str__ = _unary(str)
    __bytes__ = _unary(bytes)
    __bool__ = _unary(bool)
    __hash__ = _unary(hash)
    __len__ = _unary(len)
    __iter__ = _unary(iter)
    __reversed__ = _unary(reversed)
    __contains__ = _binary(operator.contains)

    __eq__ = _binary(operator.eq)
    __ne__ = _binary(operator.ne)
    __lt__ = _binary(operator.lt)
    __le__ = _binary(operator.le)
    __gt__ = _binary(operator.gt)
    __ge__ = _binary(operator.ge)

    __neg__ = _unary(operator.neg)
    __pos__ = _unary(operator.pos)
    __abs__ = _unary(abs)
    __invert__ = _unary(operator.invert)

    __int__ = _unary(int)
    __float__ = _unary(float)
    __complex__ = _unary(complex)
    __index__ = _unary(operator.index)
    __trunc__ = _unary(math.trunc)
    __floor__ = _unary(math.floor)
    __ceil__ = _unary(math.ceil)

    __add__ = _binary(operator.add)
    __radd__ = _reflected(operator.add)
    __sub__ = _binary(operator.sub)
    __rsub__ = _reflected(operator.sub)
    __mul__ = _binary(operator.mul)
    __rmul__ = _reflected(operator.mul)
    __matmul__ = _binary(operator.matmul)
    __rmatmul__ = _reflected(operator.matmul)
    __truediv__ = _binary(operator.truediv)
    __rtruediv__ = _reflected(operator.truediv)
    __floordiv__ = _binary(operator.floordiv)
    __rfloordiv__ = _reflected(operator.floordiv)
    __mod__ = _binary(operator.mod)
    __rmod__ = _reflected(operator.mod)
    __divmod__ = _binary(divmod)
    __rdivmod__ = _reflected(divmod)
    __lshift__ = _binary(operator.lshift)
    __rlshift__ = _reflected(operator.lshift)
    __rshift__ = _binary(operator.rshift)
    __rrshift__ = _reflected(operator.rshift)
    __and__ = _binary(operator.and_)
    __rand__ = _reflected(operator.and_)
    __xor__ = _binary(operator.xor)
    __rxor__ = _reflected(operator.xor)
    __or__ = _binary(operator.or_)
    __ror__ = _reflected(operator.or_)
