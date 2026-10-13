def _subscriptable(value):
    return hasattr(type(value), '__getitem__') or (
        isinstance(value, type) and hasattr(value, '__class_getitem__'))


class if_:
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

    def __bool__(self):
        return bool(self._)

    def __eq__(self, other):
        return self._ == other

    def __iter__(self):
        return iter(self._)

    def __contains__(self, item):
        return item in self._
