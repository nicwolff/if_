class if_:
    def __init__(self, maybe):
        self.value = maybe

    def next_if(self, fn):
        try:
            return if_(fn())
        except (AttributeError, LookupError, TypeError):
            return if_(None)

    def __getattr__(self, key, *a, **kw):
        return self.next_if(lambda: getattr(self.value, key, *a, **kw))

    def __getitem__(self, key):
        return self.next_if(lambda: self.value[key])

    def __call__(self, *a, **kw):
        return self.next_if(lambda: self.value(*a, **kw))

    @property
    def then(self):
        return self.value
